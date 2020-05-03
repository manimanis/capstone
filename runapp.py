import os
import sys

import click
from flask_script import Manager

from app import create_app, db, auth0
from app.models import Teacher, Student, User, DatabaseMethods, Exam, \
    StudentSubscription, StudentTry
from flask_migrate import Migrate, MigrateCommand

from tests.fixture import create_fixture_users, create_fixture

RUN_CONFIG = os.getenv('FLASK_ENV', 'default')
if len(sys.argv) > 1:
    if sys.argv[1] == 'tests':
        RUN_CONFIG = 'testing'
os.environ['config'] = RUN_CONFIG

app = create_app(RUN_CONFIG)
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
        'Exam': Exam,
        'StudentTry': StudentTry
    }


@app.cli.command()
@click.option('--df/--ndf', 'db_fixture',
              help='Generate test data fixtures.', default=False)
@click.option('--tests/--no-tests', 'perform_tests', default=True,
              help='Perform tests')
def tests(db_fixture, perform_tests):
    """Run the unit tests."""
    if not db_fixture and not perform_tests:
        print('Nothing to do!')
    if db_fixture:
        create_fixture()

    if perform_tests:
        import unittest
        unittests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(unittests)


manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

