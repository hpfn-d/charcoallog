import datetime as dt
from decimal import Decimal

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.get_service import MethodGet
from charcoallog.bank.models import Extract, Schedule
from charcoallog.bank.post_service import MethodPost
from charcoallog.bank.service import ScheduleData, ShowData


class RQST:
    pass


class ServiceLayerTest(TestCase):
    def setUp(self):
        now = dt.datetime.today()
        start = now + dt.timedelta(days=-1)
        ends = now + dt.timedelta(days=1)

        now_str = now.strftime("%Y-%m-%d")
        ends_str = ends + dt.timedelta(days=1)
        start_str = start + dt.timedelta(days=-1)

        self.user_name = 'teste'
        self.category = 'test'
        self.account_name = 'principal'
        data = dict(
            user_name=self.user_name,
            date=now_str,
            money='10.00',
            description='test',
            category=self.category,
            payment=self.account_name
        )
        others_data = dict(
            user_name='other',
            date=now_str,
            money='100.00',
            description='test',
            category=self.category,
            payment=self.account_name
        )
        Schedule.objects.create(**data)

        Extract.objects.create(**data)
        Extract.objects.create(**others_data)
        search_data = dict(column='all', from_date=start_str, to_date=ends_str)
        RQST.method = "GET"
        RQST.GET = search_data
        RQST.POST = dict()
        RQST.user = self.user_name
        self.response = ShowData(RQST)
        self.schdl = ScheduleData(self.user_name)

    def test_query_user_instance(self):
        self.assertIsInstance(self.response.query_bank, QuerySet)

    def test_form1_instance(self):
        self.assertIsInstance(self.response.form1, MethodPost)

    def test_form2_instance(self):
        self.assertIsInstance(self.response.form2, MethodGet)

    def test_brief_bank_instance(self):
        self.assertIsInstance(self.response.brief_bank, BriefBank)

    def test_brief_bank_account_names(self):
        self.assertIn(self.account_name, self.response.brief_bank.account_val_sorted())

    def test_brief_bank_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
        """
        self.assertEqual(self.response.brief_bank.whats_left(), Decimal('10.00'))

    def test_query_schedule_instance(self):
        self.assertIsInstance(self.schdl.query_schedule, QuerySet)

    def test_brief_schedule_instance(self):
        self.assertIsInstance(self.schdl.brief_schedule(), BriefBank)

    def test_brief_schedule_account_names(self):
        self.assertIn(self.account_name, self.schdl.brief_schedule().account_val_sorted())

    def test_brief_schedule_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
        """
        content = self.schdl.brief_schedule().account_val_sorted()
        self.assertIn('principal', content)
        content = self.schdl.brief_schedule().whats_left()
        self.assertEqual(Decimal('10'), content)

    def test_summary_instance(self):
        self.assertIsInstance(self.response.summary_categories, str)

    def test_summary_account_names(self):
        self.assertJSONEqual(
            self.response.summary_categories, '{"test": "10.00"}'
        )

    def test_summary_account_names_values(self):
        """
        user test only has 10
        user other has 100
        """
        self.assertIn('{"test": "10.00"}', self.response.summary_categories)

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

        qs_summary = Extract.objects.user_logged(self.user_name).summary('2017', '12')
        self.assertNotIn('transfer', qs_summary)
        self.assertNotIn('investments', qs_summary)
