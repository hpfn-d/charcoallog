# import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import JsonResponse
from django.shortcuts import Http404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from charcoallog.bank.brief_bank_service import BriefBank
# from charcoallog.bank.forms import EditExtractForm
from charcoallog.bank.models import Extract, Schedule
from charcoallog.bank.serializers import ExtractSerializer

from .service import ShowData


@login_required
def home(request):
    # user_logged instead of a .filter()
    context = {
        'show_data': ShowData(request),
        'schedule': Schedule.objects.user_logged(request.user).all(),
    }
    return render(request, "bank/home.html", context)


class HomeApi(LoginRequiredMixin, APIView):
    raise_exception = True

    def get_object(self, pk):
        try:
            return Extract.objects.get(pk=pk)
        except Extract.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     investment = self.get_object(pk)
    #     serializer = InvestmentSerializer(investment)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        bill = self.get_object(pk)
        serializer = ExtractSerializer(bill, data=request.data)
        if serializer.is_valid():
            serializer.update(bill, serializer.validated_data)
            extract = Extract.objects.user_logged(request.user)
            line1_data = build_json_data(extract)
            return Response(line1_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bill = self.get_object(pk)
        bill.delete()
        # delete returns nothing. Do the math by Vue
        return Response(status=status.HTTP_204_NO_CONTENT)


# @login_required
# def update(request):
#     data = {"js_alert": True, "message": 'Not a valid request'}
#
#     if request.is_ajax() and request.method == 'PUT':
#         # decode utf-8 not needed
#         form_data = form_data_from_body(request.body)
#         form = EditExtractForm(form_data)
#
#         if form.is_valid():
#             extract = Extract.objects.user_logged(request.user)
#             update_db(form_data['pk'], form.cleaned_data, extract, request.user)
#             data = build_json_data(extract)
#         else:
#             data = {"js_alert": True, "message": 'Form is not valid'}
#
#     return JsonResponse(data)


# @login_required
# def delete(request):
#     extract = Extract.objects.user_logged(request.user)
#     if request.is_ajax() and request.method == 'DELETE':
#         # body = request.body.decode('utf-8')
#         form_data = form_data_from_body(request.body)
#         pk = form_data['pk']
#         extract.filter(pk=pk).delete()
#
#     data = build_json_data(extract)
#
#     return JsonResponse(data)


# helpers for update and delete views
# def form_data_from_body(request_body):
#     body = request_body.decode('utf-8')
#     return json.loads(body)


def build_json_data(query_user):
    line1 = BriefBank(query_user)
    return {"accounts": line1.account_names(),
            "whats_left": line1.whats_left()}


# Not used
# def new_account(form_data, query_user):
#    payment = form_data.get('payment')
#    if not query_user.filter(payment=payment).first():
#        return {"js_alert": True,
#                "message": 'You can not set a new account name from here'}
#    return None


# def update_db(pk, form_cleaned_data, query_user, request_user):
#     obj = query_user.get(id=pk)
#     form = EditExtractForm(form_cleaned_data, instance=obj)
#     form.save(request_user)
