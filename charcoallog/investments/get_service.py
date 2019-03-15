from datetime import date

from django.contrib import messages

from charcoallog.investments.forms import InvestmentSearchForm


class MethodGet:
    def __init__(self, request, query_user):
        """
        :param query_user: Investment objects from ..models.py
        """
        self.month_01 = date.today().strftime('%Y-%m-01')
        self.query_user = query_user
        self.query_default = self.query_user.filter(date__gte=self.month_01)
        self.get_form = None
        self.request = request

        if request.method == "GET":
            self.method_get()

    def method_get(self):
        self.get_form = InvestmentSearchForm(self.request.GET)

        if self.get_form.is_valid():
            self.search_from_get()

    def search_from_get(self):
        column = self.get_form.cleaned_data.get('column')
        from_date = self.get_form.cleaned_data.get('from_date')
        to_date = self.get_form.cleaned_data.get('to_date')

        if column.lower() == 'all':
            bills = self.query_user.date_range(from_date, to_date)
        else:
            bills = self.query_user.date_range(from_date, to_date).which_field(column)

        if bills.exists():
            self.query_default = bills
        else:
            self.query_default = None
            messages.error(
                self.request,
                "' %s ' - Invalid search or nothing for these dates." % column
            )
