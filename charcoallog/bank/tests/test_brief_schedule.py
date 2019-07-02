import datetime as dt
import json
from decimal import Decimal

from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Schedule


class BriefScheduleTest(TestCase):
    fixtures = ['schedule_data.json']

    def setUp(self):
        self.account_name = 'principal'

        query_user = Schedule.objects.user_logged('test')
        self.response = BriefBank(query_user)
        self.brief_schedule_account_name = self.response.account_val_sorted()

    def test_schedule_names(self):
        self.assertIn(self.account_name, self.brief_schedule_account_name)

    def test_line1_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
            schedule.account_names must be called before whats_left
            (account_values)
        """
        self.assertEqual(self.response.whats_left(), Decimal('10.00'))


class UpdateScheduleApi(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        now = dt.datetime.today()
        now_str = now.strftime("%Y-%m-%d")

        user_name = 'test'

        self.login_in = self.client.login(username=user_name, password='1qa2ws3ed')

        data = dict(
            user_name=user_name,
            date=now_str,
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )

        Schedule.objects.create(**data)
        data['money'] = '20.00'
        self.response = self.client.put(r('bank:schedule_api', 1),
                                        json.dumps(data),
                                        content_type='application/json')

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_status_code(self):
        self.assertEqual(200, self.response.status_code)

    def test_data_exists(self):
        self.assertTrue(Schedule.objects.filter(pk=1).exists())

    def test_db_record_value(self):
        qs = Schedule.objects.all()
        money = str(qs[0].money)
        self.assertEqual('20.00', money)

    def test_db_record(self):
        """
            whats_left attribute must be 20.00 now
        """
        self.assertEqual('20.0', self.response.content.decode())


class DeleteScheduleApi(TestCase):
    fixtures = ['schedule_data.json', 'user.json']

    def setUp(self):
        self.login_in = self.client.login(username='test', password='1qa2ws3ed')
        self.response = self.client.delete(r('bank:schedule_api', 1))

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_status_code(self):
        self.assertEqual(204, self.response.status_code)

    def test_data_in_db(self):
        self.assertFalse(Schedule.objects.all().exists())
