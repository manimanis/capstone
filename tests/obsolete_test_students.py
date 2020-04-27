import unittest
import random

from app import create_app, db
from app.models import Student
from tests import generate_names, generate_usernames

INSERT_COUNT = 20
INEXISTANT_COUNT = 23
NEW_INSERT_COUNT = 26
TOTAL_NAMES = 30

random_names = generate_names(TOTAL_NAMES)
usernames = generate_usernames(random_names)


class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        StudentTestCase.insert_sample_data()
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
            student = Student(username=username, fullname=name)
            student.insert()

    def has_response_keys_single(self, data):
        """The server response for a single student request should include all
        of this fields"""
        keys = ['success', 'student']
        for key in keys:
            self.assertIn(key, data)

        self.has_all_fields(data['student'])

    def has_response_keys(self, data):
        """The server response should include all of this fields"""
        keys = ['success', 'students_count', 'search_count', 'start', 'end',
                'students']
        for key in keys:
            self.assertIn(key, data)

        for student in data['students']:
            self.has_all_fields(student)

    def has_all_fields(self, student):
        """The student dictionaries if they exists should contain all of this
        fields"""
        fields = ['dt_creation', 'fullname', 'id', 'username']
        for field in fields:
            self.assertIn(field, student)

    def test_get_students(self):
        res = self.client.get('/api/v1/students')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.has_response_keys(data)
        self.assertTrue(data['success'])
        self.assertGreater(data['students_count'], 0)
        self.assertEqual(data['students_count'], data['search_count'])
        self.assertEqual(data['start'], 0)
        self.assertGreater(data['end'], 0)
        self.assertEqual(len(data['students']), data['end'] - data['start'])

    def test_get_students_range(self):
        students_count = Student.get_query().count()
        start = random.randint(0, students_count // 2 - 1)
        end = random.randint(students_count // 2, students_count - 1)
        res = self.client.get(f'/api/v1/students?start={start}&end={end}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.has_response_keys(data)
        self.assertTrue(data['success'])
        self.assertEqual(data['students_count'], students_count)
        self.assertEqual(data['students_count'], data['search_count'])
        self.assertEqual(data['start'], start)
        self.assertEqual(data['end'], end)
        self.assertEqual(len(data['students']), end - start)

    def test_get_students_search(self):
        student = Student.query.first()
        # Search for words we are sure they exist in the Database
        words = student.fullname.split()
        for word in words:
            students_count = (Student.query
                              .filter(Student.fullname.ilike(f'%{word}%'))
                              .count())
            res = self.client.get(f'/api/v1/students?search={word}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys(data)
            self.assertTrue(data['success'])
            self.assertEqual(data['search_count'], students_count)
            self.assertNotEqual(data['students_count'], data['search_count'])
            self.assertGreater(data['search_count'], 0)

    def test_get_students_search_inexistant(self):
        # Search for names that does not exist
        for name in random_names[INSERT_COUNT:INEXISTANT_COUNT]:
            res = self.client.get(f'/api/v1/students?search={name}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys(data)
            self.assertTrue(data['success'])
            self.assertEqual(data['search_count'], 0)
            self.assertNotEqual(data['students_count'], data['search_count'])

    def test_get_single_student(self):
        # select three random ids
        students = Student.query.all()
        ids = [student.id for student in students]
        ids = random.choices(ids, k=3)
        for id in ids:
            res = self.client.get(f'/api/v1/students/{id}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)

    def test_get_single_student_inexistant(self):
        # select two inexistant ids
        first = Student.query.order_by(Student.id).first().id
        last = Student.query.order_by(Student.id.desc()).first().id
        for id in [first - 1, last + 1]:
            res = self.client.get(f'/api/v1/students/{id}')
            self.assertEqual(res.status_code, 404)

    def test_insert_student(self):
        old_count = Student.query.count()
        for name, username in zip(
                random_names[INEXISTANT_COUNT:NEW_INSERT_COUNT],
                usernames[INEXISTANT_COUNT:NEW_INSERT_COUNT]):
            student_dict = {
                'username': username,
                'fullname': name
            }
            res = self.client.post(f'/api/v1/students', json=student_dict)
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)
            self.assertEqual(data['student']['username'], username)
            self.assertEqual(data['student']['fullname'], name)
        new_count = Student.query.count()
        self.assertEqual(new_count - old_count,
                         NEW_INSERT_COUNT - INEXISTANT_COUNT)

    def test_insert_student_invalid(self):
        students_dict = [
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
        for student_dict in students_dict:
            res = self.client.post(f'/api/v1/students', json=student_dict)
            self.assertEqual(res.status_code, 400)
        for key, value in students_dict[0].items():
            res = self.client.post(f'/api/v1/students', json={key: value})
            self.assertEqual(res.status_code, 400)

    def test_update_student(self):
        # select random ids
        students = Student.query.all()
        ids = [student.id for student in students]
        ids = random.choices(ids, k=len(random_names)-NEW_INSERT_COUNT)
        for id, fullname in zip(ids, random_names[NEW_INSERT_COUNT:]):
            res = self.client.patch(f'/api/v1/students/{id}',
                                   json={'fullname': fullname})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.has_response_keys_single(data)
            self.assertEqual(fullname, data['student']['fullname'])

    def test_update_student_invalid(self):
        students = Student.query.all()
        for i in range(3):
            res = self.client.patch(f'/api/v1/students/{students[i].id}',
                                   json={'fullname': students[i+1].fullname})
            self.assertEqual(res.status_code, 400)
        # No data
        res = self.client.patch(f'/api/v1/students/{students[0].id}', json={})
        self.assertEqual(res.status_code, 400)
        # Junk invalid data
        res = self.client.patch(f'/api/v1/students/{students[1].id}',
                                json={'junk_data': 'Junk'})
        self.assertEqual(res.status_code, 400)

    def test_delete_student(self):
        # We are using get_query in order to skip archived user
        students_count = Student.get_query().count()
        student = Student.to_dict(Student.query.first())
        res = self.client.delete(f'/api/v1/students/{student["id"]}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        # We are using get_query in order to skip archived user
        new_count = Student.get_query().count()
        self.assertEqual(new_count+1, students_count)
        self.assertIn('deleted', data)
        self.assertEqual(data['deleted'], student['id'])

    def test_delete_student_invalid(self):
        first = Student.query.order_by(Student.id).first().id
        last = Student.query.order_by(Student.id.desc()).first().id
        for id in [first - 1, last + 1]:
            res = self.client.delete(f'/api/v1/students/{id}')
            self.assertEqual(res.status_code, 404)
