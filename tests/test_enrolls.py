import random
import unittest
from datetime import datetime, timedelta

from app import create_app, db
from app.auth import generate_user_token, TEACHER_PERMISSIONS, \
    STUDENT_PERMISSIONS
from app.models import Teacher, Exam, Student, StudentSubscription
from tests.sample_exams import generate_random_exam


class EnrollTestCase(unittest.TestCase):
    app = None
    app_context = None
    client = None
    tokens_dict = None
    users = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.app_context.pop()

    def check_fields_list(self, data, fields):
        """Check data dictionary for fields"""
        for field in fields:
            self.assertIn(field, data)

    def check_enroll_list_fields(self, data):
        """Check the json response dictionary fields for list exams fields"""
        fields = ['success', 'exams_count', 'search_count',
                  'start', 'end', 'exams']
        self.check_fields_list(data, fields)

    def test_list_enrolled_exam_student(self):
        """List of the exams the student is enrolled to"""
        students = Student.get_query().all()
        tokens = [generate_user_token(student.username, STUDENT_PERMISSIONS)
                  for student in students]
        total_exams_enrolls = StudentSubscription.get_query().count()
        for token, student in zip(tokens, students):
            res = self.client.get('/api/v1/enrolls',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 200, [student, res.get_json()])
            data = res.get_json()
            self.check_enroll_list_fields(data)
            self.assertGreater(total_exams_enrolls, 0)
            total_exams_enrolls -= data['exams_count']
        self.assertEqual(total_exams_enrolls, 0)

    def test_list_enrolled_exam_teacher(self):
        """Teachers cannot enroll to exams"""
        teachers = Teacher.get_query().all()
        for teacher in teachers:
            token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
            res = self.client.get('/api/v1/enrolls',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 403)

    def test_list_enrolled_students_teacher(self):
        """Return the names of students enrolled to one exam"""
        teacher = Teacher.get_query().first()
        exams = Exam.get_query().filter(Exam.author_id == teacher.id).all()
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        for exam in exams:
            res = self.client.get(f'/api/v1/enrolls/{exam.id}',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 200, res.get_json())
            data = res.get_json()
            self.check_fields_list(data, ['success', 'students'])
            self.assertTrue(data['success'])
            enroll_count = (StudentSubscription
                            .get_query()
                            .filter(StudentSubscription.exam_id == exam.id)
                            .count())
            self.assertEqual(len(data['students']), enroll_count)

    def test_list_enrolled_students_student(self):
        """Students cannot list who is enrolled to one exam"""
        students_subscriptions = StudentSubscription.get_query().limit(10)
        for student_subscription in students_subscriptions:
            student = Student.get_by_id(student_subscription.student_id)
            token = generate_user_token(student.username, STUDENT_PERMISSIONS)
            res = self.client.get(
                f'/api/v1/enrolls/{student_subscription.exam_id}',
                headers={'Content-Type': 'application/json',
                         'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 403, res.get_json())

    def test_list_enrolled_students_others_exams(self):
        """Teacher cannot list enrolled students of another teacher's exam"""
        teacher1 = (Teacher.get_query()
                    .join(Exam).order_by(Teacher.id).first())
        teacher2 = (Teacher.get_query()
                    .join(Exam).order_by(Teacher.id.desc()).first())
        exam1 = Exam.get_query().filter(Exam.author_id == teacher1.id).first()
        exam2 = Exam.get_query().filter(Exam.author_id == teacher2.id).first()
        tests_cases = ((teacher1, exam2), (teacher2, exam1))
        for teacher, exam in tests_cases:
            token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
            res = self.client.get(
                f'/api/v1/enrolls/{exam.id}',
                headers={'Content-Type': 'application/json',
                         'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 403, res.get_json())

    def test_enroll_students_to_exam_as_student(self):
        """Student can enroll him self to one exam"""
        exams_ids = [exam.id for exam in Exam.get_query().all()]
        # Select 5 students
        students = Student.get_query().limit(5).all()
        students_enrolls = {
            student.id: (
                subscription.exam_id
                for subscription in StudentSubscription
                .get_query()
                .filter(
                StudentSubscription.student_id == student.id)
                .all()) for student in students}
        # Determine which exams the students is not enrolled in
        students_not_enrolled = {
            student_id: set(exams_ids) - set(exams_ids_)
            for student_id, exams_ids_ in students_enrolls.items()}
        sub_count_before = StudentSubscription.get_query().count()
        try:
            for student in students:
                # Enroll the student in all the exams he is not enrolled to
                token = generate_user_token(student.username,
                                            STUDENT_PERMISSIONS)
                for exam_id in students_not_enrolled[student.id]:
                    res = self.client.post(
                        f'/api/v1/enrolls/{exam_id}',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': f'bearer {token}'},
                        json=[])
                    self.assertEqual(res.status_code, 200, res.get_json())
                    data = res.get_json()
                    self.check_fields_list(data, ['success', 'new_enrolls'])
                    # Must be one because he is was not enrolled to this exam
                    self.assertEqual(data['new_enrolls'], 1)
                # The student should be enrolled to all exams now
                sub_count = (
                    (StudentSubscription.get_query()
                     .filter(StudentSubscription.student_id == student.id)
                     .count()))
                self.assertEqual(sub_count, len(exams_ids))
            # All students should be enrolled to all exams
            sub_count_after = StudentSubscription.get_query().count()
            self.assertEqual(len(students) * len(exams_ids), sub_count_after)
        finally:
            # Restore the database to its initial state
            deletion_list = []
            for student_id, exams_ids in students_not_enrolled.items():
                for exam_id in exams_ids:
                    deletion_list.append(
                        (StudentSubscription.get_query()
                         .filter(StudentSubscription.student_id == student_id)
                         .filter(StudentSubscription.exam_id == exam_id)
                         .first()))
            Exam.persist_changes({'delete': deletion_list})
            sub_count_after = StudentSubscription.get_query().count()
            self.assertEqual(sub_count_after, sub_count_before)


