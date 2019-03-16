from charcoallog.investments.forms import InvestmentDetailsForm


class MethodPost:
    def __init__(self, request):
        """"
        :param request: http response
        """
        self.request_post = request.POST
        self.request_user = request.user
        # self.i_form = None
        self.d_form = None

        if request.method == 'POST':
            self.method_post()

    def method_post(self):
        # self.i_form = InvestmentForm(self.request_post)
        self.d_form = InvestmentDetailsForm(self.request_post)

        if self.d_form.is_valid():
            self.d_form.save(self.request_user)
        # elif self.i_form.is_valid():
        #    self.i_form.save(self.request_user)
