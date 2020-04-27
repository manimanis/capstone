import os
from app import create_app, db, auth0
from app.models import Teacher, Student, User, DatabaseMethods, Exam, \
    StudentSubscription
from flask_migrate import Migrate


app = create_app(os.getenv('FLASK_ENV', 'default'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'auth0': auth0,
        'Teacher': Teacher,
        'Student': Student,
        'User': User,
        'StudentSubscription': StudentSubscription,
        'DatabaseMethods': DatabaseMethods,
        'Exam': Exam
    }


@app.cli.command()
def tests():
    """Run the unit tests."""
    import unittest
    os.environ['config'] = 'TESTING'
    unittests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(unittests)



