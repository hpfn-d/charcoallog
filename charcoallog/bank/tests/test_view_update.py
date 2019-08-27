import json

from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.bank.models import Extract


class AjaxPostTest(TestCase):
    fixtures = ['user.json', 'update_del.json']

    def setUp(self):
        self.user_name = 'test'

        self.login_in = self.client.login(username=self.user_name, password='1qa2ws3ed')

    def test_login(self):
        self.assertTrue(self.login_in)

    # def test_post(self):
    #     """
    #        GET method must return 405
    #        method not allowed
    #     """
    #     self.assertEqual(405, self.client.get(r('bank:update')).status_code)

    def test_ajax_update(self):
        """
        Update 'payment' field value
        'principal started with 10 and now has 20
        'cartao credito' does not exists after this update

        return values that are used by line1 - brief_bank
        """
        to_update = dict(
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal',
            pk=2
        )
        response = self.client.put(r('bank:home_api', 2),
                                   json.dumps(to_update),
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)

        expected = [
            'principal',
            '20.0',
            'whats_left',
            '20.0'
        ]

        for value in expected:
            with self.subTest():
                self.assertIn(value, response.content.decode())

        self.assertNotIn('cartao credito', response.content.decode())

    def test_ajax_fail_update(self):
        """
        Invalid form, empty field
        """
        data = dict()
        data['payment'] = ''
        data['pk'] = 1
        response = self.client.put(r('bank:home_api', 1),
                                   json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)

        resp_d = json.loads(response.content.decode())
        self.assertIsInstance(resp_d, dict)
        self.assertTrue(resp_d.get('payment'))
        self.assertIn('This field may not be blank', resp_d['payment'][0])

    def test_form_not_valid(self):
        """
         Invalid date - day
        """
        not_valid = dict(
            date='2017-12-212',
            money='10.00',
            description='test',
            category='test',
            payment='principal',
            pk=1
        )
        response = self.client.put(r('bank:home_api', 1),
                                   json.dumps(not_valid),
                                   content_type='application/json')

        self.assertEqual(400, response.status_code)

        resp_d = json.loads(response.content.decode())
        self.assertIsInstance(resp_d, dict)
        self.assertIn('date', resp_d.keys())
        self.assertIn('Date has wrong format', resp_d['date'][0])

    def test_user_name(self):
        """
        Check tests have one user only
        """
        all_records = Extract.objects.all().count()
        one_user_records = Extract.objects.filter(user_name=self.user_name).count()
        self.assertEqual(all_records, one_user_records)
