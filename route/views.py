import weasyprint
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from collections import Counter
from django.http import JsonResponse

import user
from .forms import *
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.shortcuts import HttpResponse
from django.template.loader import get_template, render_to_string
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum
from .filters import *
from django.core.exceptions import ObjectDoesNotExist
from debits.models import ClientContrAgents
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateRoute(LoginRequiredMixin, CreateView):
    form_class = RouteForm
    template_name = 'route/forms/route_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('route:list_route_url')

    def get_context_data(self, **kwargs):
        data = super(CreateRoute, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = LoaderFormSet(self.request.POST)
        else:
            data['formset'] = LoaderFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                return super(CreateRoute, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

class UpdateRouteView(LoginRequiredMixin, UpdateView):
    model = Route
    form_class = RouteUpdateForm
    template_name = 'route/forms/route_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('route:list_route_url')

    def get_context_data(self, **kwargs):
        data = super(UpdateRouteView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = LoaderFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = LoaderFormSet(instance=self.object)

        data['idRoute'] = self.object.idRoute
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                return super(UpdateRouteView, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

@login_required
def deleteRoute(request, pk):
    get_object_or_404(Route, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('route:list_route_url')

class RegistrationPlaceView(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/registrations_places.html'
    def get(self, request, *args, **kwargs):

        f = RegistrationFilter(request.GET, queryset=Registration.objects.all())
        paginator = Paginator(f.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class RegPlacesAddView(LoginRequiredMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'route/forms/registration_places_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('route:reg_places')

@login_required
def reg_places_delete(request, id):
    get_object_or_404(Registration, id=id).delete()
    messages.success(request, 'Запись под номером ' + str(id) + ' была успешно удалена')
    return redirect('route:reg_places')

class RegPlacesEditView(LoginRequiredMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'route/forms/registrations_place_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('route:reg_places')


class DirectionsView(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/directions.html'
    def get(self, request, *args, **kwargs):

        f = DirectionFilter(request.GET, queryset=Direction.objects.all())

        paginator = Paginator(f.qs, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class DirectionAddView(LoginRequiredMixin, CreateView):
    form_class = DirectionsForm
    template_name = 'route/forms/direction_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('route:directions')

class DirectionEditView(LoginRequiredMixin, UpdateView):
    model = Direction
    form_class = DirectionsForm
    template_name = 'route/forms/direction_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('route:directions')

@login_required
def directions_delete(request, id):
    get_object_or_404(Direction, id=id).delete()
    messages.success(request, 'Запись под номером ' + str(id) + ' была успешно удалена')
    return redirect('route:directions')



class CurrencyView(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/currency.html'

    def get(self, request, *args, **kwargs):
        f = CurrencyFilter(request.GET, queryset=Currency.objects.all())
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class CurrencyAddView(LoginRequiredMixin, CreateView):
    form_class = CurrencyForm
    template_name = 'route/forms/currency_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('route:currency')

class CurrencyEditView(LoginRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'route/forms/currency_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('route:currency')

@login_required
def currency_delete(request, id):
    get_object_or_404(Currency, id=id).delete()
    messages.success(request, 'Запись под номером ' + str(id) + ' была успешно удалена')
    return redirect('route:currency')

class ServicePriceView(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/service_price.html'

    def get(self, request, *args, **kwargs):

        f = ServicePriceFilter(request.GET, queryset=ServicePrice.objects.all())
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class FinancialReport(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/financial_report.html'

    def get(self, request, *args, **kwargs):
        form = FinancialReportForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            if request.is_ajax():
                country = Direction.objects.get(pk=request.POST['country'])
                routes = Route.objects.filter(country_recipient=country)
                routesV = []
                for r in routes:
                    routesV.append({
                        'id': r.idRoute,
                        'route': str(r.idRoute) + ' (' + str(r.date.strftime('%Y')) + ')',
                        'country': r.country_recipient.pk
                    })
                return JsonResponse({'routes': routesV}, status=200)

            country = Direction.objects.get(pk=request.POST['country'])
            routes = Route.objects.filter(country_recipient=country)
            routesOPT = []
            for r in routes:
                routesOPT.append((r.pk, str(r.idRoute) + ' (' + str(r.date.strftime('%Y')) + ')'))

            form = FinancialReportForm(request.POST)
            form.fields['routeFrom'].choices = routesOPT
            form.fields['routeTo'].choices = routesOPT

            registration = Registration.objects.get(pk=request.POST['registration'])
            RT = ReceptionTransmission.objects.filter(route__idRoute__range=
                                                      [request.POST['routeFrom'], request.POST['routeTo']],
                                                      registration=registration)
            perevozka = []
            sum_count_Bishkek = 0
            sum_price_Bishkek = 0
            sum_count_RecipCountry = 0
            sum_price_RecipCountry = 0
            sum_general_count = 0
            sum_general_price = 0

            RouteR = []
            for rt in RT:
                ser1 = Services.objects.get(id_REC_TRAN=rt, service=1)
                currency_Som = rt.route.currency_Som
                if rt.route.idRoute not in RouteR:
                    RouteR.append(rt.route.idRoute)
                if ser1.status:
                    perevozka.append({
                        'servicePrice': ser1.priceIV*currency_Som,
                        'count_Bishkek': ser1.count,
                        'price_Bishkek': ser1.priceIV*currency_Som*ser1.count,
                        'count_RecipCountry': 0,
                        'price_RecipCountry': 0,
                        'general_count': ser1.count,
                        'general_price': ser1.priceIV*currency_Som*ser1.count})
                    sum_count_Bishkek = sum_count_Bishkek + ser1.count
                    sum_price_Bishkek = sum_price_Bishkek + ser1.priceIV*currency_Som*ser1.count
                    sum_general_count = sum_general_count + ser1.count
                    sum_general_price = sum_general_price + ser1.priceIV*currency_Som*ser1.count

                else:
                    perevozka.append({
                        'servicePrice': ser1.priceIV,
                        'count_Bishkek': 0,
                        'price_Bishkek': 0,
                        'count_RecipCountry': ser1.count,
                        'price_RecipCountry': ser1.priceIV*ser1.count,
                        'general_count': ser1.count,
                        'general_price': ser1.priceIV*ser1.count,
                    })
                    sum_count_RecipCountry = sum_count_RecipCountry + ser1.count
                    sum_price_RecipCountry = sum_price_RecipCountry + ser1.priceIV*ser1.count
                    sum_general_count = sum_general_count + ser1.count
                    sum_general_price = sum_general_price + ser1.priceIV*ser1.count

            perevozka_sum = {
                "sum_count_Bishkek": sum_count_Bishkek,
                "sum_price_Bishkek": sum_price_Bishkek,
                "sum_count_RecipCountry": sum_count_RecipCountry,
                "sum_price_RecipCountry": sum_price_RecipCountry,
                "sum_general_count": sum_general_count,
                "sum_general_price": sum_general_price
            }

            ServicesRT = []
            for i in range(0, 8):
                ServicesRT.append({
                    'service': '',
                    'servicePrice': 0,
                    'count_Bishkek': 0,
                    'price_Bishkek': 0,
                    'count_RecipCountry': 0,
                    'price_RecipCountry': 0,
                    'general_count': 0,
                    'general_price': 0})

            for rt in RT:
                currency_Som = rt.route.currency_Som

                i = 0
                serRT = Services.objects.filter(id_REC_TRAN=rt)
                for ser in serRT:

                    if ser.service != "1":
                        ServicesRT[i]['service'] = ser.get_service_display()
                        ServicesRT[i]['servicePrice'] = ser.priceIV

                        if ser.status == True:
                            ServicesRT[i]['count_Bishkek'] = ServicesRT[i]['count_Bishkek'] + ser.count
                            ServicesRT[i]['price_Bishkek'] = ServicesRT[i]['price_Bishkek'] + ser.priceIV * currency_Som * ser.count
                            ServicesRT[i]['general_count'] = ServicesRT[i]['general_count'] + ser.count
                            ServicesRT[i]['general_price'] = ServicesRT[i]['general_price'] + ser.priceIV * currency_Som * ser.count
                        else:
                            ServicesRT[i]['count_RecipCountry'] = ServicesRT[i]['count_RecipCountry'] + ser.count
                            ServicesRT[i]['price_RecipCountry'] = ServicesRT[i]['price_RecipCountry'] + ser.priceIV * ser.count
                            ServicesRT[i]['general_count'] = ServicesRT[i]['general_count'] + ser.count
                            ServicesRT[i]['general_price'] = ServicesRT[i]['general_price'] + ser.priceIV * ser.count

                        i = i+1

            Sum_Services = {
                'count_Bishkek': 0,
                'price_Bishkek': 0,
                'count_RecipCountry': 0,
                'price_RecipCountry': 0,
                'general_count': 0,
                'general_price': 0,
            }

            for i in ServicesRT:
                Sum_Services['count_Bishkek'] = Sum_Services['count_Bishkek'] + i['count_Bishkek']
                Sum_Services['price_Bishkek'] = Sum_Services['price_Bishkek'] + i['price_Bishkek']
                Sum_Services['count_RecipCountry'] = Sum_Services['count_RecipCountry'] + i['count_RecipCountry']
                Sum_Services['price_RecipCountry'] = Sum_Services['price_RecipCountry'] + i['price_RecipCountry']
                Sum_Services['general_count'] = Sum_Services['general_count'] + i['general_count']
                Sum_Services['general_price'] = Sum_Services['general_price'] + i['general_price']

            if "searh_button" in request.POST:
                context = {
                    'form': form,
                    'perevozka': perevozka,
                    "perevozka_sum": perevozka_sum,
                    'Services': ServicesRT,
                    'Sum_Services': Sum_Services,
                    'country': country.name,
                    'RouteID': RouteR,
                    'registration': registration.name,
                }
                return render(request, self.template_name, context)

            elif "print_button" in request.POST:
                context = {
                    'perevozka': perevozka,
                    "perevozka_sum": perevozka_sum,
                    'Services': Services,
                    'Sum_Services': Sum_Services,
                    'country': country.name,
                    'RouteID': RouteR,
                    'registration': registration.name,
                }
                html_string = render_to_string("route/pdf/financial_report.html", context)
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                                 presentational_hints=True)
                return response

        except Exception as e:
            print(e)


class ServicePriceAddView(LoginRequiredMixin, CreateView):
    form_class = ServicePriceForm
    template_name = 'route/forms/service_price_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('route:service_price')

    def get_context_data(self, **kwargs):
        data = super(ServicePriceAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['prices'] = PriceFormSet(self.request.POST)
        else:
            data['prices'] = PriceFormSet()

        data['text'] = 'Добавление цены сервисов'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        prices = context['prices']

        with transaction.atomic():
            if prices.is_valid():
                self.object = form.save()

                prices.instance = self.object
                prices.save()
                return super(ServicePriceAddView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())

class ServicePriceViewID(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/service_price_id.html'

    def get(self, request, *args, **kwargs):

        f = PriceFilter(request.GET, queryset=Price.objects.filter(servicePrice=self.kwargs['pk']))
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class ServicePriceEditView(LoginRequiredMixin, UpdateView):
    model = ServicePrice
    form_class = ServicePriceForm
    template_name = 'route/forms/service_price_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('route:service_price')

    def get_context_data(self, **kwargs):
        data = super(ServicePriceEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['prices'] = PriceFormSet2(self.request.POST, instance=self.object)
        else:
            data['prices'] = PriceFormSet2(instance=self.object)

        data['text'] = 'Редактирование цены сервисов'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        prices = context['prices']

        with transaction.atomic():
            if prices.is_valid():
                self.object = form.save()

                prices.instance = self.object
                prices.save()
                return super(ServicePriceEditView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())

@login_required
def service_price_delete(request, id):
    get_object_or_404(ServicePrice, id=id).delete()
    messages.success(request, 'Запись под номером ' + str(id) + ' была успешно удалена')
    return redirect('route:service_price')

class ShowRouteID(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/routeID.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        route = Route.objects.get(pk = pk)
        RT = ReceptionTransmission.objects.filter(history=False, route=route)
        general = []
        RTReturn = []
        gCount = 0
        gWeight = 0
        gBag_number = 0
        gRemainder = 0
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
                'route1': route,
                'products': products,
                'recTran': rt,
                'CounterBagNumber': len(Counter(bag_number)),
                'SumCount': SumCount,
                'SumWeight': toFixed(SumWeight, 2),
                'remainder': remainder,
            })
            gCount += SumCount
            gWeight += SumWeight
            gBag_number += len(Counter(bag_number))
            gRemainder += remainder

        general.append({
            'gCount': gCount,
            'gWeight' : toFixed(gWeight, 1),
            'gBag_number': gBag_number,
            'gRemainder': gRemainder,
            'routeID': route.idRoute,
        })

        return render(request, self.template_name, {
            'base_template_name': get_base_template_name(request.user),
            'routeID': route.idRoute,
            'RT': RTReturn,
            'general': general,
            'route': route.idRoute,
            'routeInf': 'Рейс №' + str(route.idRoute) + ' (' + route.country_recipient.name+') ' + str(route.date.date())})

def chunk_dict(d, chunk_size):
    r = {}
    for k, v in d.items():
        if len(r) == chunk_size:
            yield r
            r = {}
        r[k] = v
    if r:
        yield r

class RouteBagReportOld(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/route_bagreport_old.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

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
        return render(request, self.template_name, {'list': list(chunk_dict(dict, 12)), 'routeID': pk,
                                                    'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name
                                                    + ') ' + str(route.date.date()),
                                                    'base_template_name': get_base_template_name(request.user)
                                                    })

class RouteBagReportView(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/route_bag_report.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

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

        return render(request, self.template_name, {'dict': dict, 'remainder': remainder, "weight_sum": weight_sum, 'routeID': pk,
                                                    'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name+') ' + str(route.date.date()),
                                                    'base_template_name': get_base_template_name(request.user)
                                                    })

class RouteCountProducts(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/route_products.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

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
        return render(request, self.template_name, {'dict': dict, "last": last, 'routeID': pk,
                                                    'routeInf': 'Рейс №' + str(pk) + ' ('
                                                    + route.country_recipient.name+') ' + str(route.date.date()),
                                                    'weight_sum': weight_sum,
                                                    'base_template_name': get_base_template_name(request.user)})


class RouteNumberOfPlaces(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/route_number_of_places.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
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
                dict[key][4] += len(bag_num)
                dict[key][5] += w
                dict[key][6] += rt.remainder
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

        return {"obj": dict, 'routeID': pk,
                'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name + ') ' + str(route.date.date()),
                'base_template_name': get_base_template_name(self.request.user)}

class RouteNumberOfPlacesClient(LoginRequiredMixin, TemplateView):
    template_name = 'route/forms/number_of_places.html'
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
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
                dict[key][4] += len(bag_num)
                dict[key][5] += w
                dict[key][6] += rt.remainder
            else:
                dict[key] = [rt.recipient.fullname, rt.recipient.store, rt.recipient.container,
                             rt.recipient.row, len(bag_num), w, rt.remainder]
        initial = []
        iter = 1
        RET = []
        for key in dict:
            recipient = Client.objects.get(pk=key)
            l = [iter, key]
            l.extend(dict[key])
            RET.append(l)
            initial.append({
                "recipient": recipient,
                "route": route})
            iter += 1

        NumOfP = NumberOfPlaces.objects.filter(route=route)
        for ob in NumOfP:
            try:
                index = initial.index({"recipient": ob.recipient, "route": route})
                initial[index] = {"recipient": ob.recipient, "route": route, "agent": ob.agent, 'unloading': ob.unloading}
            except ValueError:
                print('value error')
        if self.request.POST:
            formset = NumberOfPlacesFormSet(self.request.POST)
        else:
            formset = NumberOfPlacesFormSet(initial=initial)

        obj = zip(RET, formset)

        return {"obj": obj, "formset": formset, 'routeID': pk,
                'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name + ') ' + str(route.date.date()),
                'base_template_name': get_base_template_name(self.request.user)}

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        formset = NumberOfPlacesFormSet(self.request.POST)

        obj = context['obj']
        routeInf = context['routeInf']
        RET = list(zip(*obj))
        RET = RET[0]
        obj = zip(RET, formset)

        if 'print' in request.POST:
            html_string = render_to_string("route/pdf/route_num_pl_Client.html",
                                           {'obj': obj,
                                            'routeInf': routeInf})
            response = HttpResponse(content_type='application/pdf')
            weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                                 presentational_hints=True)
            return response

        else:
            print('else')
            with transaction.atomic():
                if formset.is_valid():
                    route = Route.objects.get(pk=kwargs['pk'])
                    for form in formset:
                        try:
                            obj = NumberOfPlaces.objects.get(route=route, recipient=form.cleaned_data['recipient'])
                            obj.agent = form.cleaned_data['agent']
                            obj.unloading = form.cleaned_data['unloading']
                            obj.save()
                        except ObjectDoesNotExist:
                            obj = NumberOfPlaces(
                                route=route,
                                recipient=form.cleaned_data['recipient'],
                                agent=form.cleaned_data['agent'],
                                unloading=form.cleaned_data['unloading']
                            )
                            obj.save()
                    messages.success(request, 'Все агенты прикреплены к клиентам')

        return self.render_to_response(self.get_context_data())

def get_base_template_name(user):
    if user.role == 2:
        base_template_name = 'extends/index_sub_admin.html'
    elif user.role == 3:
        base_template_name = 'extends/index_operator.html'
    elif user.role == 4:
        base_template_name = 'extends/index_accountant.html'
    elif user.role == 5:
        base_template_name = 'extends/index_agent.html'
    elif user.role == 6:
        base_template_name = 'extends/index_client.html'
    else:
        base_template_name = 'extends/index.html'
    return base_template_name


class RouteNumberOfPlacesAgent(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/route_num_places_agent.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
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

        return {"Ret": Ret, 'routeID': pk,
                'routeInf': 'Рейс №' + str(pk) + ' (' + route.country_recipient.name + ') ' + str(route.date.date()),
                'base_template_name': get_base_template_name(self.request.user)}


def toFixed(SumWeight, param):
    return f"{SumWeight:.{param}f}"


class ListRoute(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/routes.html'

    def get(self, request, *args, **kwargs):
        f = RouteFilter(request.GET, queryset=Route.objects.all().order_by('-id'))
        routes = f.qs
        object_list = []
        for r in routes:
            SumCount = 0
            SumWeight = 0
            RT = ReceptionTransmission.objects.filter(history=False, route=r)
            for rt in RT:
                P = ProductP.objects.filter(recTranID=rt.id)
                for p in P:

                    SumCount = SumCount +  1
                    SumWeight = SumWeight + p.weight

            object_list.append({
                'idRoute': str(r.idRoute) + '(Мест - '+str(SumCount)+') (Вес - '+str(toFixed(SumWeight, 2))+')',#24 (Мест - 0) (Вес - 0.00)
                'country_recipient_name': r.country_recipient.name,
                'date': r.date.date,
                'status': r.status,
                'control_status': r.control_status,
                'pk': r.pk,
                'locaton': r.get_location_display(),
            })

        paginator = Paginator(object_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': f.form,
            'page_obj': page_obj,
            'base_template_name': get_base_template_name(request.user),
        }
        return render(request, self.template_name, context)


def showRouteModal(request):
    if request.is_ajax and request.method == "POST":
        try:
            pk = request.POST['pk']
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
                                 'priceSom': s.priceIV * currency_Som,
                                 'SumPriceIV': sumPriceIV,
                                 'SumPriceSom': sumPriceSom,
                                 'status': status,
                                 })

            products = ProductP.objects.filter(recTranID=pk)

            SumCount = 0
            SumWeight = 0
            bag_number = []
            productsJ = []
            for p in products:
                productsJ.append({
                    'product': p.product.name,
                    'code': p.product.code,
                    'bag_number': p.bag_number,
                    'count': p.count,
                    'weight': p.weight,
                })
                bag_number.append(p.bag_number)
                SumCount += p.count
                SumWeight += p.weight

            inf = {
                'rtPK': recTran.pk,
                'routeId': str(recTran.route.pk)+'('+recTran.route.country_recipient.name+')',
                'date': recTran.dateRT.date(),
                'time': recTran.dateRT.time(),
                'registration': recTran.registration.name,
                'sender': recTran.sender.fullname,
                'senderPhone': recTran.sender.phone,
                'recipient': recTran.recipient.fullname,
                'recipientPhone': recTran.recipient.phone,
                'operator': recTran.operator.email,

            }

            context = {
                'inf': inf,
                'products': productsJ,
                'services': services,
                'TotalPayable': str(TotalPayable)+'сом',
                'remainder': str(remainder)+currency_recipient,
                'CounterBagNumber': len(Counter(bag_number)),
                'SumCount': SumCount,
                'SumWeight': SumWeight,
            }

            return JsonResponse(context, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)

#----------------------------------


def searchByBagNumber(request):
    if request.is_ajax and request.method == "POST":
        try:
            bag_N = request.POST['bag_N']
            routeForSearch = request.POST['routeForSearch']
            context = {}
            RT = ReceptionTransmission.objects.filter(history=False, route__pk=routeForSearch)

            for rt in RT:
                if ProductP.objects.filter(bag_number=int(bag_N), recTranID=rt.pk).count():
                    context['answer'] = True
                    context['RecTransID'] = rt.pk
                    return JsonResponse(context, status=200)

            context['answer'] = False
            return JsonResponse(context, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def SeatsAndWeightReport(request):
    if request.is_ajax and request.method == "POST":
        try:
            recipient = Client.objects.get(pk=request.POST.get('recipient'))
            sender = Client.objects.get(pk=request.POST.get('sender'))
            registration = Registration.objects.get(pk=request.POST.get('registration'))
            print(request.POST['race'])
            print(recipient)
            print(sender)
            print(registration)

            try:
                RT = ReceptionTransmission.objects.filter(
                    history=False,
                    route=request.POST['race'],
                    recipient=recipient,
                    sender=sender,
                    registration=registration,
                    dateRT__range=[request.POST['dateFrom'], request.POST['dateTo']]
                )

                SumCount = 0
                SumWeight = 0

                for rt in RT:
                    productsRT=ProductP.objects.filter(recTranID=rt.pk)
                    for p in productsRT:
                        SumCount += p.count
                        SumWeight += p.weight

                return JsonResponse({"found": True,
                                     'count': SumCount,
                                     'weight': SumWeight}, status=200)

            except Exception as e:
                print("error !!!", e)
                return JsonResponse({"found": False}, status=200)

        except Exception as e:
            print("error2 !!!", e)
            return JsonResponse({"error": str(e)}, status=500)

@login_required
def recTrans_delete(request, pk):
    recTans = ReceptionTransmission.objects.get(pk=pk)
    recTans.history = True
    recTans.save()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('route:list_rt')

class ListReceptionTransmission(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/listReceptionTransmission.html'
    def get(self, request, *args, **kwargs):
        obj = ReceptionTransmission.objects.filter(history=False)

        f = RTFilter(request.GET, queryset=obj)
        paginator = Paginator(f.qs, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        routes = []
        for o in obj:
            routes.append({'routeID': o.route.pk, 'routeCountry': o.route.country_recipient})

        context = {'form': f.form, 'page_obj': page_obj}

        context['routes'] = routes
        context['senders'] = Client.objects.filter(type=2)
        context['recipients'] = Client.objects.filter(type=1)
        context['registrations'] = Registration.objects.all()
        context['base_template_name'] = get_base_template_name(self.request.user)

        return render(request, self.template_name, context)

class ListReceptionTransmissionHistory(LoginRequiredMixin, TemplateView):
    template_name = 'route/pages/listHistoryReceptionTransmission.html'

    def get(self, request, *args, **kwargs):

        f = RTFilter(request.GET, queryset=ReceptionTransmission.objects.filter(history=True))
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

def ReceptionTransmissionContract(request, pk):
    template = loader.get_template('route/pages/show_RecTranID.html')
    recTran = ReceptionTransmission.objects.get(pk=pk)

    services = []

    currency_Som = recTran.route.currency_Som
    currency_recipient = recTran.route.currency_recipient.name

    TotalPayable = 0
    remainder = 0
    servicesRT = Services.objects.filter(id_REC_TRAN=recTran)
    for s in servicesRT:
        sumPriceIV = s.priceIV*s.count
        sumPriceSom = s.priceIV*currency_Som*s.count
        status = ''
        if s.status:
            TotalPayable += sumPriceSom
            status = 'опл'
        else:
            remainder += sumPriceIV

        services.append({'service': s.get_service_display(),
                         'count': s.count,
                         'priceIV': s.priceIV,
                         'priceSom': round(s.priceIV*currency_Som, 3),
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
               'TotalPayable': round(TotalPayable, 0),
               'remainder': round(remainder, 0),
               'currency_recipient': currency_recipient,
               'CounterBagNumber': len(Counter(bag_number)),
               'SumCount': round(SumCount, 0),
               'SumWeight': round(SumWeight, 0),
               'sender': recTran.sender.fullname,
               'operator': recTran.operator.first_name+" "+recTran.operator.last_name,
               'recTranID': pk,
               'base_template_name': get_base_template_name(request.user),

               }

    return HttpResponse(template.render(context, request))

@login_required
def ReceptionTransmissionContractHistory(request, pk):
    template = loader.get_template('route/pages/show_RecTranId_History.html')
    recTran = ReceptionTransmission.objects.get(pk=pk)

    services = []

    currency_Som = recTran.route.currency_Som
    currency_recipient = recTran.route.currency_recipient.name

    TotalPayable = 0
    remainder = 0
    servicesRT = Services.objects.filter(id_REC_TRAN=recTran)
    for s in servicesRT:
        sumPriceIV = s.priceIV*s.count
        sumPriceSom = s.priceIV*currency_Som*s.count
        status = ''
        if s.status:
            TotalPayable += sumPriceSom
            status = 'опл'
        else:
            remainder += sumPriceIV

        services.append({'service': s.get_service_display(),
                         'count': s.count,
                         'priceIV': s.priceIV,
                         'priceSom': s.priceIV*currency_Som,
                         'SumPriceIV': sumPriceIV,
                         'SumPriceSom': sumPriceSom,
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
               'TotalPayable': TotalPayable,
               'remainder': remainder,
               'currency_recipient': currency_recipient,
               'CounterBagNumber': len(Counter(bag_number)),
               'SumCount': SumCount,
               'SumWeight': SumWeight,
               'sender': recTran.sender.fullname,
               'operator': recTran.operator.email,
               'recTranID': pk
               }

    return HttpResponse(template.render(context, request))


def checkBagNumber(request):
    if request.is_ajax and request.method == "POST":
        try:
            routeID = request.POST['routeID']

            val = request.POST['val']

            obj = ProductP.objects.filter(recTranID__route_id=routeID, bag_number=val)
            if(obj):
                return JsonResponse({'answer': True}, status=200)
            return JsonResponse({'answer': False}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def selectedRoute(request):
    if request.is_ajax and request.method == "POST":
        try:
            route_id = request.POST['route_id']
            route = Route.objects.get(pk=route_id)

            obj = Price.objects.filter(country=route.country_recipient, currency=route.currency_recipient)

            ServicesRet = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            for ob in obj:
                try:
                    ServicesRet[int(ob.service)] = ob.price
                except Exception as e:
                    print(e)
            routeZ = route.idRoute
            return JsonResponse({'routeZ': routeZ, 'Services': ServicesRet, 'currency': route.currency_Som,
                                 'currency_name': route.currency_recipient.name}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def change_location(request):
    try:
        route_id = request.POST['route_id']
        route = Route.objects.get(pk=route_id)

        location = route.location

        if location == 'F':
            route.location = 'O'
            route.save()
        elif location == 'O':
            route.location = 'P'
            route.save()
        elif location == 'P':
            route.location = 'R'
            route.save()

        return JsonResponse({'location': route.get_location_display()}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


