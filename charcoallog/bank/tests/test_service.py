# from collections import OrderedDict
from decimal import Decimal
from unittest.mock import patch

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.get_service import MethodGet
from charcoallog.bank.models import Extract, Schedule
from charcoallog.bank.post_service import MethodPost
from charcoallog.bank.service import ShowData


class RQST:
    pass


class ServiceLayerTest(TestCase):
    @patch('charcoallog.bank.service.date')
    def setUp(self, date):
        self.user_name = 'teste'
        self.category = 'test'
        self.account_name = 'principal'
        data = dict(
            user_name=self.user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category=self.category,
            payment=self.account_name
        )
        others_data = dict(
            user_name='other',
            date='2017-12-21',
            money='100.00',
            description='test',
            category=self.category,
            payment=self.account_name
        )
        Schedule.objects.create(**data)

        Extract.objects.create(**data)
        Extract.objects.create(**others_data)
        search_data = dict(column='all', from_date='2017-12-01', to_date='2017-12-31')
        RQST.method = "GET"
        RQST.GET = search_data
        RQST.POST = dict()
        RQST.user = self.user_name
        date.today.return_value.strftime.return_value = '2017-12-01'
        self.response = ShowData(RQST)

    def test_query_user_instance(self):
        self.assertIsInstance(self.response.query_bank, QuerySet)

    def test_form1_instance(self):
        self.assertIsInstance(self.response.form1, MethodPost)

    def test_form2_instance(self):
        self.assertIsInstance(self.response.form2, MethodGet)

    def test_brief_bank_instance(self):
        self.assertIsInstance(self.response.brief_bank, BriefBank)

    def test_brief_bank_account_names(self):
        self.assertIn(self.account_name, self.response.brief_bank.account_names())

    def test_brief_bank_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
            bank.account_names must be called before whats_left
            (account_values)
        """
        self.response.brief_bank.account_names()
        self.assertEqual(self.response.brief_bank.whats_left(), Decimal('10.00'))

    def test_query_schedule_instance(self):
        self.assertIsInstance(self.response.query_schedule, QuerySet)

    def test_brief_schedule_instance(self):
        self.assertIsInstance(self.response.brief_schedule, BriefBank)

    def test_brief_schedule_account_names(self):
        self.assertIn(self.account_name, self.response.brief_schedule.account_names())

    def test_brief_schedule_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
            bank.account_names must be called before whats_left
            (account_values)
        """
        self.response.brief_schedule.account_names()
        self.assertEqual(self.response.brief_schedule.whats_left(), Decimal('10.00'))

    def test_summary_instance(self):
        self.assertIsInstance(self.response.summary_categories, str)

    def test_summary_account_names(self):
        self.assertJSONEqual(
            self.response.summary_categories, '{"test": {"money__sum": "10"}}'
        )

    def test_summary_account_names_values(self):
        """
        user test only has 10
        user other has 100
        """
        self.assertIn('{"test": {"money__sum": "10"}', self.response.summary_categories)

    def test_summary_exclude(self):
        data = dict(
            user_name=self.user_name,
            date='2017-12-21',
            money=10.00,
            description='test',
            category='transfer',
            payment=self.account_name
        )
        Extract.objects.create(**data)

        data = dict(
            user_name=self.user_name,
            date='2017-12-21',
            money=10.00,
            description='test',
            category='investments',
            payment=self.account_name
        )
        Extract.objects.create(**data)

        qs_summary = Extract.objects.user_logged(self.user_name).summary('2017-12-21')
        self.assertNotIn('transfer', qs_summary)
        self.assertNotIn('investments', qs_summary)
