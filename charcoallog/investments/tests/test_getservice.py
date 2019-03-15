from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.forms import InvestmentSearchForm
from charcoallog.investments.get_service import MethodGet
from charcoallog.investments.models import NewInvestment


class RQST:
    pass


class InvalidGetMethod(TestCase):
    def test_no_get_method(self):
        """ Send a POST must keep get_form attribute as 'None' """
        data = dict(date='2017-12-21',
                    money='10.00',
                    description='test',
                    category='test',
                    payment='principal')
        query_user = NewInvestment.objects.user_logged('teste')
        RQST.method = "POST"
        RQST.GET = data
        response = MethodGet(RQST, query_user)
        self.assertEqual(response.get_form, None)


class ValidGetMethod(TestCase):
    def setUp(self):
        data = dict(
            user_name='teste',
            date='2017-12-21',
            money='10.00',
            kind='test',
            tx_op='1.00',
            brokerage='Main'
        )

        NewInvestment.objects.create(**data)

        query_user = NewInvestment.objects.user_logged('teste')
        search_data = dict(column='all', from_date='2017-12-01', to_date='2017-12-31')
        RQST.method = "GET"
        RQST.GET = search_data
        self.response = MethodGet(RQST, query_user)

    def test_send_get_method(self):
        """
            Valid GET method must set get_form attribute as
            an instance of InvestmentSearchForm.
        """
        self.assertIsInstance(self.response.get_form, InvestmentSearchForm)

    def test_valid_form(self):
        self.assertTrue(self.response.get_form.is_valid())

    def test_cleaned_data_values(self):
        col = self.response.get_form.cleaned_data.get('column')
        self.assertEqual(col, 'all')
        f_d = str(self.response.get_form.cleaned_data.get('from_date'))
        self.assertEqual(f_d, '2017-12-01')
        t_d = str(self.response.get_form.cleaned_data.get('to_date'))
        self.assertEqual(t_d, '2017-12-31')

    def test_record_exists(self):
        self.assertTrue(NewInvestment.objects.filter(brokerage='Main').exists())

    def test_valid_search(self):
        """
            query_default attribute must be a QuerySet instance
            after a valid search.
        """
        self.assertIsInstance(self.response.query_default, QuerySet)


class QModuleTest(TestCase):
    def setUp(self):
        data = dict(
            user_name='teste',
            date='2017-12-21',
            money='10.00',
            kind='test',
            tx_op='1.00',
            brokerage='Main'
        )

        NewInvestment.objects.create(**data)

        query_user = NewInvestment.objects.user_logged('teste')
        search_data = dict(column='Main', from_date='2017-12-01', to_date='2017-12-31')
        RQST.method = "GET"
        RQST.GET = search_data
        self.response = MethodGet(RQST, query_user)

    def test_record_exists(self):
        self.assertTrue(NewInvestment.objects.filter(brokerage='Main').exists())

    def test_valid_form(self):
        self.assertTrue(self.response.get_form.is_valid())

    def test_bills_var(self):
        self.assertIsInstance(self.response.query_default, QuerySet)


# I do not know how to pretend a complete request(RQST)
# to show an 'messages.error()
class InvalidSearch(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()
        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        search_data = dict(column='all', from_date='2017-01-01', to_date='2017-01-01')
        self.response = self.client.get(r('investments:home'), search_data)

    def test_invalid_search(self):
        """ Invalid search must shows an error message """
        self.assertContains(self.response, '<ul class="messages"', 1)
        self.assertContains(self.response, '<li class="error">', 1)
