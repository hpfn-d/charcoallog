from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.investments.get_service import MethodGet
from charcoallog.investments.service import ShowData


class RQST:
    pass

class ServiceTest(TestCase):
    def setUp(self):
        RQST.method = None
        RQST.POST = {}
        RQST.user = 'teste'
        self.service = ShowData(RQST)

    def test_query_set(self):
        self.assertIsInstance(self.service.query_user, QuerySet)

    def test_methodget(self):
        self.assertIsInstance(self.service.methodget, MethodGet)
