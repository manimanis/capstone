from datetime import datetime


from . import DatabaseMethods
from .. import db


class StudentSubscription(db.Model, DatabaseMethods):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'),
                           nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    dt_subscription = db.Column(db.DateTime, nullable=False,
                                default=db.func.current_timestamp())
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    dt_archive = db.Column(db.DateTime, nullable=True)

    # required fields for insert
    required_fields = ['student_id', 'exam_id']
    # optional fields for insert
    optional_fields = []
    # updateable fields
    updateable_fields = []
    # exclude fields
    excluse_fields = ['is_archived', 'dt_archive']

    @staticmethod
    def enrolled_count_by_exams_ids(exams_ids):
        from . import Exam
        from . import Student
        
        """Return a pair of values (exam_id, count(student_id)"""
        return (db.session
                .query(StudentSubscription.exam_id,
                       db.func.count(
                           StudentSubscription.student_id))
                .join(Exam)
                .join(Student)
                .group_by(StudentSubscription.exam_id)
                .filter(db.func.not_(Student.is_archived),
                        db.func.not_(Exam.is_archived),
                        db.func.not_(StudentSubscription.is_archived),
                        StudentSubscription.exam_id.in_(exams_ids)))

    @staticmethod
    def enrolled_by_exam_id(exam_id):
        return (StudentSubscription.get_query()
                .filter(StudentSubscription.exam_id == exam_id))

    @staticmethod
    def enrolled_in_students_ids(exam_id, students_id):
        """Return if the all the 'students_ids' are enrolled to 'exam_id'"""
        return (StudentSubscription
                .enrolled_by_exam_id(exam_id)
                .filter(StudentSubscription.student_id.in_(students_id)))

    @staticmethod
    def enrolled_count_in_students_ids(exam_id, students_id):
        return (StudentSubscription
                .enrolled_in_students_ids(exam_id, students_id).count())

    @staticmethod
    def enroll_students(exam_id, students_ids):
        """Enroll a list of 'students_ids' to an 'exam_id' and return True
        if the operation succeeds"""
        # fetch who is already enrolled to the course
        enrolls = (StudentSubscription
                   .enrolled_in_students_ids(exam_id, students_ids).all())
        old_enrolls = {enroll.student_id: enroll for enroll in enrolls}
        # construct a list of new enrolled students
        new_enrolls = [StudentSubscription(student_id=student_id,
                                           exam_id=exam_id)
                       for student_id in students_ids
                       if student_id not in old_enrolls]
        if len(new_enrolls) > 0:
            return StudentSubscription.persist_changes({'insert': new_enrolls})
        return True

    @staticmethod
    def un_enroll_students(exam_id, students_ids):
        """Enroll a list of 'students_ids' to an 'exam_id' and return True
        if the operation succeeds"""
        # fetch who is already enrolled to the course
        enrolls = (StudentSubscription
                   .enrolled_in_students_ids(exam_id, students_ids).all())
        if len(enrolls) > 0:
            for enroll in enrolls:
                enroll.is_archived = True
                enroll.dt_archive = datetime.now()
            return StudentSubscription.persist_changes({'update': enrolls})
        return True

    def __repr__(self):
        return self.to_str()
