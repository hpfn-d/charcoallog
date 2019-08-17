import datetime as dt
import os
from unittest.mock import patch

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract
from charcoallog.core import service
from charcoallog.core.service import SUMMARY, BuildHome, collect_summary
from charcoallog.investments.brief_investment_service import BriefInvestment


class BuildHomeTest(TestCase):
    @patch('charcoallog.core.service.by_month_cat')
    def setUp(self, quiet):
        self.user = 'teste'
        self.obj = BuildHome(self.user)

    def test_attr(self):
        expected = [
            hasattr(service, 'Extract'),
            hasattr(service, 'BriefBank'),
            # hasattr(service, 'Scrap'),
            hasattr(self.obj, 'query_bank'),
            hasattr(self.obj, 'line1'),
            # hasattr(self.obj, 'selic_info'),
            # hasattr(self.obj, 'ibov_info'),
            # hasattr(self.obj, 'ipca_info'),
            hasattr(self.obj, 'query_user_invest'),
            hasattr(self.obj, 'query_user_details'),
            hasattr(self.obj, 'line2'),
            hasattr(self.obj, 'summary_categories')
        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(e)

    def test_instance(self):
        expected = [
            (isinstance(self.obj.query_bank, QuerySet)),
            (isinstance(self.obj.line1, BriefBank)),
            # (isinstance(self.obj.selic_info, list)),
            # (isinstance(self.obj.ibov_info, list)),
            # (isinstance(self.obj.ipca_info, list)),
            (isinstance(self.obj.query_user_invest, QuerySet)),
            (isinstance(self.obj.query_user_details, QuerySet)),
            (isinstance(self.obj.line2, BriefInvestment)),

        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(e)


class CoreSummary(TestCase):
    fixtures = ['core_user.json']

    def setUp(self):
        """
        dict[year][user]

        teste1 - 2018, one record
        teste1 - 2019, one record

        teste2 - 2019, one record

        """
        self.now = dt.datetime.today()
        current = self.now.strftime("%Y-%m-%d")

        self.user1 = 'teste1'
        d = '2018-01-01'

        data = dict(
            user_name=self.user1,
            date=d,
            money='10.00',
            description='test',
            category='category',
            payment='principal'
        )
        Extract.objects.create(**data)
        data['date'] = current
        Extract.objects.create(**data)

        self.user2 = 'teste2'

        data['user_name'] = self.user2
        data['date'] = current
        Extract.objects.create(**data)

        self.to_json = collect_summary()

    def test_year_summary(self):
        """ check first key - year """
        self.assertIn(str(self.now.year), self.to_json.keys())

    def test_users_summary(self):
        """ two users """
        # check second key - user
        self.assertEqual(len(self.to_json[str(self.now.year)]), 2)
        self.assertIn(self.user1, self.to_json[str(self.now.year)].keys())
        self.assertIn(self.user2, self.to_json[str(self.now.year)].keys())

    def test_user_instance_value(self):
        """ should be a list """
        self.assertIsInstance(self.to_json[str(self.now.year)][self.user1], list)
        self.assertIsInstance(self.to_json[str(self.now.year)][self.user2], list)

    def test_content_summary(self):
        """ core does not show current month"""
        self.assertEqual(len(self.to_json[str(self.now.year)][self.user1]), 0)
        self.assertEqual(len(self.to_json[str(self.now.year)][self.user2]), 0)

    def test_count_records(self):
        """ but user1 have 2 records"""
        qs = Extract.objects.user_logged(self.user1).all()
        self.assertEqual(qs.count(), 2)

    def tearDown(self):
        os.remove(SUMMARY)


class CoreSummaryNoData(TestCase):
    fixtures = ['core_user.json']

    def setUp(self):
        self.now = dt.datetime.today()
        self.to_json = collect_summary()

    def test_has_user(self):
        self.assertIn('teste1', self.to_json[str(self.now.year)].keys())
        self.assertIn('teste2', self.to_json[str(self.now.year)].keys())

    def test_no_data(self):
        self.assertFalse(self.to_json[str(self.now.year)]['teste1'])
        self.assertFalse(self.to_json[str(self.now.year)]['teste2'])
