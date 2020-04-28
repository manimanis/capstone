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
    # - current_state: 0 for started, 1 for completed, 2 for expired
    # - answers: The student answers
    # - student_score/total_score: A measure of achievement of the student
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
