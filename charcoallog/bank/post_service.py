import calendar as cal
import datetime as dt

from charcoallog.bank.models import Extract, Schedule

from .forms import EditExtractForm


class MethodPost:
    def __init__(self, request):
        """
        :param request: request from views
        """
        # self.request_method = request_method
        self.request_post = request.POST
        self.request_user = request.user
        self.editextractform = EditExtractForm
        self.form = None

        if request.method == 'POST':
            self.method_post()

    def method_post(self):
        self.form = self.editextractform(self.request_post)

        if self.form.is_valid():
            self.insert_by_post()

    def insert_by_post(self):
        transfer = self.form.cleaned_data.get('category').startswith('transfer')
        schedule = self.form.cleaned_data['schedule']
        to_model = 'to_schedule' if schedule else 'to_extract'
        del self.form.cleaned_data['schedule']

        INSERT_TO[to_model](self.request_user, self.form.cleaned_data)

        if transfer:
            data_transfer = build_data_transfer(self.form.cleaned_data)
            INSERT_TO[to_model](self.request_user, data_transfer)


def build_data_transfer(form):
    return dict(
        # user_name=user,
        date=form.get('date'),
        money=form.get('money') * -1,
        category=form.get('category'),
        description='credit from ' + form.get('payment'),
        payment=form.get('description')
    )


def to_extract(user, data):
    Extract.objects.create(user_name=user, **data)


def to_schedule(user, data):
    """
    create one record in Schedule
    or
    create a record to all the remaining months of the year
    """
    todo_list = [data]
    if data['description'].startswith('recurrent'):
        todo_list = treat_recurrent(data)

    for item in todo_list:
        Schedule.objects.create(user_name=user, **item)


INSERT_TO = dict(
    to_extract=to_extract,
    to_schedule=to_schedule

)


def treat_recurrent(data):
    """
    return a list (item - dict) that contains
    next months stuff
    """
    todo_list = []
    counter, int_year, int_month, day = extract(data)

    year_limit = prev_m = 0
    for m in range(counter):
        if year_limit == 12:
            year, month = next_year(int_year, m, prev_m)
        else:
            year, year_limit, month, prev_m = current_year(int_year, int_month, m)

        rec = update_date(data, year, month, day)
        todo_list.append(rec)

    return todo_list


def extract(data):
    description = data['description'].split()
    counter = int(description[1])
    description = ''.join(description[2:])
    data['description'] = description.strip()
    d = data['date']
    return counter, int(d.year), int(d.month), d.day


def update_date(data, year, month, day):
    last_day = cal.monthrange(year, month)[1]
    if last_day < day:
        day = last_day

    recurrent = {**data}
    recurrent.update(date=dt.datetime(year, month, day))
    return recurrent


def next_year(int_year, m, prev_m):
    year = int_year + 1
    month = m - prev_m
    return year, month


def current_year(int_year, int_month, m):
    year = int_year
    year_limit = month = int_month + m
    # prev_m = m
    return year, year_limit, month, m
