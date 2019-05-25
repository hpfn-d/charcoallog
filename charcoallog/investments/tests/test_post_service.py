from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.forms import InvestmentDetailsForm, InvestmentForm
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails
from charcoallog.investments.post_service import MethodPost


class RQST:
    pass


class ValidPostMethodNoDetails(TestCase):
    """ Invest NoDetails (class) MethodPost test """

    def setUp(self):
        self.data = dict(
            user_name='you',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='Ativa'
        )

        RQST.method = 'POST'
        RQST.POST = self.data
        RQST.user = 'you'
        self.response = MethodPost(RQST)

    def test_investmentform_instance(self):
        """
            investmentform attr must be a InvestmentForm instance.
        """
        self.assertIsInstance(self.response.i_form, InvestmentForm)
        self.assertIsInstance(self.response.d_form, InvestmentDetailsForm)

    def test_form_is_valid(self):
        self.assertFalse(self.response.d_form.is_valid())
        self.assertTrue(self.response.i_form.is_valid())

    def test_invest_form_save(self):
        select_data = NewInvestment.objects.get(pk=1)
        select_dict = dict(
            user_name=select_data.user_name,
            date=select_data.date.strftime('%Y-%m-%d'),
            tx_op=float(select_data.tx_op),
            money=float(select_data.money),
            kind=select_data.kind,
            brokerage=select_data.brokerage
        )

        self.assertDictEqual(self.data, select_dict)

    def test_send_invest_post_url(self):
        self.assertEqual(1, NewInvestment.objects.filter().count())


class NoDetailsByPost(TestCase):
    """ Test Invest NoDetails by POST verb"""

    def setUp(self):
        self.user = 'teste'
        user = User.objects.create(username=self.user)
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username=self.user, password='1qa2ws3ed')

        self.data = dict(
            user_name='you',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='Ativa'
        )
        self.response = self.client.post(r('investments:home'), self.data)

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_count_records(self):
        """
        Test if record is in (Invest) db and also check if it is
        saved by request.user
        """
        self.assertEqual(1, NewInvestment.objects.user_logged(self.user).count())


class ValidPostMethodWithDetails(TestCase):
    """ Invest Details (class) MethodPost test """

    def setUp(self):
        data = dict(
            user_name='you',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='Ativa',
        )

        self.details = dict(
            **data,
            which_target='Details',
            segment='Details',
            tx_or_price=0.00,
            quant=0.00,
        )

        RQST.method = 'POST'
        RQST.user = 'teste'
        RQST.POST = self.details
        self.direct = MethodPost(RQST)

    def test_valid(self):
        self.assertTrue(self.direct.d_form.is_valid())

    def test_record_in_db(self):
        self.assertTrue(NewInvestmentDetails.objects.filter(segment='Details').exists())


class DetailsByPost:
    """ Test Invest Details by POST verb"""

    def setUp(self):
        self.user = 'teste'
        user = User.objects.create(username=self.user)
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username=self.user, password='1qa2ws3ed')

        data = dict(
            user_name='you',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='Ativa',
        )

        self.details = dict(
            **data,
            which_target='Details',
            segment='Details',
            tx_or_price=0.00,
            quant=0.00,
        )

        self.response = self.client.post(r('investments:home'), self.details)

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_form_instance(self):
        self.assertTrue(isinstance(self.response.context['d_form'], InvestmentDetailsForm))

    def test_detailscount_records(self):
        """
        Test if record (Details) is in db and also check if it is
        saved by request.user
        """
        self.assertEqual(1, NewInvestmentDetails.objects.user_logged(self.user).count())
