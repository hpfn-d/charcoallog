import datetime as dt
import json
import os

from django.contrib.auth.models import User

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract
from charcoallog.bank.service import Summary
# from charcoallog.core.scrap_line3_service import Scrap
from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class BuildHome:
    def __init__(self, request_user):
        self.query_bank = Extract.objects.user_logged(request_user)
        self.line1 = BriefBank(self.query_bank)
        # tabela = Scrap()
        # self.selic_info = tabela.selic_info()
        # self.ibov_info = tabela.ibov_info()
        # self.ipca_info = tabela.ipca_info()

        self.query_user_invest = NewInvestment.objects.user_logged(request_user)
        self.query_user_details = NewInvestmentDetails.objects.user_logged(request_user)
        self.line2 = BriefInvestment(self.query_user_invest, self.query_user_details)

        self.summary_categories = by_month_cat(request_user)


SUMMARY = './charcoallog/core/summary.json'


def by_month_cat(request_user):
    if os.path.isfile(SUMMARY):
        with open(SUMMARY, 'r') as fd:
            user_year_month = json.load(fd)
    else:
        user_year_month = collect_summary()

    year = dt.datetime.today().strftime("%Y")
    return user_year_month[year][str(request_user)]


def collect_summary():
    year = dt.datetime.today().strftime("%Y")

    to_json = {year: dict()}

    for who in all_users():
        w = str(who)
        all_year_month, year = year_summary(w)
        to_json[year].update({w: all_year_month})

    with open(SUMMARY, 'w') as fd:
        json.dump(to_json, fd)

    return to_json


# collect_summary helpers
def all_users():
    return (u for u in User.objects.all())


def year_summary(who):
    query_bank = Extract.objects.user_logged(who)
    summary = Summary(query_bank)
    all_year_month = []
    range_month = int(summary.month) - 1

    for m in range(range_month, 0, -1):
        wrap_year_month(query_bank, all_year_month, summary, m)

    return all_year_month, summary.year


def wrap_year_month(query_bank, all_year_month, summary, m):
    month = dt.datetime(int(summary.year), m, 1).strftime("%m")
    last = query_bank.summary(summary.year, month)
    if last:
        summary.month_summary = last
        all_year_month.append(summary.summary_categories())
