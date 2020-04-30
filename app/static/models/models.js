/**
 *
 * @param exam
 * author_id: 17
 description: "This is a sample exam that you can customize as you want"
 dt_creation: "Mon, 20 Apr 2020 21:00:45 GMT"
 exam_duration: 3600
 exam_hash: null
 exercises: "[]"
 from_date: "Mon, 20 Apr 2020 20:00:45 GMT"
 id: 3
 max_retries: 2147483647
 shuffle_exercises: false
 title: "Sample Exam"
 to_date: "Sun, 19 Jul 2020 20:00:45 GMT"
 * @constructor
 */
function Exam(exam) {
    this.setExam(exam);
}

Exam.prototype.setExam = function (exam) {
    this.author_id = exam.author_id;
    this.description = exam.description;
    this.dt_creation = new Date(exam.dt_creation).toISOString().substring(0, 10);
    this.exam_duration = exam.exam_duration;
    this.exam_hash = exam.exam_hash;
    if (typeof exam.exercises !== 'string') {
        exam.exercises = JSON.stringify(exam.exercises);
    }
    this.exercises = ((exam.exercises && JSON.parse(exam.exercises)) || []).map(exercise => new Exercise(exercise));
    this.from_date = new Date(exam.from_date).toISOString().substring(0, 10);
    this.id = exam.id;
    this.max_retries = exam.max_retries;
    this.shuffle_exercises = !!exam.shuffle_exercises;
    this.title = exam.title;
    this.to_date = new Date(exam.to_date).toISOString().substring(0, 10);
    if (exam.enrolled_count !== undefined) {
        this.enrolled_count = exam.enrolled_count ? +exam.enrolled_count : 0;
    }
    if (exam.num_tries !== undefined) {
        this.num_tries = exam.num_tries ? +exam.num_tries : 0;
        const available_time = (new Date(this.to_date).getTime() - Math.max(new Date(this.from_date).getTime(), new Date().getTime())) / 1000;
        const available_retries = Math.ceil(available_time / this.exam_duration);
        this.max_retries = Math.min(this.max_retries, available_retries);
    }
    if (exam.teacher !== undefined) {
        this.teacher = exam.teacher;
    }
};

Exam.prototype.createExercise = function () {
    const exercise = new Exercise({});
    exercise.questions.push(exercise.createQuestion());
    return exercise;
};

Exam.prototype.isAvailable = function () {
    return new Date().toISOString().substring(0, 10) <= this.to_date;
};

Exam.prototype.numTriesMessage = function () {
    if (this.num_tries === this.max_retries) {
        return 'You have consumed all of your retries.';
    }
    if (this.num_tries > 0 && this.num_tries + 1 === this.max_retries) {
        return 'You have only one another chance.';
    }
    if (this.num_tries === 0 && this.max_retries === 1) {
        return 'Be careful! You are not allowed to retry this exam';
    }
    if (this.max_retries - this.num_tries <= 3) {
        return `You are lucky there are ${this.max_retries - this.num_tries} available chance.`;
    }
    return `You consumed ${this.num_tries} out of ${this.max_retries}`;
};

Exam.prototype.canRetry = function () {
    return this.max_retries > this.num_tries;
};

function Exercise(exercise) {
    this.title = exercise.title || 'Exercise title';
    this.description = exercise.description || 'The exercise description';
    this.shuffle_questions = !!exercise.shuffle_questions;
    this.questions = (exercise.questions || []).map(question => this.createQuestion(question));
}

Exercise.prototype.createQuestion = function (question = null) {
    if (!question) {
        return new QcmQuestion({
            answers: [
                {
                    answer: 'Proposition 1',
                    is_correct: false
                },
                {
                    answer: 'Proposition 2',
                    is_correct: true
                },
                {
                    answer: 'Proposition 3',
                    is_correct: false
                }
            ]
        });
    }
    if (question.question_type == 'QcmQuestion') {
        return new QcmQuestion(question);
    }
};

function Question(question) {
    if (!question) {
        question = {};
    }
    this.title = question.title || 'Question title';
    this.description = question.description || 'Question default description';
}

function QcmQuestion(qcm_question) {
    Question.call(this, qcm_question);

    this.question_type = 'QcmQuestion';
    this.multiple_answers = !!qcm_question.multiple_answers;
    this.answers = (qcm_question.answers || []).map(answer => new QcmAnswer(answer));
    this.shuffle_answers = !!qcm_question.shuffle_answers;
}

