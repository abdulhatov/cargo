from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render
import weasyprint

from route.models import Currency
from .models import *
from django.db.models import Sum
from django.views.generic import TemplateView


def incomePrint(request, pk):
    obj = IncomeDebits.objects.get(pk=pk)
    obj_inner = IncomeDebitsInner.objects.filter(inner=obj)
    context = {'obj': obj, 'obj_inner': obj_inner}

    html_string = render_to_string("debits/print/income.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                    presentational_hints=True)
    return response

def incomePrint2(request, pk):
    obj = IncomeDebits.objects.get(pk=pk)
    obj_inner = IncomeDebitsInner.objects.filter(inner=obj)
    context = {'obj': obj, 'obj_inner': obj_inner}

    html_string = render_to_string("debits/print/income2.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                    presentational_hints=True)
    return response