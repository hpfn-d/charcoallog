from collections import OrderedDict


class BriefBank:
    """
    :type query_user: queryset
    :type col_name: str
    :type account_dict: dict

    """
    def __init__(self, query_user, col_name='payment'):
        self.query_user = query_user
        self.col_name = col_name
        self.account_dict = dict()

        self.build_dict()

    def build_dict(self):
        self.account_dict = {
            account[0]: self.query_user.pay_or_cat(account[0]).total()
            for account in self.payment_iterator()
        }

    def payment_iterator(self):
        return set(self.query_user.values_list(self.col_name))

    def account_val_sorted(self):
        return OrderedDict(sorted(self.account_dict.items()))

    def whats_left(self):
        return sum([money['money__sum'] for money in self.account_dict.values()])
