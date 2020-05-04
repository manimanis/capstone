import os
import unittest
from datetime import datetime, timedelta

from flask import session

from app import create_app, db
from app.auth import generate_user_token, TEACHER_PERMISSIONS, \
    STUDENT_PERMISSIONS
from app.models import Teacher, Exam, Student
from tests.sample_exams import generate_random_exam


class ExamTestCase(unittest.TestCase):
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

    def check_exam_list_fields(self, data):
        """Check the json response dictionary fields for list exams fields"""
        fields = ['success', 'exams_count', 'search_count',
                  'start', 'end', 'exams']
        self.check_fields_list(data, fields)

    def test_get_exams_list_teacher(self):
        """Teacher fetching their exams"""
        # Test as teacher
        teacher = Teacher.query.first()
        exams_count = Exam.query.filter(Exam.author_id == teacher.id).count()
        # Generate a header for a teacher
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        res = self.client.get('/api/v1/exams',
                              headers={'Content-Type': 'application/json',
                                       'Authorization': f'bearer {token}'})
        self.assertEqual(res.status_code, 200, res.get_json())
        data = res.get_json()
        self.check_exam_list_fields(data)
        self.assertTrue(data['success'])
        self.assertEqual(data['end'] - data['start'], len(data['exams']))
        self.assertEqual(data['exams_count'], exams_count)

    def test_get_exams_list_student(self):
        """Student trying to retrieve list of exams"""
        # Test as student
        student = Student.query.first()
        for permissions in [STUDENT_PERMISSIONS, TEACHER_PERMISSIONS]:
            # Generate a header for the student
            token = generate_user_token(student.username, permissions)
            res = self.client.get('/api/v1/exams',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': f'bearer {token}'})
            # A registered student could not access exams lists
            self.assertEqual(res.status_code, 403, res.get_json())

    def test_create_exam_teacher(self):
        """Teacher creating a new exam"""
        # Test as teacher
        teacher = Teacher.query.order_by(Teacher.id.desc()).first()
        # Generate a header for a teacher
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        res = self.client.post('/api/v1/exams',
                               headers={'Content-Type': 'application/json',
                                        'Authorization': f'bearer {token}'})
        self.assertEqual(res.status_code, 200, res.get_json())
        data = res.get_json()
        self.check_fields_list(data, ['success', 'exam'])
        self.assertTrue('success')

    def test_create_exam_student(self):
        """Student trying to create an exam"""
        # Test as student
        student = Student.query.order_by(Student.id.desc()).first()
        for permissions in [STUDENT_PERMISSIONS, TEACHER_PERMISSIONS]:
            # Generate a header for the student
            token = generate_user_token(student.username, permissions)
            res = self.client.post('/api/v1/exams',
                                   headers={
                                       'Content-Type': 'application/json',
                                       'Authorization': f'bearer {token}'})
            # A registered student could not access exams lists
            self.assertEqual(res.status_code, 403, res.get_json())

    def test_edit_exam_teacher(self):
        """Teacher edit their exam properly"""
        exam = Exam.query.first()
        teacher = Teacher.get_by_id(exam.author_id)
        # Generate a header for a teacher
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        from_date = datetime.now().replace(microsecond=0)
        exam_body = {
            'title': '',
            'description': '',
            'exercises': '[]',
            'exam_duration': 300,
            'shuffle_exercises': True,
            'max_retries': 1,
            'from_date': from_date,
            'to_date': from_date + timedelta(days=10)
        }
        res = self.client.patch(f'/api/v1/exams/{exam.id}',
                                headers={'Content-Type': 'application/json',
                                         'Authorization': f'bearer {token}'},
                                json=exam_body)
        self.assertEqual(res.status_code, 200, res.get_json())
        data = res.get_json()
        self.check_fields_list(data, ['success', 'updated'])
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], exam.id)

        exam = Exam.get_by_id(exam.id)
        for key, value in exam_body.items():
            self.assertEqual(value, getattr(exam, key), f'{key}: {value}')

    def test_edit_exam_teacher_exam_not_found(self):
        """Cannot modify not founds exams"""
        first_exam = Exam.query.order_by(Exam.id).first()
        last_exam = Exam.query.order_by(Exam.id.desc()).first()
        exams_ids = (first_exam.id - 1, last_exam.id + 1)
        teacher = Teacher.get_by_id(first_exam.author_id)
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        exam_body = {}  # Not needed
        for exam_id in exams_ids:
            res = self.client.patch(f'/api/v1/exams/{exam_id}',
                                    headers={
                                        'Content-Type': 'application/json',
                                        'Authorization': f'bearer {token}'},
                                    json=exam_body)
            self.assertEqual(res.status_code, 404, res.get_json())

    def test_edit_exam_teacher_others_exams(self):
        """Teachers cannot modify others teachers exams"""
        teacher1 = Teacher.query.order_by(Teacher.id).first()
        teacher2 = Teacher.query.order_by(Teacher.id.desc()).first()
        exam1 = Exam.query.filter(Exam.author_id == teacher1.id).first()
        exam2 = Exam.query.filter(Exam.author_id == teacher2.id).first()
        token1 = generate_user_token(teacher1.username, TEACHER_PERMISSIONS)
        token2 = generate_user_token(teacher2.username, TEACHER_PERMISSIONS)
        test_set = [(teacher1, token1, exam2), (teacher2, token2, exam1)]
        for teacher, token, exam in test_set:
            res = self.client.patch(f'/api/v1/exams/{exam.id}',
                                    headers={
                                        'Content-Type': 'application/json',
                                        'Authorization': f'bearer {token}'},
                                    json={})
            self.assertEqual(res.status_code, 403, res.get_json())

    def test_edit_exam_teacher_important_fields(self):
        """Teacher trying to edit an exam without sending appropriate data"""
        # trying to update non updateable fields
        data = {
            'id': 36,
            'author_id': 2,
            'dt_creation': datetime.now().replace(microsecond=0),
            'is_archived': True,
            'dt_archive': datetime.now().replace(microsecond=0),
        }
        exam = Exam.query.first()
        teacher = Teacher.get_by_id(exam.author_id)
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        data_list = [{}, data] + [{key: value} for key, value in data.items()]
        for data in data_list:
            res = self.client.patch(f'/api/v1/exams/{exam.id}',
                                    headers={
                                        'Content-Type': 'application/json',
                                        'Authorization': f'bearer {token}'},
                                    json=data)
            self.assertEqual(res.status_code, 400, res.get_json())

    def test_delete_exam_teacher(self):
        """Teacher archiving their exam"""
        exam = Exam.query.first()
        new_exam_dict = generate_random_exam(exam.author_id)
        new_exam = Exam(**new_exam_dict)
        new_exam.insert()
        try:
            teacher = Teacher.get_by_id(new_exam.author_id)
            token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
            res = self.client.delete(f'/api/v1/exams/{new_exam.id}',
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 200, res.get_json())
            data = res.get_json()
            self.check_fields_list(data, ['success', 'deleted'])
            self.assertTrue('success')
            self.assertEqual(data['deleted'], new_exam.id)
            self.assertIsNone(Exam.get_by_id(new_exam.id))
        finally:
            new_exam.delete()

    def test_delete_exam_teacher_inexistant(self):
        """Teacher archiving inexistant exam"""
        teacher = Teacher.query.order_by(Teacher.id.desc()).first()
        exam1 = Exam.query.order_by(Exam.id).first()
        exam2 = Exam.query.order_by(Exam.id.desc()).first()
        exams_ids = [exam1.id - 1, exam2.id + 1]
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        for exam_id in exams_ids:
            res = self.client.delete(f'/api/v1/exams/{exam_id}',
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 404, res.get_json())

    def test_delete_exam_teacher_others_exams(self):
        """Teacher trying to archive others teachers exam"""
        teacher = Teacher.query.order_by(Teacher.id.desc()).first()
        token = generate_user_token(teacher.username, TEACHER_PERMISSIONS)
        exams_ids = [exam.id
                     for exam in Exam.get_query().all()
                     if exam.author_id != teacher.id][:10]
        for exam_id in exams_ids:
            res = self.client.delete(f'/api/v1/exams/{exam_id}',
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': f'bearer {token}'})
            self.assertEqual(res.status_code, 403, res.get_json())
