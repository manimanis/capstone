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
    this.suhffle_exercises = !!exam.suhffle_exercises;
    this.title = exam.title;
    this.to_date = new Date(exam.to_date).toISOString().substring(0, 10);
    this.enrolled_count = exam.enrolled_count ? +exam.enrolled_count : 0;
};

Exam.prototype.createExercise = function () {
    const exercise = new Exercise({});
    exercise.questions.push(exercise.createQuestion());
    return exercise;
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
       this.answers.forEach((answer, index) => answer.is_correct = answers.includes('answer'+index));
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