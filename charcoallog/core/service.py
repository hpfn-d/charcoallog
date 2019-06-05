import datetime as dt

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract
from charcoallog.bank.service import Summary
from charcoallog.core.scrap_line3_service import Scrap
from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class BuildHome:
    def __init__(self, request_user):
        self.query_bank = Extract.objects.user_logged(request_user)
        self.line1 = BriefBank(self.query_bank)
        tabela = Scrap()
        self.selic_info = tabela.selic_info()
        self.ibov_info = tabela.ibov_info()
        self.ipca_info = tabela.ipca_info()

        self.query_user_invest = NewInvestment.objects.user_logged(request_user)
        self.query_user_details = NewInvestmentDetails.objects.user_logged(request_user)
        self.line2 = BriefInvestment(self.query_user_invest, self.query_user_details)

        self.summary_categories = self.by_month_cat()

    def by_month_cat(self):
        summary = Summary(self.query_bank)
        all_year_month = []
        range_month = int(summary.month) + 1
        for m in range(1, range_month):
            month = dt.datetime(int(summary.year), m, 1).strftime("%m")

            last = self.query_bank.summary('2019', month)
            summary.month_summary = last
            all_year_month.append(summary.summary_categories)

        # json.dumps to a file
        #  do like Scrap class for ibov, selic, ipca
        return reversed(all_year_month)
