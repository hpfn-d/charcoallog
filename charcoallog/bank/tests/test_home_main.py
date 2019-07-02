from django.shortcuts import resolve_url as r
from django.test import TestCase


class HomeFailTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('bank:home'))

    def test_redirect_response(self):
        """ No login yet. Redirects to login page"""
        self.assertRedirects(self.response, '/conta/entrar/?next=/bank/')


class HomeOKTest(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.login_in = self.client.login(username='test', password='1qa2ws3ed')
        self.response = self.client.get(r('bank:home'))

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_get_status_code(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'bank/home.html')
