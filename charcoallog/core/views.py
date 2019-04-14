from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from charcoallog.core.service import BuildHome


@login_required
def home(request):
    b_h = BuildHome(request.user)
    context = {'names': b_h.line1.account_names(),
               'wht_l': b_h.line1.whats_left,
               'brokerage': b_h.line2.brokerage,
               'investdetail': b_h.line2.kind_investmentdetail()}

    return render(request, "core/home.html", context)
