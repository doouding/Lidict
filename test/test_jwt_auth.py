from django.test import TestCase, Client
from jwt_auth.models import User 
import json

class UserTestCase(TestCase):
    def setUp(self):
        # used for test unique validation
        User.objects.create_user(username='codert', password="87654321", email='codert.sn@gmail.com', nickname='哈哈哈')

        self.encoder = json.JSONEncoder()
   
    def test_user_create(self):
        c1 = Client()
        c2 = Client()
        c3 = Client()
        c4 = Client()
        c5 = Client()
        c6 = Client()
        encoder = self.encoder

        # the user info is valid
        r1 = c1.post('/api/user/', encoder.encode({"username": "newuser1", "password":"12345678", "nickname": "test1", "email": "xx1@example.com"}), content_type="application/json")        
        # missing required field
        r2 = c2.post('/api/user/', encoder.encode({"username": "newuser2", "password": "87654321"}), content_type="application/json")
        # given `username` field is already exist
        r3 = c3.post('/api/user/', encoder.encode({"username": "codert", "password": "87654321", "nickname": "test3", "email": "xx3@example.com"}), content_type="application/json")
        # given `email` field is already exist
        r4 = c4.post('/api/user/', encoder.encode({"username": "newuser4", "password": "87654321", "nickname": "test4", "email": "codert.sn@gmail.com"}), content_type="application/json")
        # given `username` field is already exist but uppercase
        r5 = c5.post('/api/user/', encoder.encode({"username": "CODERT", "password": "87654321", "nickname": "test5", "email": "xx5@example.com"}), content_type="application/json")
        # given `email` field is already exist bu uppercase
        r6 = c6.post('/api/user/', encoder.encode({"username": "newuser6", "password": "87654321", "nickname": "test6", "email": "CODERT.SN@gmail.com"}), content_type="application/json")

        self.assertEqual(201, r1.status_code)
        self.assertEqual(400, r2.status_code)
        self.assertEqual(400, r3.status_code)
        self.assertEqual(400, r4.status_code)
        self.assertEqual(400, r5.status_code)
        self.assertEqual(400, r6.status_code)

class JwtAuthTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="codert", password="87654321", email="xxx@xx.com", nickname="xx")

        self.encoder = json.JSONEncoder()

    def test_token_request(self):
        c1 = Client()
        c2 = Client()
        c3 = Client()
        c4 = Client()
        encoder = self.encoder

        # the user info is valid
        r1 = c1.post('/api/auth/', encoder.encode({ "username": "codert", "pwd": "87654321" }), content_type="application/json")
        # missing `pwd` field
        r2 = c2.post('/api/auth/', encoder.encode({ "username": "codert", "xx": "xxxxxxxx" }), content_type="application/json")
        # the password is incorrect
        r3 = c3.post('/api/auth/', encoder.encode({ "username": "codert", "pwd": "12345678" }), content_type="application/json")
        # the user isn't exsit
        r4 = c4.post('/api/auth/', encoder.encode({ "username": "donotexist", "pwd": "12345678" }), content_type="application/json")

        self.assertEqual(201, r1.status_code)
        self.assertEqual(r2.json()['detail'], 'Incomplete authentication information')
        self.assertEqual(r3.json()['detail'], 'Incorrect authentication information')
        self.assertEqual(r3.json()['detail'], 'Incorrect authentication information')
    
    def test_token_validation(self):
        c1 = Client()
        c2 = Client()
        encoder = self.encoder

        r1 = c1.post('/api/auth/', encoder.encode({ "username": "codert", "pwd": "87654321" }), content_type='application/json')
        r2 = c2.get(f'/api/auth/{r1.json()["token"]}/')

        self.assertEqual(200, r2.status_code)

    def test_token_delete(self):
        c1 = Client()
        c2 = Client()
        c3 = Client()
        encoder = self.encoder

        r1 = c1.post('/api/auth/', encoder.encode({ "username": "codert", "pwd": "87654321" }), content_type="application/json")
        r2 = c2.delete(f'/api/auth/{r1.json()["token"]}/')
        r3 = c3.get(f'/api/auth/{r1.json()["token"]}/')
        
        self.assertEqual(204, r2.status_code)
        self.assertEqual(400, r3.status_code)
