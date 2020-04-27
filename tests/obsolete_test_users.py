import unittest
import random

from app import create_app, db
from app.models import User
from tests import generate_names, generate_usernames

INSERT_COUNT = 20
INEXISTANT_COUNT = 23
NEW_INSERT_COUNT = 26
TOTAL_NAMES = 30

random_names = generate_names(TOTAL_NAMES)
usernames = generate_usernames(random_names)


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        UserTestCase.insert_sample_data()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def insert_sample_data():
        # Add only 20 names the others will be used for test purpose
        for name, username in zip(random_names[:INSERT_COUNT],
                                  usernames[:INSERT_COUNT]):
            user = User(username=username, fullname=name)
            user.insert()

    def has_response_keys_single(self, data):
        """The server response for a single user request should include all
        of this fields"""
        keys = ['success', 'user']
        for key in keys:
            self.assertIn(key, data)

        self.has_all_fields(data['user'])

    def has_response_keys(self, data):
        """The server response should include all of this fields"""
        keys = ['success', 'users_count', 'search_count', 'start', 'end',
                'users']
        for key in keys:
            self.assertIn(key, data)

        for user in data['users']:
            self.has_all_fields(user)

    def has_all_fields(self, user):
        """The user dictionaries if they exists should contain all of this
        fields"""
        fields = ['dt_creation', 'fullname', 'id', 'username']
        for field in fields:
            self.assertIn(field, user)

    def test_get_users(self):
        res = self.client.get('/api/v1/users')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.has_response_keys(data)
        self.assertTrue(data['success'])
        self.assertGreater(data['users_count'], 0)
        self.assertEqual(data['users_count'], data['search_count'])
        self.assertEqual(data['start'], 0)
        self.assertGreater(data['end'], 0)
        self.assertEqual(len(data['users']), data['end'] - data['start'])

    def test_get_users_range(self):
        users_count = User.get_query().count()
        start = random.randint(0, users_count // 2 - 1)
        end = random.randint(users_count // 2, users_count - 1)
        res = self.client.get(f'/api/v1/users?start={start}&end={end}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.has_response_keys(data)
        self.assertTrue(data['success'])
        self.assertEqual(data['users_count'], users_count)
        self.assertEqual(data['users_count'], data['search_count'])
        self.assertEqual(data['start'], start)
        self.assertEqual(data['end'], end)
        self.assertEqual(len(data['users']), end - start)

    def test_get_users_search(self):
        user = User.query.first()
        # Search for words we are sure they exist in the Database
        words = user.fullname.split()
        for word in words:
            users_count = (User.query
                              .filter(User.fullname.ilike(f'%{word}%'))
                              .count())
            res = self.client.get(f'/api/v1/users?search={word}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys(data)
            self.assertTrue(data['success'])
            self.assertEqual(data['search_count'], users_count)
            self.assertNotEqual(data['users_count'], data['search_count'])
            self.assertGreater(data['search_count'], 0)

    def test_get_users_search_inexistant(self):
        # Search for names that does not exist
        for name in random_names[INSERT_COUNT:INEXISTANT_COUNT]:
            res = self.client.get(f'/api/v1/users?search={name}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys(data)
            self.assertTrue(data['success'])
            self.assertEqual(data['search_count'], 0)
            self.assertNotEqual(data['users_count'], data['search_count'])

    def test_get_single_user(self):
        # select three random ids
        users = User.query.all()
        ids = [user.id for user in users]
        ids = random.choices(ids, k=3)
        for id in ids:
            res = self.client.get(f'/api/v1/users/{id}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)

    def test_get_single_user_inexistant(self):
        # select two inexistant ids
        first = User.query.order_by(User.id).first().id
        last = User.query.order_by(User.id.desc()).first().id
        for id in [first - 1, last + 1]:
            res = self.client.get(f'/api/v1/users/{id}')
            self.assertEqual(res.status_code, 404)

    def test_insert_user(self):
        old_count = User.query.count()
        for name, username in zip(
                random_names[INEXISTANT_COUNT:NEW_INSERT_COUNT],
                usernames[INEXISTANT_COUNT:NEW_INSERT_COUNT]):
            user_dict = {
                'username': username,
                'fullname': name
            }
            res = self.client.post(f'/api/v1/users', json=user_dict)
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)
            self.assertEqual(data['user']['username'], username)
            self.assertEqual(data['user']['fullname'], name)
        new_count = User.query.count()
        self.assertEqual(new_count - old_count,
                         NEW_INSERT_COUNT - INEXISTANT_COUNT)

    def test_insert_user_invalid(self):
        users_dict = [
            # Both username and full name are used by one person
            {
                'fullname': random_names[0],
                'username': usernames[0]
            },
            # Both username and full name are used by two persons
            {
                'fullname': random_names[0],
                'username': usernames[1]
            },
            # Username is used by one person, fullname is not used
            {
                'fullname': random_names[1],
                'username': usernames[INEXISTANT_COUNT]
            },
            # Username is not used, fullname is used
            {
                'fullname': random_names[INEXISTANT_COUNT],
                'username': usernames[2]
            }
        ]
        for user_dict in users_dict:
            res = self.client.post(f'/api/v1/users', json=user_dict)
            self.assertEqual(res.status_code, 400)
        for key, value in users_dict[0].items():
            res = self.client.post(f'/api/v1/users', json={key: value})
            self.assertEqual(res.status_code, 400)

    def test_update_user(self):
        # select random ids
        users = User.query.all()
        ids = [user.id for user in users]
        ids = random.choices(ids, k=len(random_names)-NEW_INSERT_COUNT)
        for id, fullname in zip(ids, random_names[NEW_INSERT_COUNT:]):
            res = self.client.patch(f'/api/v1/users/{id}',
                                   json={'fullname': fullname})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)
            self.assertEqual(fullname, data['user']['fullname'])

    def test_update_user_invalid(self):
        users = User.query.all()
        for i in range(3):
            res = self.client.patch(f'/api/v1/users/{users[i].id}',
                                   json={'fullname': users[i+1].fullname})
            self.assertEqual(res.status_code, 400)
        # No data
        res = self.client.patch(f'/api/v1/users/{users[0].id}', json={})
        self.assertEqual(res.status_code, 400)
        # Junk invalid data
        res = self.client.patch(f'/api/v1/users/{users[1].id}',
                                json={'junk_data': 'Junk'})
        self.assertEqual(res.status_code, 400)

    def test_delete_user(self):
        # We are using get_query in order to skip archived user
        users_count = User.get_query().count()
        user = User.to_dict(User.query.first())
        res = self.client.delete(f'/api/v1/users/{user["id"]}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        # We are using get_query in order to skip archived user
        new_count = User.get_query().count()
        self.assertEqual(new_count+1, users_count)
        self.assertIn('deleted', data)
        self.assertEqual(data['deleted'], user['id'])

    def test_delete_user_invalid(self):
        first = User.query.order_by(User.id).first().id
        last = User.query.order_by(User.id.desc()).first().id
        for id in [first - 1, last + 1]:
            res = self.client.delete(f'/api/v1/users/{id}')
            self.assertEqual(res.status_code, 404)
