# The Eval Project


## Presentation of the Idea

As ***teachers want to evaluate their students skills frequently*** they often 
need tools to do it. Enrolled in a the **Udacity Fullstack Developer Nanodegree** 
I discovered many new features that can use to build a **Multiple Choice Question 
exam** tool.

At first glance, the task seems to be easy and obvious. But, after diving in 
the project I discovered that the project involves more than just coding. 
I have to make strategic choices about data models, endpoints, frontend 
coding, unit tests, etc. And, as I advance in the project I discover new 
things I have not thought of before.

Finally, after working on this project for more than 15 days I decided to 
send my draft work because I will return to duty very soon I am scare not to 
have enough time to work on it as it should.


## Presentation of the project

The project is developed using the **Flask framework** for the backend, and 
**vue.js** for the frontend. 

The folder structure is as below:

```
 |__ .flaskenv                      # Environment variables
 |__ .gitignore
 |__ app
 |  |__ api                         # API endpoints
 |  |__ auth                        # Authentication module
 |  |__ frontend                    # Frontend endpoints
 |  |__ models                      # SQLAlchemy Database modules
 |  |__ static                      # JavaScript/Stylesheets used in frontend
 |  |  |__ bootstrap
 |  |  |__ jquery
 |  |  |__ models
 |  |  |  |__ models.js             # Javascript data models
 |  |  |__ style.css
 |  |  |__ vuejs
 |  |__ templates                   # Frontend HTML files
 |  |  |__ index.html
 |  |  |__ layout.html
 |  |  |__ profile.html
 |  |  |__ select_profile.html
 |  |  |__ student.html             # Student VueJS application
 |  |  |__ teacher.html             # Teacher VueJS application
 |  |__ __init__.py                 # Flask Application factory
 |__ config.py                      # Configuration module
 |__ eval_project.sql               # Postgresql sample data
 |__ exam_sample.json
 |__ migrations                     # Flask migrations
 |__ runapp.py                      # Application shell entry point
 |__ tests                          # Tests modules
```


## Getting started

### Pre-requisites and Local Development 

Developers using this project should already have Python3, pip and PostgresSQL 
12 installed on their local machines.

### Backend

After cloning the project from this repo. `cd [project_base_folder]` to the 
folder containing the project files. Start by creating the database:

For Windows:
```commandline
createdb -U posgtres eval_project
psql -U postgres eval_project < eval_project.sql
```

Create a virtual environment, then activate it:
```commandline
virtualenv venv
venv\Scripts\activate.bat
```

Then install project requirements:
```commandline
pip install -r requirements.txt
```

Then open the `.flaskenv` file to fill the environment vars with your own.

Finally, you can launch the development server using:
```commandline
flask run
```


### Front end

There is no required installation needed for the frontend. Just open the 
browser: `http://127.0.0.1:5000/


## Testing

Unit testing of the endpoints is possible through the cli command:

```commandline
flask tests
```

You can generate test data by adding the flag `--df`:

```commandline
flask tests
```

But, before testing you should create a new database which will be used for 
this purpose:

```commandline
createdb -U posgtres eval_project_test
```


## API Endpoints

All the API endpoints are under Role Based Access Control (RBAC). In our system
we can identify three actors:

- The **admin**: which has all the available permissions \[I have not coded this 
role yet\]
- The **teacher**: who has the following rights: `archive:exams`, `create:exams`, 
`edit:exams`, `enroll:exams`, `list:exams`, `list:students`, `try-resolve:exams`, 
`view-details:exams`, `view-details:students`
- The **student**: who has only this rights: `enroll:exams`, `list:exams`, 
`list:teachers`, `try-resolve:exams`, `view-details:teachers`
 
The most important endpoints are:

### GET /api/v1/exams

**Authorization:** list:exams

Used to get the list authored by the authenticated teacher.

### POST /api/v1/exams

**Authorization:** create:exams

Creates an empty exam skeleton for the authenticated teacher.

### PATCH /api/v1/exams/<exam_id>

**Authorization:** edit:exams

After editing his exam the authenticated teacher will send his modification to 
this endpoint to be saved.

### DELETE /api/v1/exams/<exam_id>

**Authorization:** archive:exams

I have chosen not to delete exams but mark them as archived. This way I can
prevent the recurring problem of foreign keys of a student which is enrolled to
a deleted exam or a teacher authoring a deleted exam. ***Is it the 
easiest solution? No.***

### GET /api/v1/enrolls

**Authorization:** list:exams

Returns the list of exams the authenticated student is enrolled to.

### GET /api/v1/enrolls/<exam_id>

**Authorization:** list:students

Return the list of students enrolled to one exam.

### POST /api/v1/enrolls/<exam_id>

**Authorization:** enroll:exams

- When invoked by teachers: Enrolls student list to an 'exam_id'
- When invoked by students: Enrolls the authenticated student to the 'exam_id'

### DELETE /api/v1/enrolls/<exam_id>

**Authorization:** enroll:exams

- When invoked by teachers: Un-enrolls student list to an 'exam_id'
- When invoked by students: Un-enrolls the student to the 'exam_id'

_If the student access any exam he is enrolled to and submit answers they won't
be deleted. And he is not allowed to pass exams many times be enrolling then
un-enrolling._

### GET  /api/v1/tries/<exam_id>

**Authorization:** try-resolve:exams

Return the listing of students tries for one particular exam.

### POST /api/v1/tries/<exam_id>

**Authorization:** try-resolve:exams

Initiate a new try for the <exam_id>, the user will have the allocated time to 
return the exam answers.

If this endpoint is invoked multiple times, the second and next invocations
will all return the first initiated session information.

To start the exam again the student must wait until the end of the first exam
session and restart again if he is allowed to make many retries.

### PATCH /api/v1/tries/<exam_id>

**Authorization:** try-resolve:exams

The student must call this endpoint each time he/she wants to save his answers.

This endpoint could be invoked for two reasons:

1. Save the student answers
2. End the exam session for the student


## Future versions

Future versions of the API will include many new features including **Admin 
dashboard panel**.

## Author

Mohamed Anis MANI

## Acknowledgements 

The awesome team at Udacity and all of the students, soon to be full stack extraordinaires! 

  
