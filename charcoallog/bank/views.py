# import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render  # Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract, Schedule
from charcoallog.bank.serializers import ExtractSerializer, ScheduleSerializer

from .service import ShowData


@login_required
def home(request):
    show_data = ShowData(request)

    context = {
        'show_data': show_data,
        'schedule': show_data.schedule_json,
        'extract': show_data.extract_json,
        'summary': show_data.summary_categories,
    }
    return render(request, "bank/home.html", context)


class PkDoesNotExits(Exception):
    pass


class HomeApi(LoginRequiredMixin, APIView):
    raise_exception = True

    def get_object(self, pk):
        try:
            return Extract.objects.get(pk=pk)
        except Extract.DoesNotExist:
            raise PkDoesNotExits('The "pk" {} does not exists Extract db'.format(pk))
            # raise Http404

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


class ScheduleApi(LoginRequiredMixin, APIView):
    raise_exception = True

    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise PkDoesNotExits('The "pk" {} does not exists in Schedule db'.format(pk))

    # def get(self, request, pk, format=None):

    #     investment = self.get_object(pk)
    #     serializer = InvestmentSerializer(investment)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        bill = self.get_object(pk)
        serializer = ScheduleSerializer(bill, data=request.data)
        if serializer.is_valid():
            serializer.update(bill, serializer.validated_data)
            schdl = Schedule.objects.user_logged(request.user)
            schdl = build_json_data(schdl)
            return Response(schdl)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bill = self.get_object(pk)
        bill.delete()
        # delete returns nothing. Do the math by Vue
        return Response(status=status.HTTP_204_NO_CONTENT)


def build_json_data(query_user):
    line1 = BriefBank(query_user)
    return {"accounts": line1.account_names(),
            "whats_left": line1.whats_left()}
