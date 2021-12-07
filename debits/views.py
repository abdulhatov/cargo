from django.shortcuts import render, redirect, get_object_or_404
from route.views import get_base_template_name
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.db import transaction
from route.models import Services
from django.db.models import Q
from .filters import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from route.models import NumberOfPlaces, ReceptionTransmission

from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render
import weasyprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class ListAgentOfClient(LoginRequiredMixin, TemplateView):
    template_name = "debits/pages/agentofclient.html"
    def get(self, request, *args, **kwargs):

        if request.user.role == 1:
            qs = ClientContrAgents.objects.all()
        else:
            qs = ClientContrAgents.objects.filter(added_by=request.user)

        f = ClientContrAgentsFilter(request.GET, queryset=qs)

        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})


class AgentOfClientAddView(LoginRequiredMixin, CreateView):
    template_name = 'debits/forms/agentofclient.html'
    form_class = ClientContrAgentsForm

    def get_context_data(self, **kwargs):
        data = super(AgentOfClientAddView, self).get_context_data(**kwargs)
        data['text'] = "Добавление контрагента"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.added_by = self.request.user
        obj.save()
        return super(AgentOfClientAddView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('debits:agentofclient')

class AgentOfClientEditView(LoginRequiredMixin, UpdateView):
    template_name = 'debits/forms/agentofclient.html'
    model = ClientContrAgents
    form_class = ClientContrAgentsForm

    def get_context_data(self, **kwargs):
        data = super(AgentOfClientEditView, self).get_context_data(**kwargs)
        data['text'] = "Редактирование контрагента"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('debits:agentofclient')

@login_required
def deleteAgentOfClient(request, pk):
    get_object_or_404(ClientContrAgents, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('debits:agentofclient')

class ListIncomes(LoginRequiredMixin, TemplateView):
    template_name = 'debits/pages/incomes.html'

    def get(self, request, *args, **kwargs):

        if request.user.role == 1:
            qs = IncomeDebits.objects.all()
        else:
            qs = IncomeDebits.objects.filter(added_by=request.user)

        f = IncomeDebitsFilter(request.GET, queryset=qs)

        paginator = Paginator(f.qs, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class IncomeId(LoginRequiredMixin, TemplateView):
    template_name = 'debits/pages/incomeId.html'

    def get(self, request, *args, **kwargs):
        obj = IncomeDebits.objects.get(pk=kwargs['pk'])
        obj_inner = IncomeDebitsInner.objects.filter(inner=obj)
        context = {'obj': obj, 'obj_inner': obj_inner}
        context['base_template_name'] = get_base_template_name(request.user)
        return render(request, self.template_name, context)

class IncomeId2(LoginRequiredMixin, TemplateView):
    template_name = 'debits/pages/incomeId2.html'

    def get(self, request, *args, **kwargs):
        obj = IncomeDebits.objects.get(pk=kwargs['pk'])
        obj_inner = IncomeDebitsInner.objects.filter(inner=obj)
        context = {'obj': obj, 'obj_inner': obj_inner}
        context['base_template_name'] = get_base_template_name(request.user)
        return render(request, self.template_name, context)


def SetClient(agent_id):
    try:
        obj = NumberOfPlaces.objects.filter(agent=agent_id)
        objJ = []
        for ob in obj:
            str1 = "(" + str(ob.recipient.pk) + "), " + ob.recipient.fullname + ", " + ob.recipient.phone
            objJ.append((ob.recipient.pk, str1))

        return objJ

    except Exception as e:
        print("SetClient")
        print(e)
        return []

def getClientDebits(request):
    if request.is_ajax and request.method == "POST":
        try:
            client = Client.objects.get(pk=request.POST['client_id'])
            RT = ReceptionTransmission.objects.filter(
                history=False,
                recipient__pk=request.POST['client_id'])

            L, dict, total1, total2 = [], {}, 0.0, 0.0
            for rt in RT:
                key = rt.route.pk
                if key in dict:
                    dict[key][1] += rt.remainder
                else:
                    dict[key] = [str(rt.route.date.date()), rt.remainder]

            for key in dict:
                try:
                    obj = NumberOfPlaces.objects.get(recipient__pk=request.POST['client_id'],
                                                     route__pk=key)
                    dict[key][1] += obj.unloading
                except Exception as e:
                    print(e)
                total1 += dict[key][1]

            obj = IncomeDebitsInner.objects.filter(client=client)

            for ob in obj:
                L.append([ob.inner.pk, ob.sum, str(ob.inner.date)])
                total2 += ob.sum

            return JsonResponse({'dict': dict, "total1": total1,
                                 'income': L, "total2": total2,
                                 "client": client.fullname+" (" + str(client.pk) + ")"}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)


def SetRoute(pkC):
    try:
        RT = ReceptionTransmission.objects.filter(history=False, recipient__pk=pkC)
        dict = {}
        for rt in RT:
            key = rt.route.pk
            if key in dict:
                dict[key][0] += rt.remainder
            else:
                dict[key] = [rt.remainder, rt.route]

        RET = []
        remainder = 0
        for key in dict:
            obj = NumberOfPlaces.objects.filter(recipient__pk=pkC, route__pk=key)
            for ob in obj:
                dict[key][0] = dict[key][0] + ob.unloading
            route = dict[key][1]
            if dict[key][0] > 0:
                remainder = remainder + dict[key][0]

                RET.append((route.pk, str(route.idRoute) + " " + str(
                    route.date.strftime('%Y')) + " - " + route.country_recipient.name
                            + "(Долг: " + str(dict[key][0]) + ")"))
        return RET

    except Exception as e:
        print('SetRoute')
        print(e)
        return []

class IncomeDebitsAdd(LoginRequiredMixin, CreateView):
    form_class = IncomeDebitsForm
    template_name = 'debits/forms/income.html'

    def get_context_data(self, **kwargs):
        data = super(IncomeDebitsAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            formset = IncomeDebitsInnerFormset2(self.request.POST)
            agent = self.request.POST["agent"]

            for form in formset:
                form.fields['client'].choices = SetClient(agent)
                client = str(form.prefix)+"-client"
                form.fields['route'].choices = SetRoute(form.data[client])

            data["formset"] = formset

        else:
            formset = IncomeDebitsInnerFormset()
            for form in formset:
                form.fields['client'].queryset = Client.objects.none()
                form.fields['route'].queryset = Route.objects.none()
            data["formset"] = formset

        data["text"] = "Добавление приходника"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save(commit=False)
                self.object.added_by = self.request.user
                self.object.save()

                formset.instance = self.object
                formset.save()
                return super(IncomeDebitsAdd, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('debits:list_income')

class IncomeDebitsEdit(LoginRequiredMixin, UpdateView):
    model = IncomeDebits
    form_class = IncomeDEForm
    template_name = 'debits/forms/income_edit.html'

    def get_context_data(self, **kwargs):
        data = super(IncomeDebitsEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            formset = IDIEditFormSet2(self.request.POST, instance=self.object)

            for form in formset:
                client = str(form.prefix) + "-client"
                form.fields['route'].choices = SetRoute(form.data[client])

            data["formset"] = formset
        else:
            formset = IDIEditFormSet2(instance=self.object)
            for form in formset:
                form.fields['route'].choices = SetRoute(form.initial['client'])

            data["formset"] = formset

        data["text"] = "Редактирование приходника"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()

                formset.instance = self.object
                formset.save()
                return super(IncomeDebitsEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('debits:list_income')

def selectAgent(request):
    if request.is_ajax and request.method == "POST":
        try:
            obj = NumberOfPlaces.objects.filter(agent__pk=request.POST['agent_id'])
            objJ = {}

            for ob in obj:
                str1 = "(" + str(ob.recipient.pk) + "), " + ob.recipient.fullname
                objJ[ob.recipient.pk] = {'pk': ob.recipient.pk, "client": str1}

            return JsonResponse({'clients': objJ}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)


def selectClient(request):
    if request.is_ajax and request.method == "POST":
        try:
            pkC = request.POST['client_id']

            RT = ReceptionTransmission.objects.filter(recipient__pk=pkC, history=False)

            dict = {}
            for rt in RT:
                key = rt.route.pk
                if key in dict:
                    dict[key][0] = dict[key][0] + rt.remainder
                else:
                    dict[key] = [rt.remainder, rt.route]

            RET = []
            remainder = 0
            for key in dict:
                obj = NumberOfPlaces.objects.filter(recipient__pk=pkC, route__pk=key)
                for ob in obj:
                    dict[key][0] = dict[key][0] + ob.unloading
                route = dict[key][1]
                if dict[key][0] > 0:

                    remainder = remainder + dict[key][0]

                    RET.append({"pk": route.pk,
                                "text": str(route.idRoute) + " " + str(route.date.strftime('%Y')) + " - " + route.country_recipient.name
                                        +"(Долг: " + str(dict[key][0])+")"})


            return JsonResponse({'routes': RET, "remainder": remainder }, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)

# --------------------------------// SEARCH //------------------------------------------------------

class ClientReportView(LoginRequiredMixin, TemplateView):
    template_name = 'debits/pages/reportClient.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': ClientReportForm(),
                                                    'base_template_name': get_base_template_name(self.request.user)})

    def post(self, request, *args, **kwargs):
        form = ClientReportForm(request.POST)

        if form.is_valid():
            routeFrom = form.cleaned_data["routeFrom"]
            routeTo = form.cleaned_data["routeTo"]
            client = form.cleaned_data["client"]

            route = Route.objects.filter(country_recipient=form.cleaned_data["direction"])
            L, SUM_B = [], 0.0
            for r in route:
                L.append((r.pk, str(r.idRoute) + "(" + str(r.date.strftime('%Y')) + ")"))

            form.fields["routeFrom"].choices = L
            form.fields["routeTo"].choices = L

            beginning = ReceptionTransmission.objects.filter(Q(Q(route__lt=routeFrom.pk) | Q(route__gt=routeTo.pk)) &
                                                             Q(history=False) & Q(recipient=client))
            RoutesB = []

            for b in beginning:
                SUM_B += b.remainder
                if b.route not in RoutesB:
                    RoutesB.append(b.route)

            for r in RoutesB:
                try:
                    n = NumberOfPlaces.objects.get(route=r, recipient=client)
                    SUM_B += n.unloading
                except Exception as e:
                    print(e)

            RT = ReceptionTransmission.objects.filter(history=False,
                                                      route__pk__range=[routeFrom.pk, routeTo.pk],
                                                      recipient=client)

            L, dict, total1, total2 = [], {}, [0.0, 0, 0.0], 0.0
            for rt in RT:
                key = rt.route.pk
                ser1 = Services.objects.get(id_REC_TRAN=rt, service=0)
                ser2 = Services.objects.get(id_REC_TRAN=rt, service=1)

                if key in dict:
                    dict[key][2] += ser1.count
                    dict[key][3] += ser2.count
                    dict[key][4] += rt.remainder
                else:
                    dict[key] = [rt.route.idRoute,
                                 str(rt.route.date.date()),
                                 ser1.count,
                                 ser2.count,
                                 rt.remainder]
            for key in dict:
                try:
                    obj = NumberOfPlaces.objects.get(recipient=client,
                                                     route__pk=key)
                    dict[key][4] += obj.unloading
                except Exception as e:
                    print(e)

                total1[0] += dict[key][2]
                total1[1] += dict[key][3]
                total1[2] += dict[key][4]

            obj = IncomeDebitsInner.objects.filter(client=client)

            for ob in obj:
                L.append([ob.inner.pk, ob.route.idRoute, ob.sum, str(ob.inner.date)])
                total2 += ob.sum

            inf1 = client.fullname + " (" + str(client.pk) + ") c " + str(routeFrom.date.date()) + \
                   " по " + str(routeTo.date.date())
            total1[2] += SUM_B

            if 'print' in request.POST:
                html_string = render_to_string("debits/print/reportClient.html", {
                    "dict": dict,
                    "income": L,
                    "total1": total1,
                    "total2": total2,
                    "inf1": inf1,
                    "beginning": SUM_B,
                    "remainder_debt": total1[2] - total2
                })
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                    write_pdf(response, presentational_hints=True)
                return response

            else:
                return render(request, self.template_name, {"form": form,
                                                            "dict": dict,
                                                            "income": L,
                                                            "total1": total1,
                                                            "total2": total2,
                                                            "inf1": inf1,
                                                            "beginning": SUM_B,
                                                            "remainder_debt": total1[2]-total2,
                                                            'base_template_name': get_base_template_name(self.request.user)
                                                            })

        return render(request, self.template_name, {'form': form,
                                                    'base_template_name': get_base_template_name(self.request.user)})

class ClientReportTonnageView(LoginRequiredMixin, TemplateView):
    template_name = 'debits/pages/reportClientTonnage.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'form': ClientReportForm(),
                       'base_template_name': get_base_template_name(self.request.user)})

    def post(self, request, *args, **kwargs):
        form = ClientReportForm(request.POST)

        if form.is_valid():
            routeFrom = form.cleaned_data["routeFrom"]
            routeTo = form.cleaned_data["routeTo"]
            client = form.cleaned_data["client"]

            route = Route.objects.filter(country_recipient=form.cleaned_data["direction"])

            L = []
            for r in route:
                L.append((r.pk, str(r.idRoute) + "(" + str(r.date.strftime('%Y')) + ")"))

            form.fields["routeFrom"].choices = L
            form.fields["routeTo"].choices = L

            RT = ReceptionTransmission.objects.filter(history=False,
                                                      route__pk__range=[routeFrom.pk, routeTo.pk],
                                                      recipient=client)
            L, dict, total = [], {}, [0.0, 0]

            for rt in RT:
                key = rt.route.pk
                ser1 = Services.objects.get(id_REC_TRAN=rt, service=0)
                ser2 = Services.objects.get(id_REC_TRAN=rt, service=1)

                if key in dict:
                    dict[key][2] += ser1.count
                    dict[key][3] += ser2.count

                else:
                    dict[key] = [rt.route.idRoute,
                                 str(rt.route.date.date()),
                                 ser1.count,
                                 ser2.count]
            for key in dict:
                total[0] += dict[key][2]
                total[1] += dict[key][3]

            inf1 = client.fullname + " (" + str(client.pk) + ") c " + str(routeFrom.date.date()) + \
                   " по " + str(routeTo.date.date())

            if 'print' in request.POST:
                html_string = render_to_string("debits/print/reportClientTonnage.html", {
                    "dict": dict,
                    "inf1": inf1,
                    "total": total,
                })
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                    write_pdf(response, presentational_hints=True)
                return response

            return render(request, self.template_name, {"form": form,
                                                        "dict": dict,
                                                        "inf1": inf1,
                                                        "total": total,
                                                        'base_template_name': get_base_template_name(self.request.user)})

        return render(request, self.template_name,
                      {'form': form,
                       'base_template_name': get_base_template_name(self.request.user)})

class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'debits/pages/reports.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': ReportForm(),
                                                    'base_template_name': get_base_template_name(self.request.user)})

    def post(self, request, *args, **kwargs):
        form = ReportForm(request.POST)
        routesChoices = Route.objects.filter(country_recipient=request.POST["direction"])
        L, dict = [], {}
        L.append((-1, '---------'))

        for r in routesChoices:
            L.append((r.pk, str(r.idRoute) + "(" + str(r.date.strftime('%Y')) + ")"))
        form.fields["route"].choices = L

        if form.is_valid():
            agent = form.cleaned_data["agent"]
            direction = form.cleaned_data["direction"]
            routes = request.POST.getlist('route')

            if len(routes) == 0:
                routes = []
            if len(routes) == 1:
                if "-1" in routes:
                    routes = []
            if not agent:
                if not len(routes):
                    RT = ReceptionTransmission.objects.filter(history=False, route__country_recipient=direction)
                    numP = NumberOfPlaces.objects.filter(route__country_recipient=direction)

                else:
                    RT = ReceptionTransmission.objects.filter(history=False, route__in=routes)
                    numP = NumberOfPlaces.objects.filter(route__in=routes)

                for rt in RT:
                    key = rt.recipient
                    if key in dict:
                        dict[key][0] += rt.remainder
                    else:
                        dict[key] = [rt.remainder, 0.0]

                for np in numP:
                    SUM = np.unloading
                    key = np.recipient
                    if key in dict:
                        dict[key][0] += SUM

                if not len(routes):
                    for key in dict:
                        income = IncomeDebitsInner.objects.filter(
                            client=key,
                            route__country_recipient=direction)
                        for i in income:
                            dict[key][1] += i.sum
                else:
                    for key in dict:
                        income = IncomeDebitsInner.objects.filter(
                            client=key,
                            route__in=routes)
                        for i in income:
                            dict[key][1] += i.sum
            else:
                if not len(routes):
                    numP = NumberOfPlaces.objects.filter(route__country_recipient=direction, agent=agent)
                    print(numP)
                    for np in numP:
                        SUM = np.unloading
                        RT = ReceptionTransmission.objects.filter(
                            history=False,
                            route__country_recipient=direction,
                            recipient=np.recipient)
                        for rt in RT:
                            SUM += rt.remainder
                        key = np.recipient
                        if key in dict:
                            dict[key][0] += SUM
                        else:
                            dict[key] = [SUM, 0.0]

                    for key in dict:
                        income = IncomeDebitsInner.objects.filter(
                            client=key,
                            inner__agent=agent,
                            route__country_recipient=direction)

                        for i in income:
                            dict[key][1] += i.sum
                else:
                    numP = NumberOfPlaces.objects.filter(route__in=routes, agent=agent)
                    for np in numP:
                        SUM = np.unloading
                        RT = ReceptionTransmission.objects.filter(
                            history=False,
                            route__in=routes,
                            recipient=np.recipient)

                        for rt in RT:
                            SUM += rt.remainder

                        key = np.recipient

                        if key in dict:
                            dict[key][0] += SUM
                        else:
                            dict[key] = [SUM, 0.0]

                    for key in dict:
                        income = IncomeDebitsInner.objects.filter(
                            client=key,
                            inner__agent=agent,
                            route__in=routes)

                        for i in income:
                            dict[key][1] += i.sum

            if 'print' in request.POST:
                html_string = render_to_string("debits/print/reports.html", {"dict": dict})
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()). \
                    write_pdf(response, presentational_hints=True)
                return response
            else:
                return render(request, self.template_name, {"form": form, "dict": dict,
                                                            'base_template_name': get_base_template_name(
                                                                self.request.user)})

        return render(request, self.template_name, {'form': form,
                                                    'base_template_name': get_base_template_name(self.request.user)})


