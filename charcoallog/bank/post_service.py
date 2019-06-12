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


def treat_recurrent(data):
    todo_list = []

    # remove recurrent word
    description = data['description'].rpartition('recurrent')
    description = description[-1].strip()
    data['description'] = description

    # set remaining months
    d = data['date']
    for m in range(d.month, 13):
        recurrent = {**data}
        recurrent.update(date=dt.datetime(d.year, m, d.day))
        todo_list.append(recurrent)

    return todo_list


INSERT_TO = dict(
    to_extract=to_extract,
    to_schedule=to_schedule

)
