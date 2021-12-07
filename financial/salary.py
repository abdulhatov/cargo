from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction
from .filters import SalaryFilter
from django.contrib import messages
from route.models import ReceptionTransmission, Inspector, Packer, Loader
from django.http import JsonResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class SalaryView(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/salary.html'

    def get(self, request, *args, **kwargs):
        f = SalaryFilter(request.GET, queryset=Salary.objects.all())
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class SalaryViewID(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/salary_id.html'

    def get(self, request, *args, **kwargs):
        context = {}
        salary = Salary.objects.get(pk=kwargs['pk'])
        context["salary"] = salary
        context["currency"] = SalaryCurrency.objects.filter(salary=salary)
        context["inner"] = SalaryInner.objects.filter(salary=salary)

        return render(request, self.template_name, context)

class SalaryAddView(LoginRequiredMixin, TemplateView):
    template_name = 'financial/forms/salary_add.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': SalaryForm()})

    def post(self, request, *args, **kwargs):
        form = SalaryForm(request.POST)
        employees = Employee.objects.all()

        SalaryInnerFormset = inlineformset_factory(Salary, SalaryInner, form=SalaryInnerForm,
                                                   extra=employees.count())

        if "button1" in request.POST:

            if form.is_valid():
                currency = form.cleaned_data['currency']
                dateFrom = form.cleaned_data['dateFrom']
                dateTo = form.cleaned_data['dateTo']

                inspection = form.cleaned_data['inspection']
                packing = form.cleaned_data['packing']
                loading = form.cleaned_data['loading']

                list_Currency = []

                for e in employees:
                    if e.currency:
                        if e.currency.pk != currency.pk:
                            if {"currency": e.currency} not in list_Currency:
                                list_Currency.append({"currency": e.currency})

                    fine = OperationsInner.objects.filter(
                        inner__type2=4,
                        article__name__iexact='Штрафы Сотрудников',
                        inner__employee=e,
                        inner__date__range=[dateFrom, dateTo],
                    )

                    for c in fine:
                        if c.inner.currency.pk != currency.pk:
                            if {"currency": c.inner.currency} not in list_Currency:
                                list_Currency.append({"currency": c.inner.currency})

                    advance = OperationsInner.objects.filter(
                        inner__type2=4,
                        article__name__iexact='Расходы по оплате труда',
                        inner__employee=e,
                        inner__date__range=[dateFrom, dateTo],
                    )
                    for c in advance:
                        if c.inner.currency != currency:
                            if {"currency": c.inner.currency} not in list_Currency:
                                list_Currency.append({"currency": c.inner.currency})

                if len(list_Currency) > 0:
                    SalaryCurrencyFormset1 = inlineformset_factory(Salary, SalaryCurrency, form=SalaryCurrencyForm,
                                                                   extra=len(list_Currency))
                    return render(request, self.template_name, {'form': form,
                                                                "currencyFormset": SalaryCurrencyFormset1(initial=list_Currency)})
                else:
                    initial = []
                    RT = ReceptionTransmission.objects.filter(dateRT__range=[dateFrom, dateTo], history=False)

                    LoadDict = {}

                    for rt in RT:
                        load = Loader.objects.filter(route=rt.route)
                        count = load.count()
                        for l in load:
                            key = l.name.pk
                            if key in LoadDict:
                                LoadDict[key] = LoadDict[key] + rt.pogr * loading / count
                            else:
                                LoadDict[key] = rt.pogr * loading / count

                    for employee in employees:
                        Serv = 0.0

                        ins = Inspector.objects.filter(id_REC_TRAN__in=RT, employee=employee)
                        for i in ins:
                            count = Inspector.objects.filter(id_REC_TRAN=i.id_REC_TRAN,
                                                             id_REC_TRAN__history=False).count()
                            Serv = Serv + (i.id_REC_TRAN.pogr * inspection / count)

                        pac = Packer.objects.filter(id_REC_TRAN__in=RT, employee=employee)
                        for p in pac:
                            count = Packer.objects.filter(id_REC_TRAN=p.id_REC_TRAN,
                                                          id_REC_TRAN__history=False).count()
                            Serv = Serv + (p.id_REC_TRAN.pogr * packing / count)

                        key = employee.pk
                        if key in LoadDict:
                            Serv = Serv + LoadDict[key]

                        cons = OperationsInner.objects.filter(
                            inner__type2=4,
                            article__name__iexact='Штрафы Сотрудников',
                            inner__employee=employee,
                            inner__date__range=[dateFrom, dateTo])

                        fine = 0.0
                        for c in cons:
                            fine = fine + c.sum

                        adv = OperationsInner.objects.filter(
                            inner__type2=4,
                            article__name__iexact='Расходы по оплате труда',
                            inner__employee=employee,
                            inner__date__range=[dateFrom, dateTo])

                        advance = 0.0
                        for c in adv:
                            advance = advance + c.sum

                        initial.append({'employee': employee,
                                        "debt": 0.0,
                                        "oklad": employee.salary,
                                        "premiums": 0.0,
                                        "other": 0.0,
                                        "interest": 0.0,
                                        "issuance": 0.0,
                                        "fine": round(fine, 4),
                                        "services": round(Serv, 4),
                                        "advance": round(advance, 4),
                                        "totalSL": 0.0,
                                        "remainder": 0.0,
                                        "total": 0.0})

                    return render(request, self.template_name, {
                        'form': form,
                        'formset': SalaryInnerFormset(initial=initial)})

            return render(request, self.template_name, {'form': form})

        elif "button2" in request.POST:
            formset = SalaryCurrencyFormset(request.POST, request.FILES)

            if form.is_valid() and formset.is_valid():

                currency = form.cleaned_data['currency']
                dateFrom = form.cleaned_data['dateFrom']
                dateTo = form.cleaned_data['dateTo']

                inspection = form.cleaned_data['inspection']
                packing = form.cleaned_data['packing']
                loading = form.cleaned_data['loading']

                currencyD = {}

                for f in formset:
                    currencyD[f.cleaned_data['currency']] = f.cleaned_data['curs']

                initial = []

                RT = ReceptionTransmission.objects.filter(dateRT__range=[dateFrom, dateTo], history=False)

                LoadDict = {}

                for rt in RT:
                    load = Loader.objects.filter(route=rt.route)
                    count = load.count()
                    for l in load:
                        key = l.name.pk
                        if key in LoadDict:
                            LoadDict[key] = LoadDict[key] + rt.pogr * loading / count
                        else:
                            LoadDict[key] = rt.pogr * loading / count

                for employee in employees:
                    Serv = 0.0

                    ins = Inspector.objects.filter(id_REC_TRAN__in=RT, employee=employee)
                    for i in ins:
                        count = Inspector.objects.filter(id_REC_TRAN=i.id_REC_TRAN,
                                                         id_REC_TRAN__history=False).count()
                        Serv = Serv + (i.id_REC_TRAN.pogr * inspection / count)

                    pac = Packer.objects.filter(id_REC_TRAN__in=RT, employee=employee)
                    for p in pac:
                        count = Packer.objects.filter(id_REC_TRAN=p.id_REC_TRAN,
                                                      id_REC_TRAN__history=False).count()
                        Serv = Serv + (p.id_REC_TRAN.pogr * packing / count)

                    key = employee.pk
                    if key in LoadDict:
                        Serv = Serv + LoadDict[key]

                    cons = OperationsInner.objects.filter(
                        inner__type2=4,
                        article__name__iexact='Штрафы Сотрудников',
                        inner__employee=employee,
                        inner__date__range=[dateFrom, dateTo])

                    fine = 0.0
                    for c in cons:
                        if c.inner.currency in currencyD:
                            fine = fine + c.sum * currencyD[c.inner.currency]
                        else:
                            fine = fine + c.sum

                    adv = OperationsInner.objects.filter(
                        inner__type2=4,
                        article__name__iexact='Расходы по оплате труда',
                        inner__employee=employee,
                        inner__date__range=[dateFrom, dateTo])

                    advance = 0.0
                    for c in adv:
                        if c.inner.currency in currencyD:
                            advance = advance + c.sum * currencyD[c.inner.currency]

                    if employee.currency in currencyD:
                        empSalary = employee.salary * currencyD[employee.currency]
                    else:
                        empSalary = employee.salary

                    if empSalary:
                        empSalary = round(empSalary, 4)

                    initial.append({'employee': employee,
                                    "debt": 0.0,
                                    "oklad": empSalary,
                                    "premiums": 0.0,
                                    "other": 0.0,
                                    "interest": 0.0,
                                    "issuance": 0.0,
                                    "fine": round(fine, 4),
                                    "services": Serv,
                                    "advance": round(advance, 4),
                                    "totalSL": 0.0,
                                    "remainder": 0.0,
                                    "total": 0.0})

                return render(request, self.template_name, {
                    'form': form,
                    'currencyFormset': formset,
                    'formset': SalaryInnerFormset(initial=initial),
                })

            return render(request, self.template_name, {
                    'form': form,
                    'currencyFormset': formset
                })
        elif "button3" in request.POST:
            salaryInnerFormset = SalaryInnerFormset(request.POST)

            context = {}

            if 'salarycurrency_set-TOTAL_FORMS' in request.POST:
                formset = SalaryCurrencyFormset(request.POST, request.FILES)
                context['currencyFormset'] = formset

            if form.is_valid() and salaryInnerFormset.is_valid():
                object = form.save()

                if 'salarycurrency_set-TOTAL_FORMS' in request.POST:
                    formset = SalaryCurrencyFormset(request.POST, request.FILES)

                    if formset.is_valid():
                        formset.instance = object
                        formset.save()

                salaryInnerFormset.instance = object
                OBJ = salaryInnerFormset.save()

                for obj in OBJ:
                    dateFrom = form.cleaned_data['dateFrom']
                    dateTo = form.cleaned_data['dateTo']
                    inspection = float(form.cleaned_data['inspection'])
                    packing = float(form.cleaned_data['packing'])
                    loading = float(form.cleaned_data['loading'])

                    employee = obj.employee

                    RT = ReceptionTransmission.objects.filter(history=False, dateRT__range=[dateFrom, dateTo])

                    dict = {}
                    ins = Inspector.objects.filter(employee=employee, id_REC_TRAN__in=RT)

                    for i in ins:
                        count = Inspector.objects.filter(id_REC_TRAN__history=False,
                                                         id_REC_TRAN=i.id_REC_TRAN).count()
                        share = i.id_REC_TRAN.pogr * inspection / count
                        key = i.id_REC_TRAN.route.country_recipient
                        if key in dict:
                            dict[key][0] = dict[key][0] + share
                        else:
                            dict[key] = [share, 0.0, 0.0]

                    packers = Packer.objects.filter(employee=employee, id_REC_TRAN__in=RT)
                    for packer in packers:
                        count = Packer.objects.filter(id_REC_TRAN__history=False,
                                                      id_REC_TRAN=packer.id_REC_TRAN).count()
                        share = packer.id_REC_TRAN.pogr * packing / count
                        key = packer.id_REC_TRAN.route.country_recipient
                        if key in dict:
                            dict[key][1] = dict[key][1] + share
                        else:
                            dict[key] = [0.0, share, 0.0]

                    for rt in RT:
                        load = Loader.objects.filter(name=employee, route=rt.route)
                        count = load.count()

                        for l in load:
                            key = l.route.country_recipient
                            if key in dict:
                                dict[key][2] = dict[key][2] + rt.pogr * loading / count
                            else:
                                dict[key] = [0.0, 0.0, rt.pogr * loading / count]

                    for k in dict:
                        ServicesSalary(country=k,
                                       inspection=dict[k][0],
                                       packing=dict[k][1],
                                       loading=dict[k][2],
                                       employee=employee,
                                       salary=object).save()
                messages.success(self.request, "Запись успешно добавлена")
                return redirect('financial:salary')

            context['form'] = form
            context['formset'] = salaryInnerFormset
            return render(request, self.template_name, context)

