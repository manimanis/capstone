from sqlalchemy.orm import backref

from .user import User
from .. import db


class Teacher(User):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # relationship
    exams = db.relationship('Exam', backref='teacher')
    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }
