import json
from decimal import Decimal

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
        self.brief_bank = BriefBank(self.query_bank)
        self.summary_categories = Summary(self.query_bank).summary_categories


class ScheduleData:
    def __init__(self, request_user):
        self.query_schedule = Schedule.objects.user_logged(request_user)

    @property
    def brief_schedule(self):
        return BriefBank(self.query_schedule)

    @property
    def schedule_json(self):
        return serialize("json", self.query_schedule.all())


class Summary:
    current_month = date.today().strftime('%Y-%m-01')

    def __init__(self, qs):
        self.month_summary = qs.summary(self.current_month)

    @property
    def summary_categories(self):
        summary = self.categories()
        return json.dumps(summary, default=serialize_decimal)

    def categories(self):
        summary = BriefBank(self.month_summary)
        return summary.account_names('category')


def serialize_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
