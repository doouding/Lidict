from django.test import TestCase, Client
from django.contrib.auth.models import User
import json

class JwtAuthTestCase(TestCase):
    def setUp(self):
        u = User.objects.create_user(username="codert", password="87654321")
        u.save()

        self.encoder = json.JSONEncoder()

    def test_token_request(self):
        c1 = Client()
        c2 = Client()
        c3 = Client()
        c4 = Client()
        encoder = self.encoder

        r1 = c1.post('/api/auth/', encoder.encode({ "username": "codert", "pwd": "87654321" }), content_type="application/json")
        r2 = c2.post('/api/auth/', encoder.encode({ "username": "codert", "xx": "xxxxxxxx" }), content_type="application/json")
        r3 = c3.post('/api/auth/', encoder.encode({ "username": "codert", "pwd": "12345678" }), content_type="application/json")
        r4 = c4.post('/api/auth/', encoder.encode({ "username": "donotexist", "pwd": "12345678" }), content_type="application/json")

        self.assertEqual(201, r1.status_code)
        self.assertEqual(r2.json()['detail'], '不完整的验证信息')
        self.assertEqual(r3.json()['detail'], '验证信息错误')
        self.assertEqual(r3.json()['detail'], '验证信息错误')
    
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