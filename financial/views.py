from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from .filters import ArticleFilter, OperationsViewFilter
from django.contrib import messages
from route.models import Currency
from django.core.paginator import Paginator
from route.views import get_base_template_name

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class CashBoxView(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/cash_boxes.html'

    def get(self, request, *args, **kwargs):

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

        return render(request, self.template_name, {'header': header,
                                                    'dict': dict,
                                                    'base_template_name': get_base_template_name(request.user)})


class CashBoxAddView(LoginRequiredMixin, CreateView):
    template_name = 'financial/forms/cash_boxes_add.html'
    form_class = CashBoxForm
    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:cash_box')

class ArticlesView(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/articles.html'

    def get(self, request, *args, **kwargs):
        f = ArticleFilter(request.GET, queryset=Articles.objects.all())

        paginator = Paginator(f.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class ArticlesViewAdd(LoginRequiredMixin, CreateView):
    template_name = 'financial/forms/articles_add.html'
    form_class = ArticlesForm

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:articles')

    def get_context_data(self, **kwargs):
        data = super(ArticlesViewAdd, self).get_context_data(**kwargs)
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

class ArticlesEditView(LoginRequiredMixin, UpdateView):
    template_name = 'financial/forms/article_edit.html'
    model = Articles
    form_class = ArticlesForm

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:articles')

    def get_context_data(self, **kwargs):
        data = super(ArticlesEditView, self).get_context_data(**kwargs)
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

@login_required
def article_delete(request, id):
    get_object_or_404(Articles, id=id).delete()
    messages.success(request, 'Запись под номером ' + str(id) + ' была успешно удалена')
    return redirect('financial:articles')

class OperationsView(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/operations.html'

    def get(self, request, *args, **kwargs):

        if request.user.role == 1 or request.user.role == 4:
            qs = Operations.objects.all()
        else:
            qs = Operations.objects.filter(added_by=request.user)

        f = OperationsViewFilter(request.GET, queryset=qs)
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class OperationsIncomeClientAdd(LoginRequiredMixin, CreateView):
    form_class = IncomeClientForm
    template_name = 'financial/forms/income_client.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsIncomeClientAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = IncomeClientInnerFormset(self.request.POST)
        else:
            data['formset'] = IncomeClientInnerFormset()
        data['text'] = 'Добавление приходника'
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
                return super(OperationsIncomeClientAdd, self).form_valid(form)

        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_income_ID', kwargs={'pk': self.object.pk})

class OperationsIncomeClientEdit(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = IncomeClientForm
    template_name = 'financial/forms/income_client.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsIncomeClientEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = IncomeClientInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = IncomeClientInnerFormset2(instance=self.object)

        data['text'] = 'Редактирование приходника'
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
                return super(OperationsIncomeClientEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_income_ID', kwargs={'pk': self.object.pk})

class OperationsIncomeAgentAdd(LoginRequiredMixin, CreateView):
    form_class = IncomeCounterpartyForm
    template_name = 'financial/forms/income_agent.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsIncomeAgentAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = IncomeCounterpartyInnerFormset2(self.request.POST)
        else:
            data['formset'] = IncomeCounterpartyInnerFormset()

        data['text'] = 'Добавление приходника'
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
                return super(OperationsIncomeAgentAdd, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_income_ID', kwargs={'pk': self.object.pk})


class OperationsIncomeAgentEdit(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = IncomeCounterpartyForm
    template_name = 'financial/forms/income_agent.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsIncomeAgentEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = IncomeCounterpartyInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = IncomeCounterpartyInnerFormset2(instance=self.object)

        data['text'] = 'Редактирование приходника'
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
                return super(OperationsIncomeAgentEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_income_ID', kwargs={'pk': self.object.pk})


class IncomeId(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/income.html'

    def get(self, request, *args, **kwargs):
        obj = Operations.objects.get(pk=kwargs['pk'])
        obj_inner = OperationsInner.objects.filter(inner=obj)
        context = {'obj': obj, 'obj_inner': obj_inner}
        context['base_template_name'] = get_base_template_name(request.user)
        return render(request, self.template_name, context)

class OperationsVarioustAdd(LoginRequiredMixin, CreateView):
    form_class = IncomeVariousForm
    template_name = 'financial/forms/income_various.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsVarioustAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = IncomeVariousInnerFormset(self.request.POST)
        else:
            data['formset'] = IncomeVariousInnerFormset()

        data['text'] = 'Добавление приходника'
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
                return super(OperationsVarioustAdd, self).form_valid(form)
        print(form.errors)
        print(formset.errors)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_income_ID', kwargs={'pk': self.object.pk})

class OperationsIncomeVariousEdit(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = IncomeVariousForm
    template_name = 'financial/forms/income_various.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsIncomeVariousEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = IncomeVariousInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = IncomeVariousInnerFormset2(instance=self.object)

        data['text'] = 'Редактирование приходника'
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
                return super(OperationsIncomeVariousEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_income_ID', kwargs={'pk': self.object.pk})

#-------------------------------------------------------

class ConsumptionEmployeeAdd(LoginRequiredMixin, CreateView):
    form_class = ConsumptionEmployeeForm
    template_name = 'financial/forms/consumption_employee.html'

    def get_context_data(self, **kwargs):
        data = super(ConsumptionEmployeeAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsumptionEmployeeInnerFormset2(self.request.POST)
        else:
            data['formset'] = ConsumptionEmployeeInnerFormset()

        data['text'] = 'Добавление расходника'
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
                return super(ConsumptionEmployeeAdd, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

class ConsEmployeeEdit(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = ConsumptionEmployeeForm
    template_name = 'financial/forms/consumption_employee.html'

    def get_context_data(self, **kwargs):
        data = super(ConsEmployeeEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsumptionEmployeeInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = ConsumptionEmployeeInnerFormset2(instance=self.object)

        data['text'] = 'Редактирование расходника'
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
                return super(ConsEmployeeEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

#-------------------------------------------------------

class ConsumptionAgentAdd(LoginRequiredMixin, CreateView):
    form_class = ConsumptionAgentForm
    template_name = 'financial/forms/consumption_agent.html'

    def get_context_data(self, **kwargs):
        data = super(ConsumptionAgentAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsumptionAgentInnerFormset2(self.request.POST)
        else:
            data['formset'] = ConsumptionAgentInnerFormset()

        data['text'] = 'Добавление расходника'
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
                return super(ConsumptionAgentAdd, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

class ConsumptionAgentEdit(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = ConsumptionAgentForm
    template_name = 'financial/forms/consumption_agent.html'

    def get_context_data(self, **kwargs):
        data = super(ConsumptionAgentEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsumptionAgentInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = ConsumptionAgentInnerFormset2(instance=self.object)

        data['text'] = 'Редактирование расходника'
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
                return super(ConsumptionAgentEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

#-------------------------------------------------------

class ConsAgentClientAdd(LoginRequiredMixin, CreateView):
    form_class = ConsAgentClientForm
    template_name = 'financial/forms/consumption_agent_client.html'

    def get_context_data(self, **kwargs):
        data = super(ConsAgentClientAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsAgentClientInnerFormset2(self.request.POST)
        else:
            data['formset'] = ConsAgentClientInnerFormset()
        data['text'] = 'Добавление расходника'
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
                return super(ConsAgentClientAdd, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

class ConsAgentClientEdit(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = ConsAgentClientForm
    template_name = 'financial/forms/consumption_agent_client.html'

    def get_context_data(self, **kwargs):
        data = super(ConsAgentClientEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsAgentClientInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = ConsAgentClientInnerFormset2(instance=self.object)

        data['text'] = 'Редактирование расходника'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()

                formset.instance = self.object
                formset.save()
                return super(ConsAgentClientEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

#-------------------------------------------------------

class OperationsConsVarioustAdd(LoginRequiredMixin, CreateView):
    form_class = ConsVariousForm
    template_name = 'financial/forms/consumption_various.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsConsVarioustAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsVariousInnerFormset2(self.request.POST)
        else:
            data['formset'] = ConsVariousInnerFormset()
        data['text'] = 'Добавление расходника'
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
                return super(OperationsConsVarioustAdd, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

class OperationsConsVarioustEdit(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = ConsVariousForm
    template_name = 'financial/forms/consumption_various.html'

    def get_context_data(self, **kwargs):
        data = super(OperationsConsVarioustEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ConsVariousInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = ConsVariousInnerFormset2(instance=self.object)
        data['text'] = 'Редактирование расходника'
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
                return super(OperationsConsVarioustEdit, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_cons_ID', kwargs={'pk': self.object.pk})

#-------------------------------------------------------

class PaymentStatementEmployeeAddView(LoginRequiredMixin, CreateView):
    form_class = PaymentStatementEmployeeForm
    template_name = 'financial/forms/payroll_employee.html'

    def get_context_data(self, **kwargs):
        data = super(PaymentStatementEmployeeAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = PSEmployeeInnerFormset2(self.request.POST)
        else:
            data['formset'] = PSEmployeeInnerFormset()
        data['label'] = 'Получатель (Сотрудники)'
        data['text'] = 'Добавление платежной ведомости'
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
                return super(PaymentStatementEmployeeAddView, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_payroll_ID', kwargs={'pk': self.object.pk})

class PaymentStatementEmployeeEditView(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = PaymentStatementEmployeeForm
    template_name = 'financial/forms/payroll_employee.html'

    def get_context_data(self, **kwargs):
        data = super(PaymentStatementEmployeeEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = PSEmployeeInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = PSEmployeeInnerFormset2(instance=self.object)

        data['label'] = 'Получатель (Сотрудники)'
        data['text'] = 'Редактирование'
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
                return super(PaymentStatementEmployeeEditView, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_payroll_ID', kwargs={'pk': self.object.pk})
#------------------------------------------------------------------------------------------------

class PaymentStatementAgentAddView(LoginRequiredMixin, CreateView):
    form_class = PaymentStatementAgentForm
    template_name = 'financial/forms/payroll_agent.html'

    def get_context_data(self, **kwargs):
        data = super(PaymentStatementAgentAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = PSAgentInnerFormset2(self.request.POST)
        else:
            data['formset'] = PSAgentInnerFormset()

        data['label'] = 'Получатель (Контрагенты)'
        data['text'] = 'Добавление платежной ведомости'
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
                return super(PaymentStatementAgentAddView, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:operations_payroll_ID', kwargs={'pk': self.object.pk})

class PaymentStatementAgentEditView(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = PaymentStatementAgentForm
    template_name = 'financial/forms/payroll_agent.html'

    def get_context_data(self, **kwargs):
        data = super(PaymentStatementAgentEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = PSAgentInnerFormset2(self.request.POST, instance=self.object)
        else:
            data['formset'] = PSAgentInnerFormset2(instance=self.object)

        data['label'] = 'Получатель (Контрагенты)'
        data['text'] = 'Редактирование'
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
                return super(PaymentStatementAgentEditView, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:operations_payroll_ID', kwargs={'pk': self.object.pk})


#--------------------------------------------------------------------------------------------
class OperationsConsCashMovingAdd(LoginRequiredMixin, CreateView):
    template_name = 'financial/forms/variouse_moving.html'
    form_class = CashMovingForm

    def get_context_data(self, **kwargs):
        data = super(OperationsConsCashMovingAdd, self).get_context_data(**kwargs)
        data['text'] = 'Добавление перемещения по кассам'
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('financial:cons_cash_moving_ID', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.added_by = self.request.user
        self.object.save()
        return super(OperationsConsCashMovingAdd, self).form_valid(form)



class OperationsConsCashMovingEdit(LoginRequiredMixin, UpdateView):
    template_name = 'financial/forms/variouse_moving.html'
    model = Operations
    form_class = CashMovingForm

    def get_context_data(self, **kwargs):
        data = super(OperationsConsCashMovingEdit, self).get_context_data(**kwargs)
        data['text'] = 'Редактирование перемещения по кассам'
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('financial:cons_cash_moving_ID', kwargs={'pk': self.object.pk})


#--------------------------------------------------------------------------------------------

class ConsumptionId(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/consumption.html'

    def get(self, request, *args, **kwargs):
        obj = Operations.objects.get(pk=kwargs['pk'])
        obj_inner = OperationsInner.objects.filter(inner=obj)

        context = {'obj': obj, 'obj_inner': obj_inner }
        context['base_template_name'] = get_base_template_name(request.user)

        return render(request, self.template_name, context)


class PayrollID(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/payroll.html'

    def get(self, request, *args, **kwargs):
        obj = Operations.objects.get(pk=kwargs['pk'])
        obj_inner = OperationsInner.objects.filter(inner=obj)
        context = {'obj': obj, 'obj_inner': obj_inner}
        context['base_template_name'] = get_base_template_name(request.user)
        return render(request, self.template_name, context)

class OperationsConsCashMovingID(LoginRequiredMixin, TemplateView):
    template_name = 'financial/pages/various_moving.html'

    def get(self, request, *args, **kwargs):
        obj = Operations.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, {'obj': obj,
                                                    'base_template_name': get_base_template_name(request.user)})

@login_required
def deleteOperations(request, pk):
    get_object_or_404(Operations, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('financial:operations')

def getArticle(request):
    if request.is_ajax and request.method == "POST":

        typeO = request.POST['typeO']
        art = Articles.objects.filter(type=typeO).values('pk', 'name')
        return JsonResponse({'articles': list(art)}, status=200)

    # some error occured
    return JsonResponse({"error": "error"}, status=400)

