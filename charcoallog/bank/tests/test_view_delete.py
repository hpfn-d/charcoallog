# import json

from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.bank.models import Extract


class AjaxPostTest(TestCase):
    def setUp(self):
        user_name = 'teste'
        self.data = dict(
            user_name=user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )
        Extract.objects.create(**self.data)

        # the return after delete
        update_test = dict(
            user_name=user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='cartao credito'
        )
        Extract.objects.create(**update_test)

        user = User.objects.create(username=user_name)
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username=user_name, password='1qa2ws3ed')

    def test_login_ok(self):
        self.assertTrue(self.login_in)

    def test_count_records(self):
        self.assertEqual(2, Extract.objects.filter(user_name='teste').count())

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

        self.assertEqual(response.status_code, 204)
        self.assertEqual(1, Extract.objects.filter(user_name='teste').count())
        self.assertEqual(0, Extract.objects.filter(payment='principal').count())
        # response is empty after delete
        self.assertFalse(response.content.decode())
