from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from route.views import get_base_template_name
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from django.db.models import Sum
from django.contrib import messages
from .filters import *
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse
import weasyprint
from route.models import ReceptionTransmission, Inspector, Packer, Loader, Currency

class Reports(TemplateView):
    template_name = 'financial/pages/reports.html'
    def get(self, request, *args, **kwargs):
        f = OperationsFilter(request.GET, queryset=Operations.objects.all())

        if 'print' in request.GET:
            html_string = render_to_string("financial/print/reports.html", {"obj_list": f.qs})
            response = HttpResponse(content_type='application/pdf')
            weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                write_pdf(response, presentational_hints=True)
            return response

        return render(request, self.template_name, {'filter': f,
                                                    'base_template_name': get_base_template_name(request.user)})


class AdvanceView(TemplateView):
    template_name = 'financial/pages/prepaid.html'

    def get(self, request, *args, **kwargs):
        f = AdvanceFilter(request.GET, queryset=OperationsInner.objects.filter(inner__type2=4,
                                                                               article__name__iexact="Расходы по оплате труда"))
        text = 'Авансы сотрудников'

        try:
            currency = request.GET["inner__currency"]
            dateFrom = request.GET["inner__date_min"]
            dateTo = request.GET["inner__date_max"]
            currency = Currency.objects.get(pk=currency)
            text = 'Авансы сотрудников (' + currency.name + ') c ' + str(dateFrom) + ' по ' + str(dateTo)

        except Exception as e:
            print(e)

        if 'print' in request.GET:
            html_string = render_to_string("financial/print/advance.html", {'text': text, "obj_list": f.qs})
            response = HttpResponse(content_type='application/pdf')
            weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                write_pdf(response, presentational_hints=True)
            return response
        else:
            return render(request, self.template_name, {'text': text, 'filter': f})

class FinesView(TemplateView):
    template_name = 'financial/pages/fines.html'

    def get(self, request, *args, **kwargs):
        f = FinesFilter(request.GET, queryset=OperationsInner.objects.filter(inner__type2=4,
                                                                             article__name__iexact="Штрафы Сотрудников"))
        text = 'Штрафы сотрудников'

        try:
            currency = request.GET["inner__currency"]
            dateFrom = request.GET["inner__date_min"]
            dateTo = request.GET["inner__date_max"]
            currency = Currency.objects.get(pk=currency)
            text = 'Штрафы сотрудников (' + currency.name + ') c ' + str(dateFrom) + ' по ' + str(dateTo)

        except Exception as e:
            print(e)

        if 'print' in request.GET:
            html_string = render_to_string("financial/print/fines.html", {'text': text, "obj_list": f.qs})
            response = HttpResponse(content_type='application/pdf')
            weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                write_pdf(response, presentational_hints=True)
            return response
        else:
            return render(request, self.template_name, {'text': text, 'filter': f})

class WorkPayView(TemplateView):
    template_name = 'financial/pages/work_pay.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': WorkPayForm()})

    def post(self, request, *args, **kwargs):
        form = WorkPayForm(request.POST)
        if form.is_valid():
            RT = ReceptionTransmission.objects.filter(history=False,
                                                      dateRT__range=[form.cleaned_data['dateFrom'], form.cleaned_data["dateTo"]],
                                                      route__in=request.POST.getlist('route'))

            obj = Inspector.objects.filter(id_REC_TRAN__in=RT)
            dict = {}
            for ob in obj:
                key = ob.employee
                count = Inspector.objects.filter(id_REC_TRAN=ob.id_REC_TRAN).count()
                if key in dict:
                    dict[key] = dict[key] + float(form.cleaned_data['inspection'])*ob.id_REC_TRAN.pogr/count
                else:
                    dict[key] = float(form.cleaned_data['inspection'])*ob.id_REC_TRAN.pogr/count

            obj1 = Packer.objects.filter(id_REC_TRAN__in=RT)

            for ob in obj1:
                key = ob.employee
                count = Packer.objects.filter(id_REC_TRAN=ob.id_REC_TRAN).count()
                if key in dict:
                    dict[key] = dict[key] + float(form.cleaned_data['packing']) * ob.id_REC_TRAN.pogr / count
                else:
                    dict[key] = float(form.cleaned_data['packing']) * ob.id_REC_TRAN.pogr / count

            L, N = [], 1
            for k in dict:
                L.append([N, "("+str(k.employeeID)+") " + k.fullname, dict[k], k.pk])
                N = N + 1

            text = str(form.cleaned_data['dateFrom']) + " - " + str(form.cleaned_data['dateTo'])

            if 'print' in request.POST:
                html_string = render_to_string("financial/print/work_pay.html", {"obj": L, 'text': text})
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                    write_pdf(response, presentational_hints=True)
                return response

            return render(request, self.template_name, {'form': form, "obj": L, 'text': text})

        print(form.errors)
        return render(request, self.template_name, {'form': form})

