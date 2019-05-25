from django import forms

from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class InvestmentForm(forms.ModelForm):
    """ Pode passar o argumento 'label'"""

    class Meta:
        model = NewInvestment
        fields = ['date', 'money', 'kind', 'tx_op', 'brokerage']

    def save(self, user, commit=True):
        form = super(InvestmentForm, self).save(commit=False)
        form.user_name = user

        if commit:
            form.save()

        return form


class InvestmentDetailsForm(forms.ModelForm):
    class Meta:
        model = NewInvestmentDetails
        fields = [
            'date', 'money', 'kind', 'tx_op',
            'brokerage', 'which_target', 'segment',
            'tx_or_price', 'quant'
        ]

    def save(self, user, commit=True):
        form = super(InvestmentDetailsForm, self).save(commit=False)
        form.user_name = user

        if commit:
            form.save()

        return form


class InvestmentSearchForm(forms.Form):
    """ Specific Columm """
    column = forms.CharField(max_length=70, required=True)
    from_date = forms.DateField(required=True)
    to_date = forms.DateField(required=True)
