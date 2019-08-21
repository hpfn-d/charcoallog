import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.models import NewInvestmentDetails
from charcoallog.investments.views import inheritance_serializer, kind_quant


class InvestmentDetailTest(TestCase):
    def setUp(self):
        user_n = 'teste'
        user = User.objects.create(username=user_n)
        user.set_password('1qa2ws3ed')
        user.save()

        self.date = '2018-03-27'
        self.money = '94.42'
        self.kind = 'Títulos Públicos'
        # self.which_target = 'Tesouro Direto'

        self.login_in = self.client.login(username=user_n, password='1qa2ws3ed')

        self.which_target = 'Tesouro Direto'
        self.segment = 'Selic'
        self.tx_or_price = '0.01'
        self.quant = '1.00'

        self.data = dict(
            user_name=user_n,
            date=self.date,
            money=self.money,
            kind=self.kind,
            which_target=self.which_target,
            segment=self.segment,
            tx_or_price=self.tx_or_price,
            quant=self.quant,
        )

        self.obj = NewInvestmentDetails.objects.create(**self.data)
        self.resp = self.client.get(r('investments:details', 'Títulos Públicos'))

    def test_login(self):
        """ Must login to access html file"""
        self.assertTrue(self.login_in)

    def test_get_status_code(self):
        """ Must return status code 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'investments/details/newinvestmentdetails_detail.html')

    def test_db_record_exists(self):
        qs = NewInvestmentDetails.objects.filter(pk=1)
        self.assertTrue(qs.exists())

    def test_instances(self):
        expected = [
            # (self.resp.context['form'], InvestmentDetailsForm),
            (self.resp.context['newinvestmentdetails'], str),
            (self.resp.context['w_target'], dict),
            # (self.resp.context['quant'], dict)
        ]

        for e, cls in expected:
            with self.subTest():
                self.assertIsInstance(e, cls)

    def test_html(self):
        """
        Must contain input tags
        vue template does not count
        """
        expected = [
            ('<form', 1),
            ('<input', 3),  # search form
            # ("type='hidden'", 1),
            ('type="text"', 1),
            # ('type="number"', 2),
            # ('step="0.01"', 1),
            ('type="date"', 2),
            ('type="submit"', 1),
            ('</form>', 1),
            ('class="row', 5),
            ('method="get"', 1),
            # ('method="post"', 1),
            ('id="vue_ajax_detail"', 1),
        ]
        for tag, x in expected:
            with self.subTest():
                self.assertContains(self.resp, tag, x)

    # inside vue template
    # def test_csrf(self):
    #    """ html must contain csrf """
    #    self.assertContains(self.resp, 'csrfmiddlewaretoken', 1)

    # test above
    # def test_context_instance(self):
    #    form3 = self.resp.context['newinvestmentdetails']
    #    self.assertIsInstance(form3, QuerySet)

    def test_context(self):
        data = self.resp.context['newinvestmentdetails']
        data = json.loads(data)
        # del data['pk']

        expected = [
            self.date, str(Decimal(self.money)), self.kind, self.which_target,
            self.segment, str(Decimal(self.tx_or_price)), self.quant
        ]

        for v in data[0]['fields'].values():
            with self.subTest():
                self.assertIn(v, expected)

    def test_inheritance_serializer(self):
        k_json = inheritance_serializer('teste', self.kind)

        self.assertEqual(k_json,
                         [
                             {
                                 'pk': 1,
                                 'fields': {
                                     'date': '2018-03-27',
                                     'money': '94.42',
                                     'kind': 'Títulos Públicos',
                                     'which_target': 'Tesouro Direto',
                                     'segment': 'Selic',
                                     'tx_or_price': '0.01',
                                     'quant': '1.00'
                                 }
                             }
                         ]
                         )

    def test_item_quant(self):
        """ show quantity of each investment in details page """
        data = dict(
            user_name='teste',
            date=self.date,
            money=self.money,
            kind='FAKE',
            which_target='ORUIM',
            segment=self.segment,
            tx_or_price=self.tx_or_price,
            quant=35,
        )

        NewInvestmentDetails.objects.create(**data)
        data['quant'] = 15
        NewInvestmentDetails.objects.create(**data)
        data['kind'] = 'Third'
        data['which_target'] = 't'
        data['quant'] = 15
        NewInvestmentDetails.objects.create(**data)
        NewInvestmentDetails.objects.create(**data)
        NewInvestmentDetails.objects.create(**data)
        data['which_target'] = 't_2'
        data['quant'] = 15
        NewInvestmentDetails.objects.create(**data)
        data['which_target'] = 't_3'
        data['quant'] = 20
        NewInvestmentDetails.objects.create(**data)
        NewInvestmentDetails.objects.create(**data)
        NewInvestmentDetails.objects.create(**data)
        NewInvestmentDetails.objects.create(**data)

        self.assertEqual(NewInvestmentDetails.objects.all().count(), 11)

        expected = [
            (self.kind, self.which_target, 1),
            ('FAKE', 'ORUIM', 50),
            ('Third', 't', 45),
            ('Third', 't_2', 15),
            ('Third', 't_3', 80),

        ]

        for k, v, q in expected:
            quant, _ = kind_quant('teste', k)
            self.assertEqual(quant[v], q)

        for x in range(2, 12):
            NewInvestmentDetails.objects.get(pk=x).delete()
