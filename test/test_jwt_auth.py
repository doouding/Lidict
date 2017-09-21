from django.test import TestCase
from jwt_auth.models import User
from .util import test_request

class UserTestCase(TestCase):
    def setUp(self):
        # used for test unique validation
        User.objects.create_user(username='codert', password="87654321", email='codert.sn@gmail.com', nickname='setup')

    def test_user_create(self):
        # the user info is valid
        res1 = test_request('/api/user/', data={"username": "newuser1", "password":"12345678", "nickname": "test1", "email": "xx1@example.com"})        
        # missing required field
        res2 = test_request('/api/user/', data={"username": "newuser2", "password": "87654321"})
        # given `username` field is already exist
        res3 = test_request('/api/user/', data={"username": "codert", "password": "87654321", "nickname": "test3", "email": "xx3@example.com"})
        # given `email` field is already exist
        res4 = test_request('/api/user/', data={"username": "newuser4", "password": "87654321", "nickname": "test4", "email": "codert.sn@gmail.com"})
        # given `username` field is already exist but uppercase
        res5 = test_request('/api/user/', data={"username": "CODERT", "password": "87654321", "nickname": "test5", "email": "xx5@example.com"})
        # given `email` field is already exist bu uppercase
        res6 = test_request('/api/user/', data={"username": "newuser6", "password": "87654321", "nickname": "test6", "email": "CODERT.SN@gmail.com"})

        self.assertEqual(201, res1.status_code)
        self.assertEqual(400, res2.status_code)
        self.assertEqual(400, res3.status_code)
        self.assertEqual(400, res4.status_code)
        self.assertEqual(400, res5.status_code)
        self.assertEqual(400, res6.status_code)

    def test_user_retrieve(self):
        user = User.objects.get(username='codert')

        res1 = test_request('/api/user/codert/', method='GET', auth=user)
        data = res1.json()

        self.assertEqual(200, res1.status_code)
        self.assertEqual('codert', data['username'])
        self.assertEqual('setup', data['nickname'])
        self.assertEqual('codert.sn@gmail.com', data['email'])

    def test_update_password(self):
        user = User.objects.get(username='codert')

        res1 = test_request('/api/user/codert/', method='PUT', data={"password": "zaqwsx21", "nickname":"rename1"}, auth=user)

        user.refresh_from_db()
        self.assertEqual(True, user.check_password('zaqwsx21'))
        self.assertEqual('rename1', user.nickname)
        self.assertEqual(200, res1.status_code)

class JwtAuthTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="codert", password="87654321", email="xxx@xx.com", nickname="xx")

    def test_token_request(self):
        # the user info is valid
        res1 = test_request('/api/auth/', data={"username": "codert", "pwd": "87654321"})
        # missing `pwd` field
        res2 = test_request('/api/auth/', data={"username": "codert", "xx": "xxxxxxxx"})
        # the password is incorrect
        res3 = test_request('/api/auth/', data={"username": "codert", "pwd": "12345678"})
        # the user isn't exsit
        res4 = test_request('/api/auth/', data={"username": "donotexist", "pwd": "12345678"})

        self.assertEqual(201, res1.status_code)
        self.assertEqual(res2.json()['detail'], 'Incomplete authentication information')
        self.assertEqual(res3.json()['detail'], 'Incorrect authentication information')
        self.assertEqual(res3.json()['detail'], 'Incorrect authentication information')
        self.assertEqual(res4.json()['detail'], 'Incorrect authentication information')

    def test_token_validation(self):
        res1 = test_request('/api/auth/', data={"username": "codert", "pwd": "87654321"})
        res2 = test_request(f'/api/auth/{res1.json()["token"]}/', method='GET')

        self.assertEqual(200, res2.status_code)

    def test_token_delete(self):
        res1 = test_request('/api/auth/', data={"username": "codert", "pwd": "87654321"})
        res2 = test_request(f'/api/auth/{res1.json()["token"]}/', method='DELETE')
        res3 = test_request(f'/api/auth/{res1.json()["token"]}/', method='GET')

        self.assertEqual(204, res2.status_code)
        self.assertEqual(400, res3.status_code)
