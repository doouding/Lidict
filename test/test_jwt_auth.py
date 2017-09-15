from django.test import TestCase, Client
from django.contrib.auth.models import User
from jwt_auth.views import AuthViews
import json

class JwtAuthTestCase(TestCase):
    def setUp(self):
        u = User.objects.create_user(username="codert", password="87654321")
        u.save()

    def test_token_request(self):
        c1 = Client()
        c2 = Client()
        c3 = Client()
        c4 = Client()
        encoder = json.JSONEncoder()

        r1 = c1.post('/auth', encoder.encode({ "username": "codert", "pwd": "87654321" }), content_type="application/json")
        r2 = c2.post('/auth', encoder.encode({ "username": "codert", "xx": "xxxxxxxx" }), content_type="application/json")
        r3 = c3.post('/auth', encoder.encode({ "username": "codert", "pwd": "12345678" }), content_type="application/json")
        r4 = c4.post('/auth', encoder.encode({ "username": "donotexist", "pwd": "12345678" }), content_type="application/json")

        self.assertEqual(201, r1.status_code)
        self.assertEqual(r2.json()['detail'], '不完整的验证信息')
        self.assertEqual(r3.json()['detail'], '验证信息错误')
        self.assertEqual(r3.json()['detail'], '验证信息错误')