def showReportClientModal(request):
    if request.is_ajax and request.method == "POST":
        dict, L, total = {}, [], [0.0, 0.0, 0.0]

        routes = request.POST.getlist('routes[]')
        agent = request.POST['agent']
        clientID = request.POST['clientID']
        direction = request.POST['direction']

        client = Client.objects.get(pk=clientID)
        inf1 = "(" + str(client.clientID) + ") " + client.fullname

        if len(routes) == 0:
            routes = []

        if len(routes) == 1:
            if "-1" in routes:
                routes = []

        if not agent:
            if not len(routes):
                RT = ReceptionTransmission.objects.filter(history=False,
                                                          route__country_recipient=direction,
                                                          recipient=clientID)
                numP = NumberOfPlaces.objects.filter(route__country_recipient=direction,
                                                     recipient=clientID)
            else:
                RT = ReceptionTransmission.objects.filter(history=False, route__in=routes,
                                                          recipient=clientID)
                numP = NumberOfPlaces.objects.filter(route__in=routes, recipient=clientID)

            for rt in RT:
                key = rt.route

                if key in dict:
                    dict[key][0] += rt.remainder
                else:
                    dict[key] = [rt.remainder, 0.0, 0.0]

            for np in numP:
                key = np.route

                if key in dict:
                    dict[key][1] += np.unloading

            if not len(routes):
                income = IncomeDebitsInner.objects.filter(
                    client=clientID,
                    route__country_recipient=direction)

                for i in income:
                    key = i.route
                    if key in dict:
                        dict[key][2] += i.sum

                for key in dict:
                    L.append([str(key.idRoute) + "(" + str(key.date.strftime('%Y')) + ")",
                              dict[key][0], dict[key][1], dict[key][2]])

                    total[0] += dict[key][0]
                    total[1] += dict[key][1]
                    total[2] += dict[key][2]

            else:
                income = IncomeDebitsInner.objects.filter(
                    client=clientID,
                    route__in=routes)
                for i in income:
                    key = i.route
                    if key in dict:
                        dict[key][1] += i.sum

                for key in dict:
                    L.append([str(key.idRoute) + "(" + str(key.date.strftime('%Y')) + ")",
                              dict[key][0], dict[key][1], dict[key][2]])

                    total[0] += dict[key][0]
                    total[1] += dict[key][1]
                    total[2] += dict[key][2]

        else:
            if not len(routes):
                numP = NumberOfPlaces.objects.filter(route__country_recipient=direction,
                                                     agent=agent,
                                                     recipient=clientID)
                for np in numP:
                    RT = ReceptionTransmission.objects.filter(
                        history=False,
                        route__country_recipient=direction,
                        recipient=np.recipient)

                    for rt in RT:
                        key = rt.route
                        if key in dict:
                            dict[key][0] += rt.remainder
                        else:
                            dict[key] = [rt.remainder, 0.0, 0.0]

                    key = np.route
                    if key in dict:
                        dict[key][1] += np.unloading

                income = IncomeDebitsInner.objects.filter(
                    client=clientID,
                    inner__agent=agent,
                    route__country_recipient=direction)

                for i in income:
                    key = i.route
                    if key in dict:
                        dict[key][2] += i.sum

                for key in dict:
                    L.append([str(key.idRoute) + "(" + str(key.date.strftime('%Y')) + ")",
                              dict[key][0],
                              dict[key][1],
                              dict[key][2]])

                    total[0] += dict[key][0]
                    total[1] += dict[key][1]
                    total[2] += dict[key][2]
            else:
                print("here")

                numP = NumberOfPlaces.objects.filter(route__in=routes,
                                                     agent=agent,
                                                     recipient=clientID)
                for np in numP:
                    RT = ReceptionTransmission.objects.filter(
                        history=False,
                        route__in=routes,
                        recipient=np.recipient)

                    for rt in RT:
                        key = rt.route
                        if key in dict:
                            dict[key][0] += rt.remainder
                        else:
                            dict[key] = [rt.remainder, 0.0, 0.0]

                    key = np.route
                    if key in dict:
                        dict[key][1] += np.unloading

                income = IncomeDebitsInner.objects.filter(
                    client=clientID,
                    inner__agent=agent,
                    route__in=routes)

                for i in income:
                    key = i.route
                    if key in dict:
                        dict[key][2] += i.sum

                for key in dict:
                    L.append([str(key.idRoute) + "(" + str(key.date.strftime('%Y')) + ")",
                              dict[key][0],
                              dict[key][1],
                              dict[key][2]])

                    total[0] += dict[key][0]
                    total[1] += dict[key][1]
                    total[2] += dict[key][2]

        return JsonResponse({"L": L, "inf1": inf1, "total": total}, status=200)

    return JsonResponse({"error": "error"}, status=400)

def getRoute(request):
    if request.is_ajax and request.method == "POST":
        L = []
        route = Route.objects.filter(country_recipient__pk=request.POST['country_id'])

        for r in route:
            L.append([r.pk, str(r.idRoute) + "(" + str(r.date.strftime('%Y')) + ")"])

        return JsonResponse({'routes': L}, status=200)
    return JsonResponse({"error": "error"}, status=400)

