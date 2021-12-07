from django.template.loader import get_template, render_to_string
from django.shortcuts import HttpResponse
import weasyprint
from .models import *

def incomeWarehousePrint(request, pk):
    whIncome = WarehouseOperation.objects.get(pk=pk)
    wh_income_inner = WarehouseOperationInner.objects.filter(inner=whIncome)
    whIncomeRT = []

    sum_count = 0
    sum_price = 0
    sumS = 0

    for w_i in wh_income_inner:
        whIncomeRT.append({
            'id': w_i.pk,
            'name': w_i.name.title,
            'category': w_i.category.title + "(" + w_i.category.unit + ")",
            'count': w_i.sum,
            'price': w_i.price,
            'sum': w_i.sum * w_i.price
        })
        sum_count = sum_count + w_i.sum
        sum_price = sum_price + w_i.price
        sumS = sumS + w_i.sum * w_i.price

    context = {
        "id": whIncome.id,
        "date": whIncome.date,
        "warehouse": whIncome.warehouse.title,
        "sum_count": sum_count,
        "sum_price": sum_price,
        'sumS': sumS,
        "whInner": whIncomeRT,
        "added_by": whIncome.added_by.first_name + " " + whIncome.added_by.last_name,
    }

    html_string = render_to_string("warehouse/print/incomeWarehouse.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response

def movingWarehousePrint(request, pk):
    whMoving = WarehouseOperation.objects.get(pk=pk)
    wh_inner = WarehouseOperationInner.objects.filter(inner=whMoving)
    context = {
        "id": whMoving.id,
        "date": str(whMoving.date),
        "to_the_warehouse": whMoving.warehouse.title,
        "from_warehouse": whMoving.from_warehouse.title,
        "whInner": wh_inner,
    }

    html_string = render_to_string("warehouse/print/movingWarehouse.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response

def incomeWarehouseCashierPrint(request, pk):
    whIncome = WarehouseOperation.objects.get(pk=pk)
    wh_income_inner = WarehouseOperationInner.objects.filter(inner=whIncome)
    sumS = 0

    for w_i in wh_income_inner:
        sumS = sumS + w_i.sum * w_i.price

    context = {
        "id": whIncome.id,
        "date": str(whIncome.date),
        "wh_article": whIncome.wh_article.name,
        "sumS": sumS,
        "added_by": whIncome.added_by.first_name + " " + whIncome.added_by.last_name
    }
    html_string = render_to_string("warehouse/print/incomeWarehouseCashier.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response


def consumablesWarehousePrint(request, pk):
    whConsumption = WarehouseOperation.objects.get(pk=pk)
    wh_inner = WarehouseOperationInner.objects.filter(inner=whConsumption)
    context = {
        "id": whConsumption.id,
        "date": str(whConsumption.date),
        "warehouse": whConsumption.warehouse.title,
        'route': str(whConsumption.route.pk) + " - " + whConsumption.route.country_recipient.name,
        'client': whConsumption.client.fullname,
        'clientID': whConsumption.client.pk,
    }
    whConsumptionRT = []
    for w_i in wh_inner:
        whConsumptionRT.append({
            'id': w_i.pk,
            'name': w_i.name.title,
            'category': w_i.category.title + "(" + w_i.category.unit + ")",
            'count': w_i.sum,
            'price': w_i.price,
            'sum': w_i.sum * w_i.price
        })
        context['whConsumption'] = whConsumptionRT

    html_string = render_to_string("warehouse/print/consumablesWarehouse.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response