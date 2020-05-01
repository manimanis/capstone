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

Then install project requirements:

```commandline
pip install requirements.txt
```

Then open the `.flaskenv` file to fill the environment vars with your own.


