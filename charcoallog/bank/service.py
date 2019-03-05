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
        self.query_schedule = Schedule.objects.user_logged(request.user)
        self.brief_schedule = BriefBank(self.query_schedule)
