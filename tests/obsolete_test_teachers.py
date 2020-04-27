import unittest
import random

from app import create_app, db
from app.models import Teacher
from tests import generate_names, generate_usernames

INSERT_COUNT = 20
INEXISTANT_COUNT = 23
NEW_INSERT_COUNT = 26
TOTAL_NAMES = 30

random_names = generate_names(TOTAL_NAMES)
usernames = generate_usernames(random_names)


class TeacherTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        TeacherTestCase.insert_sample_data()
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
            teacher = Teacher(username=username, fullname=name)
            teacher.insert()

    def has_response_keys_single(self, data):
        """The server response for a single teacher request should include all
        of this fields"""
        keys = ['success', 'teacher']
        for key in keys:
            self.assertIn(key, data)

        self.has_all_fields(data['teacher'])

    def has_response_keys(self, data):
        """The server response should include all of this fields"""
        keys = ['success', 'teachers_count', 'search_count', 'start', 'end',
                'teachers']
        for key in keys:
            self.assertIn(key, data)

        for teacher in data['teachers']:
            self.has_all_fields(teacher)

    def has_all_fields(self, teacher):
        """The teacher dictionaries if they exists should contain all of this
        fields"""
        fields = ['dt_creation', 'fullname', 'id', 'username']
        for field in fields:
            self.assertIn(field, teacher)

    def test_get_teachers(self):
        res = self.client.get('/api/v1/teachers')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.has_response_keys(data)
        self.assertTrue(data['success'])
        self.assertGreater(data['teachers_count'], 0)
        self.assertEqual(data['teachers_count'], data['search_count'])
        self.assertEqual(data['start'], 0)
        self.assertGreater(data['end'], 0)
        self.assertEqual(len(data['teachers']), data['end'] - data['start'])

    def test_get_teachers_range(self):
        teachers_count = Teacher.get_query().count()
        start = random.randint(0, teachers_count // 2 - 1)
        end = random.randint(teachers_count // 2, teachers_count - 1)
        res = self.client.get(f'/api/v1/teachers?start={start}&end={end}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.has_response_keys(data)
        self.assertTrue(data['success'])
        self.assertEqual(data['teachers_count'], teachers_count)
        self.assertEqual(data['teachers_count'], data['search_count'])
        self.assertEqual(data['start'], start)
        self.assertEqual(data['end'], end)
        self.assertEqual(len(data['teachers']), end - start)

    def test_get_teachers_search(self):
        teacher = Teacher.query.first()
        # Search for words we are sure they exist in the Database
        words = teacher.fullname.split()
        for word in words:
            teachers_count = (Teacher.query
                              .filter(Teacher.fullname.ilike(f'%{word}%'))
                              .count())
            res = self.client.get(f'/api/v1/teachers?search={word}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys(data)
            self.assertTrue(data['success'])
            self.assertEqual(data['search_count'], teachers_count)
            self.assertNotEqual(data['teachers_count'], data['search_count'])
            self.assertGreater(data['search_count'], 0)

    def test_get_teachers_search_inexistant(self):
        # Search for names that does not exist
        for name in random_names[INSERT_COUNT:INEXISTANT_COUNT]:
            res = self.client.get(f'/api/v1/teachers?search={name}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys(data)
            self.assertTrue(data['success'])
            self.assertEqual(data['search_count'], 0)
            self.assertNotEqual(data['teachers_count'], data['search_count'])

    def test_get_single_teacher(self):
        # select three random ids
        teachers = Teacher.query.all()
        ids = [teacher.id for teacher in teachers]
        ids = random.choices(ids, k=3)
        for id in ids:
            res = self.client.get(f'/api/v1/teachers/{id}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)

    def test_get_single_teacher_inexistant(self):
        # select two inexistant ids
        first = Teacher.query.order_by(Teacher.id).first().id
        last = Teacher.query.order_by(Teacher.id.desc()).first().id
        for id in [first - 1, last + 1]:
            res = self.client.get(f'/api/v1/teachers/{id}')
            self.assertEqual(res.status_code, 404)

    def test_insert_teacher(self):
        old_count = Teacher.query.count()
        for name, username in zip(
                random_names[INEXISTANT_COUNT:NEW_INSERT_COUNT],
                usernames[INEXISTANT_COUNT:NEW_INSERT_COUNT]):
            teacher_dict = {
                'username': username,
                'fullname': name
            }
            res = self.client.post(f'/api/v1/teachers', json=teacher_dict)
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)
            self.assertEqual(data['teacher']['username'], username)
            self.assertEqual(data['teacher']['fullname'], name)
        new_count = Teacher.query.count()
        self.assertEqual(new_count - old_count,
                         NEW_INSERT_COUNT - INEXISTANT_COUNT)

    def test_insert_teacher_invalid(self):
        teachers_dict = [
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
        for teacher_dict in teachers_dict:
            res = self.client.post(f'/api/v1/teachers', json=teacher_dict)
            self.assertEqual(res.status_code, 400)
        for key, value in teachers_dict[0].items():
            res = self.client.post(f'/api/v1/teachers', json={key: value})
            self.assertEqual(res.status_code, 400)

    def test_update_teacher(self):
        # select random ids
        teachers = Teacher.query.all()
        ids = [teacher.id for teacher in teachers]
        ids = random.choices(ids, k=len(random_names)-NEW_INSERT_COUNT)
        for id, fullname in zip(ids, random_names[NEW_INSERT_COUNT:]):
            res = self.client.patch(f'/api/v1/teachers/{id}',
                                   json={'fullname': fullname})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)
            self.assertEqual(fullname, data['teacher']['fullname'])

    def test_update_teacher_invalid(self):
        teachers = Teacher.query.all()
        for i in range(3):
            res = self.client.patch(f'/api/v1/teachers/{teachers[i].id}',
                                   json={'fullname': teachers[i+1].fullname})
            self.assertEqual(res.status_code, 400)
        # No data
        res = self.client.patch(f'/api/v1/teachers/{teachers[0].id}', json={})
        self.assertEqual(res.status_code, 400)
        # Junk invalid data
        res = self.client.patch(f'/api/v1/teachers/{teachers[1].id}',
                                json={'junk_data': 'Junk'})
        self.assertEqual(res.status_code, 400)

    def test_delete_teacher(self):
        # We are using get_query in order to skip archived user
        teachers_count = Teacher.get_query().count()
        teacher = Teacher.to_dict(Teacher.query.first())
        res = self.client.delete(f'/api/v1/teachers/{teacher["id"]}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        # We are using get_query in order to skip archived user
        new_count = Teacher.get_query().count()
        self.assertEqual(new_count+1, teachers_count)
        self.assertIn('deleted', data)
        self.assertEqual(data['deleted'], teacher['id'])

    def test_delete_teacher_invalid(self):
        first = Teacher.query.order_by(Teacher.id).first().id
        last = Teacher.query.order_by(Teacher.id.desc()).first().id
        for id in [first - 1, last + 1]:
            res = self.client.delete(f'/api/v1/teachers/{id}')
            self.assertEqual(res.status_code, 404)
