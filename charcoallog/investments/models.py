from django.db import models
from django.db.models import Q, Sum


class InvestmentStatementQuerySet(models.QuerySet):
    def user_logged(self, user_name):
        return self.filter(user_name=user_name)

    def total_money(self):
        return self.aggregate(Sum('money'))['money__sum']

    def brokerage(self):
        return self.values_list('brokerage')

    def kind(self, k='kind'):
        """
        if kind is default get all values from column
        else filter by value set by user
        """
        if k == 'kind':
            return self.values_list(k)
        else:
            return self.filter(kind=k)

    def date_range(self, from_date, to_date):
        return self.filter(date__gte=from_date, date__lte=to_date)

    def which_field(self, column):
        # ['date', 'money', 'kind', 'tx_op', 'brokerage']
        return self.filter(Q(kind=column) | Q(brokerage=column))
        # | Q(description=column))
        # .filter(~Q(category__startswith='transfer'))


class NewInvestment(models.Model):
    # corretagem
    tx_op = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    brokerage = models.CharField(max_length=15)
    user_name = models.CharField(max_length=30)
    date = models.DateField()
    money = models.DecimalField(max_digits=8, decimal_places=2)
    # Acao, Titulo Publico, CDB, FII
    kind = models.CharField(max_length=40, default='---')

    # both a custom Manager and a custom QuerySet
    # https://docs.djangoproject.com/en/1.11/topics/db/managers/#from-queryset
    # objects = models.Manager.from_queryset(InvestmentStatementQuerySet)()
    #
    # to create an instance of Manager with a copy of a custom QuerySet’s
    # https://docs.djangoproject.com/en/1.11/topics/
    # db/managers/#creating-a-manager-with-queryset-methods
    objects = InvestmentStatementQuerySet.as_manager()

    class Meta:
        ordering = ['-date']
        verbose_name = 'investments'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.brokerage


class NewInvestmentDetails(NewInvestment):
    # Qual acao, titulo publico, banco(CDB), cod FII
    which_target = models.CharField(max_length=20, default='---')
    # PN|ON, NTNB|SELIC|LTF, carencia CDB, sobre FII
    segment = models.CharField(max_length=30, default='---')
    # VALOR cada acao, taxa Tesouro, taxa CDB, valor de compra|venda FII
    tx_or_price = models.DecimalField(max_digits=8, decimal_places=2, default=00.00)
    quant = models.DecimalField(max_digits=8, decimal_places=2, default=00.00)

    objects = InvestmentStatementQuerySet.as_manager()

    class Meta:
        verbose_name = 'investment details'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.which_target