QcmQuestion.prototype = new Question();
QcmQuestion.prototype.constructor = QcmQuestion;
Object.defineProperty(QcmQuestion.prototype, 'correct_answer', {
    get: function () {
        let cAnswer = this.answers
            .map((answer, index) => answer.is_correct ? 'answer' + index : null)
            .filter(answer => answer !== null);
        if (!this.multiple_answers) {
            if (cAnswer.length > 0) {
                return cAnswer[0];
            }
        } else {
            return cAnswer;
        }
    },
    set: function (answers) {
        this.answers.forEach((answer, index) => answer.is_correct = answers.includes('answer' + index));
    }
});
Object.defineProperty(QcmQuestion.prototype, '_multiple_answers', {
    get: function () {
        return this.multiple_answers;
    },
    set: function (multiple_answers) {
        this.multiple_answers = multiple_answers;
        const cAnswers = this.answers
            .map((answer, index) => answer.is_correct ? index : null)
            .filter((index) => index !== null);
        if (!this.multiple_answers && cAnswers.length > 1) {
            this.answers.forEach((answer, index) => answer.is_correct = index == cAnswers[0]);
        }
    }
});


function QcmAnswer(answer) {
    this.answer = answer.answer || 'This is an answer';
    this.is_correct = !!answer.is_correct;
    this.mark = this.mark || 1;
}

/*
    "description": "This is the second part of the MCQ Exam.",
    "dt_expiration": "Wed, 29 Apr 2020 10:53:45 GMT",
    "dt_try": "Wed, 29 Apr 2020 09:53:45 GMT",
    "exam_duration": 3600
    "exam_id": 2,
    "id": 4,
    "student_id": 4,
    "teacher_id": 3,
    "title": "HTML MCS - Part 2",
    "total_score": 0
 */
function ExamTry(exam, student_try) {
    this.id = student_try.id;
    this.exam_id = student_try.exam_id;
    this.student_id = student_try.student_id;
    this.teacher_id = student_try.teacher_id;
    this.title = student_try.title;
    this.description = student_try.description.split('\n');
    student_try.dt_try = student_try.dt_try.substr(0, student_try.dt_try.indexOf('GMT'));
    student_try.dt_expiration = student_try.dt_expiration.substr(0, student_try.dt_expiration.indexOf('GMT'));
    this.start_time = Math.floor(new Date(student_try.dt_try).getTime() / 1000);
    this.end_time = Math.floor(new Date(student_try.dt_expiration).getTime() / 1000);
    this.display_time = '';
    this.exam = exam;
    for (let exercise of this.exam) {
        exercise.description = exercise.description.split('\n');
        for (let question of exercise.questions) {
            question.description = question.description.split('\n');
        }
    }
    this.totalQuestionsCount = this.getTotalQuestionsCount();
    this.questionIndex = 0;
    if (!Array.isArray(student_try.answers) || student_try.answers.length !== this.totalQuestionsCount) {
        student_try.answers = new Array(this.totalQuestionsCount).fill([]);
    }
    this.answers = student_try.answers;
    this.setQuestionByIndex(this.questionIndex);
    this.exercisesCount = this.exam.length;
}

ExamTry.prototype.elapsedTime = function (time) {
    return Math.floor(time.getTime() / 1000) - this.start_time;
};

ExamTry.prototype.remainingTime = function (time) {
    return this.end_time - Math.floor(time.getTime() / 1000);
};

ExamTry.prototype.isTimedOut = function (time) {
    return this.remainingTime(time) <= 0;
};

ExamTry.prototype.start = function () {
    const time = new Date();
    const remainingTime = this.remainingTime(time);
    this.display_time = this.durationToString(remainingTime);
    if (remainingTime > 0) {
        setTimeout(() => {
            this.start()
        }, Math.min(remainingTime*1000, 5000));
    }
};

ExamTry.prototype.durationToString = function (duration) {
    if (duration <= 0) {
      return 'Timed out';
    } else if (duration < 60) {
        return 'Less than one minute'
    } else if (duration < 120) {
        return 'Above one minute';
    }
    const m = Math.floor((duration % 3600) / 60);
    const h = Math.floor(duration / 3600);
    let res = '';
    if (h > 0) {
        res += (res !== '') ? ' ' : '';
        res += `${h}hour${h != 1 ? 's' : ''}`;
    }
    if (m > 0) {
        res += (res !== '') ? ' ' : '';
        res += `${m}minute${m != 1 ? 's' : ''}`;
    }
    return res;
};

ExamTry.prototype.getTotalQuestionsCount = function () {
    let tqc = 0;
    for (let exercise of this.exam) {
        tqc += exercise.questions.length;
    }
    return tqc;
};

ExamTry.prototype.setQuestionByIndex = function (index) {
    let cum = 0;
    for (let i = 0; i < this.exam.length; i++) {
        if (cum <= index && index < cum + this.exam[i].questions.length) {
            this.currQuestionIndex = index - cum;
            this.currExerciseIndex = i;
            this.currExercise = this.exam[i];
            this.currQuestion = this.currExercise.questions[this.currQuestionIndex];
        }
    }
};

ExamTry.prototype.nextQuestion = function () {
    if (this.questionIndex + 1 < this.totalQuestionsCount) {
        this.questionIndex++;
        this.setQuestionByIndex(this.questionIndex);
    }
};

ExamTry.prototype.prevQuestion = function () {
    if (this.questionIndex > 0) {
        this.questionIndex--;
        this.setQuestionByIndex(this.questionIndex);
    }
};

