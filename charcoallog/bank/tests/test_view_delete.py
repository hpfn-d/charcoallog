# import json

from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.bank.models import Extract


class AjaxPostTest(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.user_name = 'test'
        self.data = dict(
            user_name=self.user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )
        Extract.objects.create(**self.data)

        # keep tihs one
        update_test = dict(
            user_name=self.user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='cartao credito'
        )
        Extract.objects.create(**update_test)

        self.login_in = self.client.login(username=self.user_name, password='1qa2ws3ed')

    def test_login_ok(self):
        self.assertTrue(self.login_in)

    def test_count_records(self):
        self.assertEqual(2, Extract.objects.filter(user_name=self.user_name).count())

    def test_ajax_remove(self):
        """
        Delete first record - payment == principal
        4 asserts
        Return empty content - 204
        Only one record now
        No payment principal
        Check response content
        """
        obj = Extract.objects.get(**self.data)

        self.data['pk'] = obj.pk
        response = self.client.delete(r('bank:home_api', obj.pk))

        keep = Extract.objects.filter(user_name=self.user_name).count()
        no_principal = Extract.objects.filter(payment='principal').count()
        no_return = response.content.decode()

        expected = [
            (response.status_code, 204),
            (1, keep),
            (0, no_principal),
            (no_return, '')
        ]

        for resp, e in expected:
            with self.subTest():
                self.assertEqual(resp, e)
