import json
from _decimal import Decimal

from django.core.serializers import serialize
from django.utils.datetime_safe import date

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.get_service import MethodGet
from charcoallog.bank.models import Extract, Schedule
from charcoallog.bank.post_service import MethodPost


class ShowData:
    def __init__(self, request):
        self.query_bank = Extract.objects.user_logged(request.user)
        self.form1 = MethodPost(request, self.query_bank)

        self.form2 = MethodGet(request, self.query_bank)
        self.extract_json = serialize("json", self.form2.query_default)

        self.brief_bank = BriefBank(self.query_bank)

        self.query_schedule = Schedule.objects.user_logged(request.user)
        self.schedule_json = serialize("json", self.query_schedule.all())

        self.brief_schedule = BriefBank(self.query_schedule)
        self.summary_categories = summary_json(self.query_bank)


def summary_json(bank_qs):
    current_month = date.today().strftime('%Y-%m-01')
    query_summary = bank_qs.summary(current_month)
    summary = BriefBank(query_summary)
    return json.dumps(summary.account_names('category'), default=serialize_decimal)


def serialize_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
