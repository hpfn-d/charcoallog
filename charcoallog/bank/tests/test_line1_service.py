from decimal import Decimal

from django.test import TestCase

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract


class BriefBankTest(TestCase):
    fixtures = ['extract_data.json']

    def setUp(self):
        query_user = Extract.objects.user_logged('test')
        self.response = BriefBank(query_user)
        self.brief_bank_account_name = self.response.account_val_sorted()

    def test_line1_account_names(self):
        self.assertIn('principal', self.brief_bank_account_name)

    def test_line1_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
            line1.account_names must be called before whats_left
            (account_values)
        """
        self.assertEqual(self.response.whats_left(), Decimal('10.00'))
