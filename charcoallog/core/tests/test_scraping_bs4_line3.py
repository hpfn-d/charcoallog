# from bs4 import BeautifulSoup
from django.test import TestCase
from charcoallog.core.scrap_line3_service import Scrap


class ScrapTest(TestCase):
    def setUp(self):
        self.context = Scrap()

    def test_selic_info_type(self):
        self.assertIsInstance(self.context.selic_info(), type(dict()))

    def test_ibov_info_type(self):
        self.assertIsInstance(self.context.ibov_info(), type(dict()))

    def test_ipca_info_type(self):
        self.assertIsInstance(self.context.ipca_info(), type(dict()))

