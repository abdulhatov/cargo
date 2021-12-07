from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render
import weasyprint

from route.models import Currency
from .models import *
from django.db.models import Sum
from django.views.generic import TemplateView


class IncomePrint(TemplateView):
    template_name = 'financial/print/income.html'

    def get(self, request, *args, **kwargs):
        obj = Operations.objects.get(pk=kwargs['pk'])
        obj_inner = OperationsInner.objects.filter(inner=obj)
        context = {'obj': obj, 'obj_inner': obj_inner}

        html_string = render_to_string("financial/print/income.html", context)
        response = HttpResponse(content_type='application/pdf')
        weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
        return response

def consEmployee_print(request, pk):
    obj = Operations.objects.get(pk=pk)
    obj_inner = OperationsInner.objects.filter(inner=obj)


    context = {'obj': obj, 'obj_inner': obj_inner}

    html_string = render_to_string("financial/print/cons_employee.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                            presentational_hints=True)
    return response

def consAgent_print(request, pk):
    obj = Operations.objects.get(pk=pk)
    obj_inner = OperationsInner.objects.filter(inner=obj)
    sum = obj_inner.aggregate(Sum('sum'))['sum__sum']

    context = {'obj': obj, 'obj_inner': obj_inner, 'sum': sum}

    html_string = render_to_string("financial/print/cons_agent.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                            presentational_hints=True)
    return response

def consAgentClient_print(request, pk):
    obj = Operations.objects.get(pk=pk)
    obj_inner = OperationsInner.objects.filter(inner=obj)
    sum = obj_inner.aggregate(Sum('sum'))['sum__sum']

    context = {'obj': obj, 'obj_inner': obj_inner, 'sum': sum}

    html_string = render_to_string("financial/print/cons_agent_client.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                            presentational_hints=True)
    return response

def consVarious_print(request, pk):
    obj = Operations.objects.get(pk=pk)
    obj_inner = OperationsInner.objects.filter(inner=obj)
    sum = obj_inner.aggregate(Sum('sum'))['sum__sum']

    context = {'obj': obj, 'obj_inner': obj_inner, 'sum': sum}

    html_string = render_to_string("financial/print/cons_various.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                            presentational_hints=True)
    return response

def psEmployee_print(request, pk):
    obj = Operations.objects.get(pk=pk)
    obj_inner = OperationsInner.objects.filter(inner=obj)
    sum = obj_inner.aggregate(Sum('sum'))['sum__sum']

    context = {'obj': obj, 'obj_inner': obj_inner, 'sum': sum}

    html_string = render_to_string("financial/print/ps_employee.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                            presentational_hints=True)
    return response

def psAgent_print(request, pk):
    obj = Operations.objects.get(pk=pk)
    obj_inner = OperationsInner.objects.filter(inner=obj)
    sum = obj_inner.aggregate(Sum('sum'))['sum__sum']

    context = {'obj': obj, 'obj_inner': obj_inner, 'sum': sum}

    html_string = render_to_string("financial/print/ps_agent.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                            presentational_hints=True)
    return response

def consCashMoving_print(request, pk):
    obj = Operations.objects.get(pk=pk)

    html_string = render_to_string("financial/print/various_moving.html", {'obj': obj})
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                            presentational_hints=True)
    return response

def printSalaryID(request, pk):
    context = {}
    salary = Salary.objects.get(pk=pk)
    context["salary"] = salary
    context["currency"] = SalaryCurrency.objects.filter(salary=salary)
    context["inner"] = SalaryInner.objects.filter(salary=salary)

    html_string = render_to_string("financial/print/salary_id.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                         presentational_hints=True)
    return response

def printCashBoxes(request):

    currency = Currency.objects.all()
    cashbox = CashBox.objects.all()

    header = []
    for c in currency:
        header.append(c.name)

    dict = {}
    for c in cashbox:
        l = {}
        for curr in currency:
            l[curr.name] = 0
        dict[c.name] = l

    obj = OperationsInner.objects.all()
    for ob in obj:
        if ob.inner.type == 1:
            dict[ob.inner.cash.name][ob.inner.currency.name] += ob.sum

        elif ob.inner.type in [2, 3]:
            dict[ob.inner.cash.name][ob.inner.currency.name] -= ob.sum

        elif ob.inner.type == 4:
            dict[ob.inner.cash.name][ob.inner.currency.name] += ob.sum
            dict[ob.inner.cash_sender.name][ob.inner.currency.name] -= ob.sum


    html_string = render_to_string("financial/print/cash_boxes.html", {'header': header,'dict': dict})
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                         presentational_hints=True)
    return response
