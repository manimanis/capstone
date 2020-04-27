from . import StudentSubscription
from .user import User
from .. import db


class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    exams = db.relationship('Exam',
                            secondary='subscriptions',
                            foreign_keys=[StudentSubscription.exam_id,
                                          StudentSubscription.student_id],
                            backref='student')
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    @classmethod
    def check_students_ids(cls, students_ids):
        """Return if the provided students ids are valid"""
        return (Student
                .get_query()
                .filter(Student.id.in_(students_ids))
                .count() != len(students_ids))
