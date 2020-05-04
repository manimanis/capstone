from datetime import datetime, timedelta

from app import db
from app.models import DatabaseMethods


class StudentTry(db.Model, DatabaseMethods):
    __tablename__ = 'students_tries'
    id = db.Column(db.Integer, primary_key=True)
    # As the exams, the teacher and the student data can be deleted
    # we duplicate them in this entity this is why there is no foreign keys

    # student data
    student_id = db.Column(db.Integer, nullable=False)
    student_username = db.Column(db.String(128), nullable=False)
    student_fullname = db.Column(db.String(128), nullable=False)
    student_picture = db.Column(db.String(), nullable=True)

    # teacher data
    teacher_id = db.Column(db.Integer, nullable=False)
    teacher_username = db.Column(db.String(128), nullable=False)
    teacher_fullname = db.Column(db.String(128), nullable=False)
    teacher_picture = db.Column(db.String(), nullable=True)

    # exam data
    exam_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=False)
    exam_hash = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(), nullable=False)
    exercises = db.Column(db.String(), nullable=False, default='')
    exam_duration = db.Column(db.Integer, nullable=False, default=3600)

    # student try
    # - dt_try: The student begin the exam at this datetime
    # - dt_expiration: The exam will expire at this point of datetime
    # - current_state: 0 for started, 1 for completed, 2 for expired, 3 save
    # - answers: The student answers
    # - student_score/total_score: A measure of achievement of the student
    STARTED, COMPLETED, EXPIRED, SAVE = range(4)
    dt_try = db.Column(db.DateTime, nullable=False,
                       default=db.func.current_timestamp())
    dt_expiration = db.Column(db.DateTime, nullable=False,
                              default=db.func.current_timestamp())
    current_state = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.String(), nullable=True)
    total_score = db.Column(db.Integer(), nullable=True, default=0)
    student_score = db.Column(db.Integer(), nullable=True, default=0)

    # required fields for insert
    required_fields = ['answers', 'current_state', 'description',
                       'dt_expiration', 'dt_try', 'exam_duration', 'exam_hash',
                       'exercises', 'exam_id',
                       'student_id', 'student_fullname', 'student_picture',
                       'teacher_id', 'student_username', 'teacher_fullname',
                       'teacher_picture', 'teacher_username', 'title',
                       'total_score']
    # optional fields for insert
    optional_fields = []
    # updateable fields
    updateable_fields = ['answers']
    # exclude fields
    exclude_fields = []
    # text fields for text search
    text_fields = ['answers', 'description', 'exercises',
                   'student_fullname', 'student_picture', 'student_username',
                   'teacher_fullname', 'teacher_picture', 'teacher_username',
                   'title']

    def fill_student_info(self, student):
        """Fill by the student data"""
        self.student_id = student.id
        self.student_username = student.username
        self.student_fullname = student.fullname
        self.student_picture = student.picture

    def fill_teacher_info(self, teacher):
        """Fill by the teacher data"""
        self.teacher_id = teacher.id
        self.teacher_username = teacher.username
        self.teacher_fullname = teacher.fullname
        self.teacher_picture = teacher.picture

    def fill_exam_info(self, exam):
        """Fill by the exam data"""
        self.exam_id = exam.id
        self.title = exam.title
        self.description = exam.description
        self.exam_hash = exam.exam_hash
        self.exercises = exam.exercises
        self.exam_duration = exam.exam_duration

    def create_new_try(self, student, teacher, exam):
        """Create a new try given the passed arguments"""
        self.fill_student_info(student)
        self.fill_teacher_info(teacher)
        self.fill_exam_info(exam)
        self.dt_try = datetime.now()
        self.dt_expiration = self.dt_try + timedelta(
            seconds=exam.exam_duration)
        self.current_state = self.STARTED
        self.answers = '[]'
        self.total_score = 0
        self.student_score = 0

    @staticmethod
    def num_tries_by_exams_ids(exams_ids, student_id):
        return (db.session
                .query(StudentTry.exam_id,
                       StudentTry.student_id,
                       db.func.count(StudentTry.student_id))
                .group_by(StudentTry.exam_id, StudentTry.student_id)
                .filter(StudentTry.exam_id.in_(exams_ids),
                        StudentTry.student_id == student_id))
