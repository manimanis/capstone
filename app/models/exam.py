import json
from datetime import datetime, timedelta

from . import StudentSubscription, Teacher
from .. import db
from .databasemethods import DatabaseMethods


class Exam(db.Model, DatabaseMethods):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('teachers.id'),
                          nullable=False)
    title = db.Column(db.String(), nullable=False)
    exam_hash = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(), nullable=False)
    exercises = db.Column(db.String(), nullable=False, default='')
    shuffle_exercises = db.Column(db.Boolean, nullable=False, default=False)
    exam_duration = db.Column(db.Integer, nullable=False, default=3600)
    max_retries = db.Column(db.Integer, nullable=False,
                            default=2147483647)  # infinite
    dt_creation = db.Column(db.DateTime, nullable=False,
                            default=db.func.current_timestamp())
    from_date = db.Column(db.DateTime, nullable=False,
                          default=db.func.current_timestamp())
    to_date = db.Column(db.DateTime, nullable=False,
                        default=db.func.current_timestamp())
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    dt_archive = db.Column(db.DateTime, nullable=True)
    # required fields for insert
    required_fields = ['author_id', 'title', 'description', 'exercises']
    # optional fields for insert
    optional_fields = ['exam_hash', 'shuffle_exercises', 'max_retries',
                       'from_date', 'to_date', 'exam_duration']
    # updateable fields
    updateable_fields = ['title', 'description', 'exercises', 'exam_duration',
                         'shuffle_exercises', 'max_retries', 'from_date',
                         'to_date']
    # exclude fields
    exclude_fields = ['is_archived', 'dt_archive']
    # text fields for text search
    text_fields = ['title', 'description', 'exercises']

    students = db.relationship('Student',
                               secondary='subscriptions',
                               foreign_keys=[StudentSubscription.exam_id,
                                             StudentSubscription.student_id],
                               backref='exam')

    @classmethod
    def create_sample(cls, teacher):
        """Create a sample empty Exam for the teacher"""
        return cls(teacher=teacher, title="Sample Exam",
                   description="This is a sample exam that you can customize "
                               "as you want",
                   exercises="[]", from_date=datetime.now(),
                   to_date=datetime.now() + timedelta(days=90))

    def prepare_update(self, data_dict):
        if 'exercises' in data_dict and type(data_dict['exercises']) == list:
            data_dict['exercises'] = json.dumps(data_dict['exercises'])
        super().prepare_update(data_dict)

    @classmethod
    def get_by_student_id(cls, student_id):
        """Return the list of exams by student_id"""
        return (cls.query
                .join(StudentSubscription)
                .filter(StudentSubscription.student_id == student_id))

    @classmethod
    def text_search_by_student_id(cls, search, student_id):
        """Make a text search by student_id"""
        return (Exam
                .text_search(search)
                .join(StudentSubscription)
                .filter(StudentSubscription.student_id == student_id,
                        db.func.not_(StudentSubscription.is_archived)))

    @classmethod
    def to_dict(cls, obj, exclude_fields=None, include_fields=None):
        exam = super().to_dict(obj,
                               exclude_fields=exclude_fields,
                               include_fields=include_fields)
        if 'exercises' in exam:
            exam['exercises'] = json.loads(exam['exercises'])
        if 'teacher' in exam:
            exam['teacher'] = Teacher.to_dict(
                exam['teacher'],
                exclude_fields=['dt_creation', 'username', 'user_type'])
        return exam

    @classmethod
    def to_list_of_dict(cls, data_list, include_fields=None,
                        exclude_fields=None):
        enrolled_count = {}
        exams_ids = [exam.id for exam in data_list]
        if include_fields is not None and 'enrolled_count' in include_fields:
            enrolled_count = {
                key: value
                for key, value in (StudentSubscription
                                   .enrolled_count_by_exams_ids(exams_ids)
                                   .all())}
        exams = super().to_list_of_dict(data_list,
                                        exclude_fields, include_fields)
        if include_fields is not None and 'teacher' in include_fields:
            fields = ['id', 'fullname', 'picture']
            for exam in exams:
                exam['teacher'] = {field: exam['teacher'][field]
                                   for field in fields
                                   if field in exam['teacher']}
        if enrolled_count:
            for exam in exams:
                exam['enrolled_count'] = (enrolled_count[exam['id']]
                                          if exam['id'] in enrolled_count
                                          else 0)
        return exams

    def stripped_exercises(self):
        """Return a dictionary of the exercises answers being stripped."""
        if type(self.exercises) == str:
            exercise_dict = json.loads(self.exercises)
        else:
            exercise_dict = self.exercises.copy()
        for exercise in exercise_dict:
            for question in exercise['questions']:
                for answer in question['answers']:
                    if 'is_correct' in answer:
                        del answer['is_correct']
        return exercise_dict

    def to_dict_strip_answers(self):
        exam_dict = self.to_dict(self)
        if 'exercises' not in exam_dict:
            return exam_dict
        for exercise in exam_dict['exercises']:
            for question in exercise['questions']:
                for answer in question['answers']:
                    if 'is_correct' in answer:
                        del answer['is_correct']
        return exam_dict

    def __repr__(self):
        return self.to_str()
