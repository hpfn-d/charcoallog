from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.bank.service import ShowData


class HomeContextTest(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.login_in = self.client.login(username='test', password='1qa2ws3ed')
        self.response = self.client.get(r('bank:home'))  # ('/bank/')

    def test_status_code(self):
        """ status code must be 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'bank/home.html')

    def test_showdata_instance(self):
        show_data = self.response.context['show_data']
        self.assertIsInstance(show_data, ShowData)

    def test_schedule_type(self):
        schedule = self.response.context['schedule']
        self.assertIsInstance(schedule, str)

    def test_extract_type(self):
        extract = self.response.context['extract']
        self.assertIsInstance(extract, str)

    def test_summary_type(self):
        summary = self.response.context['summary']
        self.assertIsInstance(summary, str)

    def test_number_of_href(self):
        self.assertContains(self.response, '<a href', 4)

    def test_html_forms_initial(self):
        """" Html must contain input tags at first time """
        tags = (
            ('<form', 2),
            ('<input', 10),
            ('<select', 0),
            ('type="text"', 4),
            ('type="number"', 1),
            ('step="0.01"', 1),
            ('<button', 3),
            ('type="submit"', 2),
            ('<summary-tpl', 1),
            ('<all-reg-forms', 3)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """" must have csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken', 2)

    def test_total_line3(self):
        self.assertContains(self.response, '')

    def test_whats_left(self):
        """
            Whats left must be zero at first time
            check line1.account_names
        """
        zero = self.response.context['show_data']
        self.assertEqual(zero.brief_bank.whats_left(), 0)

    def test_bottom_id(self):
        self.assertContains(self.response, 'Charcoallog License - GPL-3+')