class SalaryEditView(LoginRequiredMixin, UpdateView):
    model = Salary
    form_class = SalaryEditForm
    template_name = 'financial/forms/salary_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:salary')

    def get_context_data(self, **kwargs):
        data = super(SalaryEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['currencyFormset'] = SalaryCurrencyEditFormset(self.request.POST, instance=self.object)
            data['formset'] = SalaryInnerFormset0(self.request.POST, instance=self.object)
        else:
            data['currencyFormset'] = SalaryCurrencyEditFormset(instance=self.object)
            data['formset'] = SalaryInnerFormset0(instance=self.object)

        data["PK"] = self.object.pk
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        currencyFormset = context['currencyFormset']
        formset = context['formset']

        with transaction.atomic():
            if currencyFormset.is_valid() and formset.is_valid():
                self.object = form.save()
                currencyFormset.instance = self.object
                currencyFormset.save()
                formset.instance = self.object
                formset.save()
                return super(SalaryEditView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())

def showEmployeeModal(request):

    if request.is_ajax and request.method == "POST":

        empID = request.POST['empID']
        currency = request.POST['currency']
        dateFrom = request.POST['dateFrom']
        dateTo = request.POST['dateTo']
        inspection = float(request.POST['inspection'])
        packing = float(request.POST['packing'])
        loading = float(request.POST['loading'])

        employee = Employee.objects.get(pk=empID)
        RT = ReceptionTransmission.objects.filter(history=False, dateRT__range=[dateFrom, dateTo])

        dict = {}
        ins = Inspector.objects.filter(employee=employee, id_REC_TRAN__in=RT)

        for i in ins:
            count = Inspector.objects.filter(id_REC_TRAN__history=False,
                                             id_REC_TRAN=i.id_REC_TRAN).count()
            share = i.id_REC_TRAN.pogr * inspection / count
            key = i.id_REC_TRAN.route.country_recipient.name
            if key in dict:
                dict[key][0] = dict[key][0] + share
            else:
                dict[key] = [share, 0.0, 0.0]

        packers = Packer.objects.filter(employee=employee, id_REC_TRAN__in=RT)
        for packer in packers:
            count = Packer.objects.filter(id_REC_TRAN__history=False,
                                          id_REC_TRAN=packer.id_REC_TRAN).count()
            share = packer.id_REC_TRAN.pogr * packing / count
            key = packer.id_REC_TRAN.route.country_recipient.name
            if key in dict:
                dict[key][1] = dict[key][1] + share
            else:
                dict[key] = [0.0, share, 0.0]

        for rt in RT:
            load = Loader.objects.filter(name=employee, route=rt.route)
            count = load.count()

            for l in load:
                key = l.route.country_recipient.name
                if key in dict:
                    dict[key][2] = dict[key][2] + rt.pogr * loading / count
                else:
                    dict[key] = [0.0, 0.0, rt.pogr * loading / count]

        s = "(" + str(employee.employeeID) + ") " + employee.fullname

        total = [0.0, 0.0, 0.0]

        for k in dict:
            total[0] = total[0] + dict[k][0]
            total[1] = total[1] + dict[k][1]
            total[2] = total[2] + dict[k][2]

        sum = total[0]+total[1]+total[2]

        if employee.phone:
            s = s + ", " + employee.phone

        data = {
            "inf1": s,
            "inf2": str(dateFrom) + " - " + str(dateTo),
            "total": total,
            "sum": sum,
            "dict": dict,
        }
        return JsonResponse(data, status=200)

    # some error occured
    return JsonResponse({"error": "error"}, status=400)

def showEmployeeEditModal(request):

    if request.is_ajax and request.method == "POST":

        empID = request.POST['empID']
        employee = Employee.objects.get(id=empID)
        salaryID = request.POST['salaryID']
        salary = Salary.objects.get(pk=salaryID)

        OBJ = ServicesSalary.objects.filter(salary_id=salaryID, employee=employee)

        dict = {}
        for obj in OBJ:
            key = obj.country.name
            dict[key] = [obj.inspection, obj.packing, obj.loading]


        total = [0.0, 0.0, 0.0]

        for k in dict:
            total[0] = total[0] + dict[k][0]
            total[1] = total[1] + dict[k][1]
            total[2] = total[2] + dict[k][2]

        sum = total[0]+total[1]+total[2]

        s = "(" + str(employee.employeeID) + ") " + employee.fullname
        if employee.phone:
            s = s + ", " + employee.phone

        data = {
            "inf1": s,
            "inf2": "c " + str(salary.dateFrom) + " по " + str(salary.dateTo),
            "total": total,
            "sum": sum,
            "dict": dict,
        }
        return JsonResponse(data, status=200)

    return JsonResponse({"error": "error"}, status=400)

@login_required
def deleteSalary(request, pk):
    get_object_or_404(Salary, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('financial:salary')