import unittest

from tests.sample_users import generate_names, generate_usernames, \
    generate_random_users


class FixtureMethodTestCase(unittest.TestCase):
    def test_generate_usernames(self):
        """Function return different users names"""
        random_names = generate_names(count=2)
        random_names = [name for _ in range(10) for name in random_names]
        usernames = generate_usernames(random_names)
        self.assertEqual(len(random_names), len(set(usernames)))

    def test_generate_random_users(self):
        """Function users dictionaries"""
        users = generate_random_users(500, ['teacher', 'student'])
        usernames = set([user['username'] for user in users])
        self.assertEqual(len(usernames), len(users))
