from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.get_service import MethodGet
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails
from charcoallog.investments.post_service import MethodPost


class ShowData:
    def __init__(self, request):
        self.newinvestment = NewInvestment.objects.user_logged(request.user)
        self.newinvestmentdetails = NewInvestmentDetails.objects.user_logged(request.user)
        self.methodpost = MethodPost(request)
        self.methodget = MethodGet(request, self.newinvestment)
        self.brief_investment = BriefInvestment(
            self.newinvestment,
            self.newinvestmentdetails
        )
