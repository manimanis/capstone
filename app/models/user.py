import random

from .. import db
from .databasemethods import DatabaseMethods

PICTURE_HOST = 'https://randomuser.me/api/portraits/lego/'


class User(db.Model, DatabaseMethods):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(32), nullable=False)
    picture = db.Column(db.String(), nullable=True,
                        default=f'{PICTURE_HOST}{random.randint(0, 8)}.jpg')
    dt_creation = db.Column(db.DateTime, nullable=False,
                            default=db.func.current_timestamp())
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    dt_archive = db.Column(db.DateTime, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }
    # required fields for insert
    required_fields = ['username', 'fullname']
    # optional fields for insert
    optional_fields = []
    # updateable fields
    updateable_fields = ['fullname']
    # exclude fields
    exclude_fields = ['user_type', 'is_archived', 'dt_archive']
    # text fields for text search
    text_fields = ['username', 'fullname']

    def __repr__(self):
        return self.to_str()

    def is_teacher(self):
        return self.user_type == 'teacher'

    def is_student(self):
        return self.user_type == 'student'

    @classmethod
    def get_by_username(cls, username):
        return (User.get_query()
                .filter(db.func.lower(User.username) == username.lower())
                .first())
