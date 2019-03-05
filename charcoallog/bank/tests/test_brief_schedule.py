from decimal import Decimal

from django.test import TestCase

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Schedule


class BriefScheduleTest(TestCase):
    def setUp(self):
        user_name = 'teste'
        self.account_name = 'principal'
        data = dict(
            user_name=user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment=self.account_name
        )

        Schedule.objects.create(**data)
        query_user = Schedule.objects.user_logged(user_name)
        self.response = BriefBank(query_user)
        self.brief_schedule_account_name = self.response.account_names()

    def test_schedule_names(self):
        self.assertIn(self.account_name, self.brief_schedule_account_name)

    def test_line1_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
            schedule.account_names must be called before whats_left
            (account_values)
        """
        self.assertEqual(self.response.whats_left(), Decimal('10.00'))
