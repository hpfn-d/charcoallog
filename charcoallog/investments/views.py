import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from charcoallog.investments.detail_post_service import DetailPost
from charcoallog.investments.forms import (
    InvestmentDetailsForm, InvestmentSearchForm
)
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails
from charcoallog.investments.serializers import (
    InvestmentDetailsSerializer, InvestmentSerializer
)
from charcoallog.investments.service import ShowData


@login_required
def home(request):
    show_data = ShowData(request)

    context = {
        'd_form': InvestmentDetailsForm(),
        'form2': InvestmentSearchForm(),
        'show_data': show_data,
        'extract': show_data.methodget.extract_json,
    }

    return render(request, 'investments/home.html', context)


# @api_view
@login_required
def newinvestmetdetails_detail(request, kind):
    # post = DetailPost(request)  # noqa F841
    w_target_quant, kind_qs = kind_quant(request.user, kind)

    context = {
        'w_target': w_target_quant,
        'newinvestmentdetails': json.dumps(kind_qs),
        # 'form': InvestmentDetailsForm()
    }
    return render(request, 'investments/details/newinvestmentdetails_detail.html', context)


class HomeApi(LoginRequiredMixin, APIView):
    raise_exception = True

    def get_object(self, pk):
        try:
            return NewInvestment.objects.get(pk=pk)
        except NewInvestment.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     investment = self.get_object(pk)
    #     serializer = InvestmentSerializer(investment)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        investment = self.get_object(pk)
        serializer = InvestmentSerializer(investment, data=request.data)
        if serializer.is_valid():
            serializer.update(investment, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        investment = self.get_object(pk)
        investment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API for details here
class DetailApi(LoginRequiredMixin, APIView):
    raise_exception = True

    def get_object(self, pk):
        try:
            return NewInvestmentDetails.objects.get(pk=pk)
        except NewInvestmentDetails.DoesNotExist:
            raise Http404

        # def get(self, request, pk, format=None):
        #     investment = self.get_object(pk)
        #     serializer = InvestmentSerializer(investment)
        #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        investment_d = self.get_object(pk)
        serializer = InvestmentDetailsSerializer(investment_d, data=request.data)
        if serializer.is_valid():
            serializer.update(investment_d, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        investment_d = self.get_object(pk)
        investment_d.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# HELPERS
def inheritance_serializer(request_user, kind):
    qs_kind_details = NewInvestmentDetails.objects.user_logged(request_user).kind(kind)
    all_model = [
        {
            'pk': i.pk,
            'fields': {
                'date': i.date.strftime("%Y-%m-%d"),
                'money': str(i.money),
                'kind': i.kind,
                'which_target': i.which_target,
                'segment': i.segment,
                'tx_or_price': str(i.tx_or_price),
                'quant': str(i.quant)}
        }

        for i in qs_kind_details]

    return all_model


def kind_quant(u, k):
    kind_json = inheritance_serializer(u, k)
    choosen_one = dict()

    for q in kind_json:
        k = q['fields']['which_target']
        v = float(q['fields']['quant'])

        if not choosen_one.get(k, 0):
            choosen_one[k] = v
        else:
            choosen_one[k] += v

    # w_t = NewInvestmentDetails.objects.user_logged(u).filter(kind=k).values_list('which_target')
    # w_t = set(w_t)
    # choosen_one = {
    #     x[0]: NewInvestmentDetails.objects.user_logged(u).filter(
    #         which_target=x[0]).aggregate(Sum('quant'))['quant__sum']
    #     for x in w_t
    # }

    return choosen_one, kind_json
