import json
import os
import unittest
from datetime import datetime
from time import sleep

from app import db, create_app
from app.auth import verify_decode_jwt, generate_user_token
from app.models import User
from tests import generate_random_users, generate_token_by_role, load_tokens, \
    verify_token_exp


print(generate_user_token())

class UserTestCase(unittest.TestCase):
    app = None
    app_context = None
    client = None
    tokens_dict = None
    users = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()
        # cls.insert_sample_data()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        # db.drop_all()
        cls.app_context.pop()

    # def setUp(self):
    #     self.app = create_app('testing')
    #     self.app_context = self.app.app_context()
    #     self.app_context.push()
    #     db.create_all()
    #     UserTestCase.insert_sample_data()
    #     self.client = self.app.test_client()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     # db.drop_all()
    #     self.app_context.pop()

    @classmethod
    def insert_sample_data(cls):
        cls.tokens_dict = load_tokens()
        token_ok = cls.verify_tokens()
        print('Verifying tokens...', 'not valid' if not token_ok else 'valid')
        cls.users = None
        if token_ok:
            print('Verifying token and their corresponding user names...')
            cls.users = (User.query
                         .filter(User.username.in_(cls.tokens_dict.keys()))
                         .all())
            print('Must be', len(cls.tokens_dict), 'users:',
                  len(cls.tokens_dict), 'found...')
            if len(cls.users) != len(cls.tokens_dict):
                token_ok = False
        if not token_ok:
            if cls.users is None:
                cls.users = User.query.all()
            print('Deleting all old users...')
            for user in cls.users:
                user.delete()
            print('Creating new users...')
            cls.users = generate_random_users(1, 'teacher') + \
                        generate_random_users(1, 'student')
            cls.tokens_dict = {}
            print('Generating token for the new users')
            try:
                for user in cls.users:
                    # 1. Insert the user
                    user.insert()
                    # 2. request a token using his role
                    token = generate_token_by_role(user.user_type)
                    # 3. Decode the token to extract the payload
                    payload = verify_decode_jwt(token['access_token'])
                    # 4. Update local db user
                    cls.tokens_dict[payload['sub']] = token['access_token']
                    user.username = payload['sub']
                    user.update()
                    # 5. Wait before requesting another token to avoid spam
                    sleep(1.0)
                print(len(cls.tokens_dict), 'users created...')
            except Exception as error:
                print('Could not create users', error)

            print('Dumping users tokens...')
            with open(cls.tokens_file, 'w') as f:
                json.dump(cls.tokens_dict, f)

    @classmethod
    def verify_tokens(cls):
        if cls.tokens_dict is None or len(cls.tokens_dict) != 2:
            return False
        return all(verify_token_exp(token)
                   for token in cls.tokens_dict.values())

    def test_first(self):
        pass
