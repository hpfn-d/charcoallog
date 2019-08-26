# import json

from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.bank.models import Extract


class AjaxPostTest(TestCase):
    fixtures = ['user.json', 'update_del.json']

    def setUp(self):
        self.login_in = self.client.login(username='test', password='1qa2ws3ed')

    def test_login_ok(self):
        self.assertTrue(self.login_in)

    def test_count_records(self):
        self.assertEqual(2, Extract.objects.all().count())

    def test_ajax_remove(self):
        """
        Delete first record - payment == principal
        Return empty content - 204
        Only one record now
        payment == cartao
        """
        # obj = Extract.objects.get(**self.data)

        # self.data['pk'] = obj.pk
        response = self.client.delete(r('bank:home_api', 1))

        count = Extract.objects.all().count()
        cartao = Extract.objects.filter(pk=2).exists()
        # no_return = response.content.decode()

        expected = [
            (response.status_code, 204),
            (1, count),
            (True, cartao),
            # (no_return, '')
        ]

        for resp, e in expected:
            with self.subTest():
                self.assertEqual(resp, e)
