from datetime import date

from django.contrib import messages
from django.core.serializers import serialize

from charcoallog.bank.forms import SelectExtractForm


class MethodGet:
    month_01 = date.today().strftime('%Y-%m-01')

    def __init__(self, request, query_user):
        """
        :param request: request from views
        :param query_user: Extract objects from .models.py
        """
        self.request = request
        self.query_user = query_user
        self.extract_json = ''
        self.query_default = ''
        self.query_default_total = ''
        self.get_form = SelectExtractForm(self.request.GET)

        self.build_request()

    def build_request(self):
        if self.request.method == 'GET' and self.get_form.is_valid():
            self.search_from_get()
        else:
            self.query_default = self.query_user.filter(date__gte=self.month_01)
            self.query_default_total = self.query_default.total()
            self.extract_json = serialize("json", self.query_default)

    def method_get(self):
        self.get_form = SelectExtractForm(self.request.GET)

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
            self.extract_json = serialize("json", self.query_default)
        else:
            messages.error(
                self.request,
                "' %s ' - Invalid search or nothing for these dates." % column
            )
