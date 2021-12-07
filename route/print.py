import weasyprint
from collections import Counter
from .forms import *
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.template.loader import get_template, render_to_string
from .views import chunk_dict
from django.db.models import Sum
from .filters import *
from django.core.exceptions import ObjectDoesNotExist
from debits.models import ClientContrAgents

def export_to_pdf(request, pk):
    recTran = ReceptionTransmission.objects.get(pk=pk)
    services = []
    currency_Som = recTran.route.currency_Som
    currency_recipient = recTran.route.currency_recipient.name
    TotalPayable = 0
    remainder = 0
    servicesRT = Services.objects.filter(id_REC_TRAN=recTran)
    for s in servicesRT:
        sumPriceIV = s.priceIV * s.count
        sumPriceSom = s.priceIV * currency_Som * s.count
        status = ''
        if s.status:
            TotalPayable += sumPriceSom
            status = 'опл'
        else:
            remainder += sumPriceIV

        services.append({'service': s.get_service_display(),
                         'count': s.count,
                         'priceIV': s.priceIV,
                         'priceSom': round(s.priceIV * currency_Som, 3),
                         'SumPriceIV': round(sumPriceIV, 3),
                         'SumPriceSom': round(sumPriceSom, 3),
                         'status': status,
                         })

    products = ProductP.objects.filter(recTranID=pk)

    SumCount = 0
    SumWeight = 0
    bag_number = []
    for p in products:
        bag_number.append(p.bag_number)
        SumCount += p.count
        SumWeight += p.weight

    context = {'recTran': recTran,
               'products': products,
               'services': services,
               'TotalPayable': round(TotalPayable, 4),
               'remainder': round(remainder, 4),
               'currency_recipient': currency_recipient,
               'CounterBagNumber': len(Counter(bag_number)),
               'SumCount': SumCount,
               'SumWeight': SumWeight,
               'sender': recTran.sender.fullname,
               'operator': recTran.operator.first_name + " " + recTran.operator.last_name,
               'recTranID': pk
               }

    html_string = render_to_string("route/pdf/recTran.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                         presentational_hints=True)
    return response

def printRouteID(request, pk):
    route = Route.objects.get(pk=pk)
    RT = ReceptionTransmission.objects.filter(route=route)
    RTReturn = []
    for rt in RT:
        products = ProductP.objects.filter(recTranID=rt.pk)
        SumCount = 0
        SumWeight = 0
        bag_number = []
        for p in products:
            bag_number.append(p.bag_number)
            SumCount += p.count
            SumWeight += p.weight

        remainder = 0
        servicesRT = Services.objects.filter(id_REC_TRAN=rt)
        for s in servicesRT:
            sumPriceIV = s.priceIV * s.count
            if s.status == False:
                remainder += sumPriceIV

        RTReturn.append({
            'products': products,
            'recTran': rt,
            'CounterBagNumber': len(Counter(bag_number)),
            'SumCount': SumCount,
            'SumWeight': SumWeight,
            'remainder': remainder,
        })

    context = {
        'RT': RTReturn,
        'routeInf': "№"+str(pk)+' '+str(route.date.date())+' ('+route.country_recipient.name+')'}

    html_string = render_to_string("route/pdf/routeID.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                         presentational_hints=True)
    return response

def printRouteBagReportOld(request, pk):
    route = Route.objects.get(pk=pk)
    RT = ReceptionTransmission.objects.filter(history=False, route=route)
    dict = {}

    for rt in RT:
        products = ProductP.objects.filter(recTranID=rt)
        for p in products:
            if p.bag_number in dict:
                dict[p.bag_number][0] = dict[p.bag_number][0] + p.weight
            else:
                dict[p.bag_number] = [p.weight, rt.recipient.pk]

    context = {'list': list(chunk_dict(dict, 12)),
               'routeID': pk,
               'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name
                           + ') ' + str(route.date.date())}

    html_string = render_to_string("route/pdf/route_bag_report_old.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response

def printRouteBagReport(request, pk):
    route = Route.objects.get(pk=pk)
    RT = ReceptionTransmission.objects.filter(history=False, route=route)
    dict = {}

    for rt in RT:
        products = ProductP.objects.filter(recTranID=rt)
        for p in products:
            key = rt.recipient.pk
            if key in dict:
                dict[key][1] = dict[key][1] + p.weight
                if str(p.bag_number) not in dict[key][0]:
                    dict[key][0].append(str(p.bag_number))
            else:
                dict[key] = [[str(p.bag_number)], p.weight, 0]

    remainder = 0
    weight_sum = 0

    for k in dict:
        dict[k][2] = len(dict[k][0])
        remainder = remainder + dict[k][2]

        dict[k][0] = ", ".join(dict[k][0])
        weight_sum = weight_sum + dict[k][1]

    context = {'dict': dict, 'remainder': remainder, "weight_sum": weight_sum, 'routeID': pk,
                   'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name + ') ' +
                               str(route.date.date())}

    html_string = render_to_string("route/pdf/route_bag_report.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response


def printRouteNumberOfPlaces(request, pk):
    route = Route.objects.get(pk=pk)
    RT = ReceptionTransmission.objects.filter(history=False, route=route)
    dict = {}
    for rt in RT:
        key = rt.recipient.pk
        product = ProductP.objects.filter(recTranID=rt)
        w = 0
        bag_num = []
        for p in product:
            w = w + p.weight
            if p.bag_number not in bag_num:
                bag_num.append(p.bag_number)

        if key in dict:
            dict[key][4] = dict[key][4] + len(bag_num)
            dict[key][5] = dict[key][5] + w
            dict[key][6] = dict[key][6] + rt.remainder
        else:
            dict[key] = [rt.recipient.fullname, rt.recipient.store, rt.recipient.container,
                         rt.recipient.row, len(bag_num), w, rt.remainder, '', 0.0]

    NumOfP = NumberOfPlaces.objects.filter(route=route)

    for ob in NumOfP:
        key = ob.recipient.pk
        if key in dict:
            dict[key][7] = ob.agent.fullname
            dict[key][8] = ob.unloading
    iter = 1
    for key in dict:
        dict[key].insert(0, key)
        dict[key].insert(0, iter)
        iter = iter + 1

    context = {"obj": dict, 'routeID': pk,
            'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name + ') ' + str(route.date.date())}

    html_string = render_to_string("route/pdf/route_number_of_places.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response

def printRouteNumberOfPlacesAgent(request, pk):
    route = Route.objects.get(pk=pk)
    obj = NumberOfPlaces.objects.filter(route=route)
    dict = {}
    for ob in obj:
        key = ob.agent.pk
        if key in dict:
            dict[key].append(ob.recipient)
        else:
            dict[key] = [ob.recipient]

    Ret = []
    iter = 0

    for key in dict:
        agent = ClientContrAgents.objects.get(pk=key)
        k1 = "(" + str(agent.pk) + ") " + agent.fullname
        agent_rec_l = {}
        agent_rec_l[k1] = []
        for i in dict[key]:
            rec_p = ProductP.objects.filter(recTranID__history=False,
                                            recTranID__route__idRoute=pk,
                                            recTranID__recipient=i)
            bag_num = []
            for rp in rec_p:
                if rp.bag_number not in bag_num:
                    bag_num.append(rp.bag_number)

            w = rec_p.aggregate(Sum('weight'))["weight__sum"]
            c = rec_p.aggregate(Sum('count'))["count__sum"]

            agent_rec_l[k1].append([iter, i.pk, i.fullname,
                                    i.store, i.container, i.row, len(bag_num), w, c])
            iter = iter + 1

        Ret.append(agent_rec_l)

    context = {"Ret": Ret, 'routeID': pk,
            'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name + ') ' + str(route.date.date())}
    html_string = render_to_string("route/pdf/route_num_places_agent.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response

def printRouteCountProducts(request, pk):
    route = Route.objects.get(pk=pk)
    RT = ReceptionTransmission.objects.filter(history=False, route=route)
    dict = {}

    for rt in RT:
        products = ProductP.objects.filter(recTranID=rt)
        for p in products:
            key = p.product.pk
            if key in dict:
                dict[key][3] = dict[key][3] + p.count
                dict[key][4] = dict[key][4] + p.weight

                if p.bag_number not in dict[key][5]:
                    dict[key][5].append(p.bag_number)
            else:
                dict[key] = [0, p.product.name, p.product.code, p.count, p.weight, [p.bag_number]]

    count_sum = 0
    weight_sum = 0
    bag_sum = 0
    iter = 1
    for k in dict:
        dict[k][0] = iter
        dict[k][5] = len(dict[k][5])
        count_sum = count_sum + dict[k][3]
        weight_sum = weight_sum + dict[k][4]
        bag_sum = bag_sum + dict[k][5]
        iter = iter + 1

    last = ['', '', '', count_sum, weight_sum, bag_sum]
    context = {'dict': dict, "last": last, 'routeID': pk,
               'routeInf': 'Рейс №' + str(pk) + ' ('
                           + route.country_recipient.name + ') ' + str(route.date.date()),
               "weight_sum": weight_sum}

    html_string = render_to_string("route/pdf/route_products.html", context)
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                        presentational_hints=True)
    return response

