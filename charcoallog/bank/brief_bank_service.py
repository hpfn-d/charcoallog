from collections import OrderedDict


class BriefBank:
    """
    :type account_values: dictionary views
          dict.values()
    """

    def __init__(self, query_user):
        self.query_user = query_user
        self.account_values = None

    def account_names(self, col_type='payment'):
        payment_iterator = set(self.query_user.values_list(col_type))

        account = {
            conta[0]: filter_dict[col_type](self.query_user, conta[0])
            for conta in payment_iterator
        }

        self.account_values = account.values()

        return OrderedDict(sorted(account.items()))

    def whats_left(self):
        return sum([resto['money__sum'] for resto in self.account_values])


def payment(qs, vl):
    return qs.filter(payment=vl).total()


def category(qs, vl):
    return qs.filter(category=vl).total()


filter_dict = dict(
    payment=payment,
    category=category
)
