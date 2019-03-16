from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.forms import InvestmentDetailsForm, InvestmentForm
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails
from charcoallog.investments.post_service import MethodPost


class RQST:
    pass


class ValidPostMethodNoDetails(TestCase):
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

        RQST.method = 'POST'
        RQST.POST = self.data
        RQST.user = self.user
        self.response = MethodPost(RQST)

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_investmentform_instance(self):
        """
            investmentform attr must be a InvestmentForm instance.
        """
        self.assertIsInstance(self.response.i_form, InvestmentForm)

    def test_form_is_valid(self):
        self.assertTrue(self.response.i_form.is_valid())

    def test_invest_form_save(self):
        query_user = NewInvestment.objects.user_logged(self.user)
        select_data = query_user.get(pk=1)
        select_dict = dict(
            user_name=select_data.user_name,
            date=select_data.date.strftime('%Y-%m-%d'),
            tx_op=float(select_data.tx_op),
            money=float(select_data.money),
            kind=select_data.kind,
            brokerage=select_data.brokerage
        )
        self.data['user_name'] = self.user
        self.assertDictEqual(self.data, select_dict)

    def test_send_invest_post_url(self):
        self.data['kind'] = 'HERE'
        response = self.client.post(r('investments:home'), self.data)  # noqa
        self.assertEqual('HERE', NewInvestment.objects.get(pk=2).kind)
        self.assertEqual(2, NewInvestment.objects.count())


class ValidPostMethodWithDetails(TestCase):
    """ Wierd """
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

        RQST.method = 'POST'
        RQST.POST = data
        RQST.user = self.user
        self.direct = MethodPost(RQST)

        self.details = dict(
            **data,
            which_target='Details',
            segment='Details',
            tx_or_price=0.00,
            quant=0.00,
        )
        # RQST.POST = self.details
        # self.direct = MethodPost(RQST)

        self.response = self.client.post(r('investments:home'), self.details)  # noqa

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_is_valid(self):
        self.assertTrue(self.direct.i_form.is_valid())
        self.assertFalse(self.direct.d_form.is_valid())

    def test_record_in_db(self):
        self.assertTrue(NewInvestmentDetails.objects.filter(segment='Details').exists())

    def test_form_instance(self):
        self.assertTrue(isinstance(self.response.context['formd'](), InvestmentDetailsForm))
        self.assertTrue(isinstance(self.response.context['form'](), InvestmentForm))

    def test_count_records(self):
        self.assertEqual(2, NewInvestment.objects.count())
