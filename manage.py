import os
import sys

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app

RUN_CONFIG = os.getenv('FLASK_ENV', 'default')
if len(sys.argv) > 1:
    if sys.argv[1] == 'tests':
        RUN_CONFIG = 'testing'
os.environ['config'] = RUN_CONFIG


app = create_app(RUN_CONFIG)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
