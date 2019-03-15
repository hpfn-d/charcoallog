from django.test import TestCase

from charcoallog.investments.forms import InvestmentForm, InvestmentSearchForm


class InvestmentFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 2 fields. The third field is in test_basicdata_form"""
        form = InvestmentForm()
        self.assertSequenceEqual(
            ['date', 'money', 'kind', 'tx_op', 'brokerage'],
            list(form.fields)
        )


class InvestmentSearchFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 3 fields. The third field is in test_basicdata_form"""
        form = InvestmentSearchForm()
        self.assertSequenceEqual(
            ['column', 'from_date', 'to_date'],
            list(form.fields)
        )
