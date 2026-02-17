from django.test import TestCase, Client
from django.urls import reverse


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user-register')

    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'email': 'a@b.com',
            'password': 'abcd1234',
            'password_confirm': 'abcd1234'
        }
        resp = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('message', resp.json())
        self.assertEqual(resp.json()['message'], 'User registered successfully')

    def test_password_mismatch(self):
        data = {
            'username': 'testuser2',
            'email': 'b@c.com',
            'password': 'abcd1234',
            'password_confirm': 'different'
        }
        resp = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Passwords do not match', resp.content.decode())

    def test_health_endpoint(self):
        # the simple health view should return a small JSON object
        resp = self.client.get(reverse('health'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'status': 'ok'})

