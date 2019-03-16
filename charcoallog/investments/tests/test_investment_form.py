from django.test import TestCase

from charcoallog.investments.forms import (
    InvestmentDetailsForm, InvestmentForm, InvestmentSearchForm
)


class InvestmentFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 2 fields. The third field is in test_basicdata_form"""
        form = InvestmentForm()
        self.assertSequenceEqual(
            ['date', 'money', 'kind', 'tx_op', 'brokerage'],
            list(form.fields)
        )

    def test_attr_save(self):
        self.assertTrue(hasattr(InvestmentForm, 'save'))


class InvestmentDetailsFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 2 fields. The third field is in test_basicdata_form"""
        form = InvestmentDetailsForm()
        fields = [
            'date', 'money', 'kind', 'tx_op',
            'brokerage', 'which_target', 'segment',
            'tx_or_price', 'quant'
        ]

        self.assertSequenceEqual(fields, list(form.fields))

    def test_attr_save(self):
        self.assertTrue(hasattr(InvestmentDetailsForm, 'save'))


class InvestmentSearchFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 3 fields. The third field is in test_basicdata_form"""
        form = InvestmentSearchForm()
        self.assertSequenceEqual(
            ['column', 'from_date', 'to_date'],
            list(form.fields)
        )