class WorkPayEmpView(TemplateView):
    template_name = 'financial/pages/work_pay_emp.html'

    def post(self, request, *args, **kwargs):
        try:
            form = WorkPayForm(request.POST)
            if form.is_valid():
                RT = ReceptionTransmission.objects.filter(history=False,
                                                          dateRT__range=[form.cleaned_data['dateFrom'],
                                                                         form.cleaned_data["dateTo"]],
                                                          route__in=request.POST.getlist('route'))
                employee = Employee.objects.get(pk=kwargs['pk'])
                dict = {}
                ins = Inspector.objects.filter(employee=employee, id_REC_TRAN__in=RT)

                for i in ins:
                    count = Inspector.objects.filter(id_REC_TRAN=i.id_REC_TRAN).count()
                    share = i.id_REC_TRAN.pogr * form.cleaned_data['inspection'] / count
                    key = i.id_REC_TRAN
                    dict[key] = share

                packers = Packer.objects.filter(employee=employee, id_REC_TRAN__in=RT)

                for p in packers:
                    count = Packer.objects.filter(id_REC_TRAN=p.id_REC_TRAN).count()
                    share = p.id_REC_TRAN.pogr * form.cleaned_data['packing'] / count
                    key = p.id_REC_TRAN
                    if key in dict:
                        dict[key] = dict[key] + share
                    else:
                        dict[key] = share

                L, N, total = [], 1, 0

                for k in dict:
                    inf = "(акт - " + str(k.pk)+") ( RACE ID - " + str(k.route.idRoute) + \
                          " - " + k.route.country_recipient.name + " )"
                    L.append([N, inf, dict[k], k.pk])
                    N = N + 1
                    total = total + dict[k]

                return render(request, self.template_name, {"obj": L,
                                                            'date': str(form.cleaned_data['dateFrom'])+" - "
                                                                    +str(form.cleaned_data['dateTo']),
                                                            "employee": employee,
                                                            "total": total})
            return render(request, 'financial/pages/work_pay.html', {'form': form})
        except Exception as e:
            print(e)

        return render(request, 'financial/pages/work_pay.html', {'form': WorkPayForm()})


class LoadingPayView(TemplateView):
    template_name = 'financial/pages/loading_pay.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': LoadingPayForm()})

    def post(self, request, *args, **kwargs):
        form = LoadingPayForm(request.POST)

        if form.is_valid():
            RT = ReceptionTransmission.objects.filter(history=False,
                                                      dateRT__range=[form.cleaned_data['dateFrom'],
                                                                     form.cleaned_data["dateTo"]],
                                                      route__in=request.POST.getlist('route'))
            routesRT, dict, N, RET  = [], {}, 1, []
            for r in RT:
                if r.route not in routesRT:
                    routesRT.append(r.route)

            load = Loader.objects.filter(route__in=routesRT)

            for l in load:
                key = l.name
                rt = RT.filter(route=l.route)
                count = Loader.objects.filter(route=l.route).count()
                for r in rt:
                    if key in dict:
                        dict[key] = dict[key] + float(request.POST['loading']) * r.pogr / count
                    else:
                        dict[key] = float(request.POST['loading'])*r.pogr/count

            for k in dict:
                RET.append([N, "("+str(k.employeeID)+"), " + k.fullname, dict[k], k.pk])

            date = str(form.cleaned_data['dateFrom']) + " - " + str(form.cleaned_data['dateTo'])

            if 'print' in request.POST:
                html_string = render_to_string("financial/print/loading_pay.html", {"obj": RET,
                                                        'text': date})
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                    write_pdf(response, presentational_hints=True)
                return response
            return render(request, self.template_name, {"obj": RET, 'form': form,
                                                        'text': date})

        return render(request, self.template_name, {'form': LoadingPayForm()})


class LoadingPayEmpView(TemplateView):
    template_name = 'financial/pages/loading_pay_emp.html'

    def post(self, request, *args, **kwargs):
        form = LoadingPayForm(request.POST)
        if form.is_valid():
            RT = ReceptionTransmission.objects.filter(history=False,
                                                      dateRT__range=[form.cleaned_data['dateFrom'],
                                                                     form.cleaned_data["dateTo"]],
                                                      route__in=request.POST.getlist('route'))
            routesRT, dict, N, RET, t  = [], {}, 1, [], 0
            for r in RT:
                if r.route not in routesRT:
                    routesRT.append(r.route)

            employee = Employee.objects.get(pk=kwargs['pk'])

            load = Loader.objects.filter(route__in=routesRT, name=employee)

            for l in load:
                rt = RT.filter(route=l.route)
                count = Loader.objects.filter(route=l.route).count()
                for r in rt:
                    dict[r] = float(form.cleaned_data['loading'])*r.pogr/count

            for k in dict:
                inf = "(акт - " + str(k.pk) + ") ( RACE ID - " + str(k.route.idRoute) + \
                      " - " + k.route.country_recipient.name + " )"
                RET.append([N, inf, dict[k], k.pk])
                N = N + 1
                t = t + dict[k]
            return render(request, self.template_name, {"obj": RET,
                                                        'date': str(form.cleaned_data['dateFrom']) + " - "
                                                                + str(form.cleaned_data['dateTo']),
                                                        "employee": employee,
                                                        "total": t})

        return render(request, self.template_name, {'form': LoadingPayForm()})