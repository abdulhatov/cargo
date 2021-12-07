from django.db import transaction, IntegrityError
from route.models import ReceptionTransmission, Services
from django.db.models import Q
import weasyprint
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse

from route.views import get_base_template_name
from .forms import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import HttpResponse
from django.template.loader import get_template, render_to_string
from django.views.generic.edit import UpdateView, CreateView
from django.contrib import messages
from .filters import *
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class WarehouseAddView(LoginRequiredMixin, CreateView):
    form_class = AddListForm
    template_name = 'warehouse/forms/warehouse_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('warehouse:list_warehouse')

class WarehouseListView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/warehouse.html'
    def get(self, request, *args, **kwargs):
        f = AddListFilter(request.GET, queryset=AddList.objects.all())
        paginator = Paginator(f.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    model = AddList
    form_class = AddListForm
    template_name = 'warehouse/forms/warehouse_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('warehouse:list_warehouse')

@login_required
def deleteWarehose(request, pk):
    get_object_or_404(AddList, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('warehouse:list_warehouse')

class CategoryAddView(LoginRequiredMixin, CreateView):
    form_class = CategoryNameForm
    template_name = 'warehouse/forms/category_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('warehouse:list_category')


class CategoryListView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/category.html'

    def get(self, request, *args, **kwargs):
        f = CategoryNameFilter(request.GET, queryset=CategoryName.objects.all())

        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = CategoryName
    form_class = CategoryNameForm
    template_name = 'warehouse/forms/category_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('warehouse:list_category')

@login_required
def deleteCategory(request, pk):
    get_object_or_404(CategoryName, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('warehouse:list_category')

class NamingAddView(LoginRequiredMixin, CreateView):
    form_class = ListNameForm
    template_name = 'warehouse/forms/naming_add.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('warehouse:list_naming')

class NamingListView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/naming.html'
    def get(self, request, *args, **kwargs):

        f = ListNameFilter(request.GET, queryset=ListName.objects.all())

        paginator = Paginator(f.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class NamingUpdateView(LoginRequiredMixin, UpdateView):
    model = ListName
    form_class = ListNameForm
    template_name = 'warehouse/forms/naming_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('warehouse:list_naming')

@login_required
def deleteNaming(request, pk):
    get_object_or_404(ListName, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('warehouse:list_naming')

class BagReportView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/bag_report.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": BagReportForm()})

    def post(self, request, *args, **kwargs):
        context = {}
        form = BagReportForm(request.POST)

        if request.POST['direction']:
            routes = Route.objects.filter(country_recipient__pk=request.POST['direction'])
            routesOPT = []
            for r in routes:
                routesOPT.append((r.pk, str(r.idRoute) + ' (' + str(r.date.strftime('%Y')) + ')'))
            form.fields['routeFrom'].choices = routesOPT
            form.fields['routeTo'].choices = routesOPT

        context['form'] = form

        context['warehouse_title'] = request.POST['warehouse']
        context['dateFrom'] = request.POST['dateFrom']
        context['dateTo'] = request.POST['dateTo']

        if form.is_valid():
            warehouse = form.cleaned_data['warehouse']
            operation = form.cleaned_data['operation']
            dateFrom = form.cleaned_data['dateFrom']
            dateTo = form.cleaned_data['dateTo']
            routeFrom = form.cleaned_data['routeFrom']
            routeTo = form.cleaned_data['routeTo']

            obj = []

            if operation == "1":

                context['text'] ='Мешки, склад "' + warehouse.title + '", приход от ' + str(dateFrom) + ' по ' + str(dateTo)
                context['header'] = ['ID', 'Дата', 'Наименование', 'Количество', 'Сумма']
                if not routeFrom and not routeTo:
                    whIncomeS = WarehouseOperation.objects.filter(type=1, warehouse=warehouse, date__range=[dateFrom, dateTo])
                    sumS = 0
                    sum_price = 0
                    for w in whIncomeS:
                        wh_inner = WarehouseOperationInner.objects.filter(inner=w, category__title__iexact='Мешки')
                        if wh_inner:
                            for w_i in wh_inner:
                                obj.append([w_i.pk, str(w.date), w_i.name.title, w_i.sum, w_i.price*w_i.sum])
                                sumS = sumS + w_i.sum
                                sum_price = sum_price + w_i.price*w_i.sum
                    obj.append(['', '', 'Итого', sumS, sum_price])
                    context['obj'] = (obj)

                else:
                    obj.append(['', '', 'Итого', '0', '0'])
                    context['obj'] = obj

            elif operation == "2":

                if not routeFrom and not routeTo:
                    context['text'] = 'Мешки, склад "' + warehouse.title + '", расход от ' + str(dateFrom) + ' по ' + str(dateTo)
                    context['header'] = ['ID', 'Дата', 'Наименование', 'Количество', 'Сумма']
                    whConsumption = WarehouseOperation.objects.filter(type=2, warehouse=warehouse, date__range=[dateFrom, dateTo])

                    obj = []
                    sumS = 0
                    sum_price = 0
                    for w in whConsumption:
                        wh_inner = WarehouseOperationInner.objects.filter(inner=w, category__title__iexact='Мешки').order_by('name')
                        if wh_inner:
                            for w_i in wh_inner:
                                obj.append([w_i.pk, w.date, w_i.name, w_i.sum, w_i.price * w_i.sum])
                                sumS = sumS + w_i.sum
                                sum_price = sum_price + w_i.price * w_i.sum

                    obj.append(['', '', 'Итого', sumS, sum_price])
                    context['obj'] = obj

                elif request.POST['routeFrom'] and request.POST['routeTo']:
                    routeFrom_obj = Route.objects.get(pk=request.POST['routeFrom'])
                    routeTo_obj = Route.objects.get(pk=request.POST['routeTo'])
                    direction_obj = Direction.objects.get(pk=request.POST['direction'])

                    context['text'] = 'Мешки, склад "' + warehouse.title + '", расход по рейсам ' + direction_obj.name + ' c ' + str(routeFrom_obj.idRoute) + ' - ' + str(routeTo_obj.idRoute)

                    context['header'] = ['№ Рейса', 'Большой мешок', 'Средний мешок', 'Малый мешок']

                    RT = ReceptionTransmission.objects.filter(route__id__range=[routeFrom, routeTo], history=False)

                    sum_ser3 = 0
                    sum_ser4 = 0
                    sum_ser5 = 0

                    for rt in RT:
                        obj.append([
                            'Рейс №' + str(rt.pk),
                            Services.objects.get(id_REC_TRAN=rt, service='3').count,
                            Services.objects.get(id_REC_TRAN=rt, service='4').count,
                            Services.objects.get(id_REC_TRAN=rt, service='5').count
                        ])

                        sum_ser3 = sum_ser3 + Services.objects.get(id_REC_TRAN=rt, service='3').count
                        sum_ser4 = sum_ser4 + Services.objects.get(id_REC_TRAN=rt, service='4').count
                        sum_ser5 = sum_ser5 + Services.objects.get(id_REC_TRAN=rt, service='5').count

                    obj.append(['Всего:', sum_ser3, sum_ser4, sum_ser5])
                    context['obj'] = obj

            elif operation == "3":
                context['text'] = 'Мешки, склад "' + warehouse.title + '", перемещение от ' + str(dateFrom) + ' по ' + str(dateTo)
                context['header'] = ['ID', 'Дата', 'Наименование', 'Количество']
                if not routeFrom and not routeTo:
                    whMovingS = WarehouseOperation.objects.filter(type=3).\
                        filter(Q(from_warehouse=warehouse) | Q(to_the_warehouse=warehouse),
                               date__range=[dateFrom, dateTo])
                    sumS = 0

                    for w in whMovingS:
                        wh_inner = WarehouseOperationInner.objects.filter(inner=w, category__title__iexact='Мешки')
                        if wh_inner:
                            for w_i in wh_inner:
                                obj.append([w_i.pk, w.date, w_i.name, w_i.sum])
                                sumS = sumS + w_i.sum

                    obj.append(['', '', 'Итого', sumS])
                    context['obj'] = obj
                else:
                    obj.append(['', '', 'Итого', '0'])
                    context['obj'] = obj

            if "submit_button" in request.POST:
                return render(request, self.template_name, context)

            elif "print_button" in request.POST:
                html_string = render_to_string("warehouse/print/bag_report.html", context)
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                             presentational_hints=True)
                return response
        else:
            print(form.errors)
        return render(request, self.template_name, context)

class WHReportView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/wh_report.html'
    def get(self, request, *args, **kwargs):

        f = WHReportFilter(request.GET, queryset=WarehouseOperationInner.objects.all())

        paginator = Paginator(f.qs, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if "print_button" in request.GET:
            html_string = render_to_string("warehouse/print/wh_report.html", {"obj_list": f.qs})
            response = HttpResponse(content_type='application/pdf')
            weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                                 presentational_hints=True)
            return response

        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class OstatokView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/ostatok.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name,
                      {"form": OstatokForm(),
                       'base_template_name': get_base_template_name(self.request.user)})

    def post(self, request, *args, **kwargs):
        form = OstatokForm(request.POST)
        warehouse = AddList.objects.get(pk=request.POST['warehouse'])
        RT = ReceptionTransmission.objects.filter(registration__name__iexact=warehouse.title, history=False)

        WAREHOUSE = {}
        sum_ser3 = 0
        sum_ser4 = 0
        sum_ser5 = 0

        for rt in RT:
            sum_ser3 = sum_ser3 + Services.objects.get(id_REC_TRAN=rt, service='3').count
            sum_ser4 = sum_ser4 + Services.objects.get(id_REC_TRAN=rt, service='4').count
            sum_ser5 = sum_ser5 + Services.objects.get(id_REC_TRAN=rt, service='5').count


        WAREHOUSE['большой мешок'] = 0-sum_ser3
        WAREHOUSE['средний мешок'] = 0-sum_ser4
        WAREHOUSE['маленький мешок'] = 0-sum_ser5

        whInner = WarehouseOperationInner.objects.filter(inner__type=1, inner__warehouse=warehouse)

        for w in whInner:
            key = w.name.title.lower()

            if key in WAREHOUSE:
                WAREHOUSE[key] += w.sum
            else:
                WAREHOUSE[key] = w.sum

        whConsInner = WarehouseOperationInner.objects.filter(inner__type=2, inner__warehouse=warehouse)

        for w in whConsInner:
            key = w.name.title.lower()
            if key in WAREHOUSE:
                WAREHOUSE[key] -= w.sum
            else:
                WAREHOUSE[key] = 0 - w.sum

        whmovingInner = WarehouseOperationInner.objects.filter(inner__type=3, inner__from_warehouse=warehouse)

        for w in whmovingInner:
            key = w.name.title.lower()
            if key in WAREHOUSE:
                WAREHOUSE[key] -= w.sum
            else:
                WAREHOUSE[key] = 0 - w.sum

        whmovingInner2 = WarehouseOperationInner.objects.filter(inner__type=3, inner__warehouse=warehouse)

        for w in whmovingInner2:
            key = w.name.title.lower()

            if key in WAREHOUSE:
                WAREHOUSE[key] += w.sum
            else:
                WAREHOUSE[key] = w.sum

        if "print_button" in request.POST:
            html_string = render_to_string("warehouse/print/ostatok.html", {'WAREHOUSE': WAREHOUSE,
                                                    'wh_selected': warehouse})

            response = HttpResponse(content_type='application/pdf')
            weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response,
                                                                                                 presentational_hints=True)
            return response

        return render(request, self.template_name, {'form': form,
                                                    'WAREHOUSE': WAREHOUSE,
                                                    'wh_selected': warehouse,
                                                    'base_template_name': get_base_template_name(self.request.user)})

class WHOperatiosView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/operations.html'
    def get(self, request, *args, **kwargs):

        if request.user.role == 1:
            qs = WarehouseOperation.objects.all()
        else:
            qs = WarehouseOperation.objects.filter(added_by=request.user)

        f = WarehouseOperationFilter(request.GET, queryset=qs)
        paginator = Paginator(f.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})


class WHIncomeAddView(LoginRequiredMixin, CreateView):
    form_class = WHIncomeForm
    template_name = 'warehouse/forms/wh_income.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('warehouse:wh_operations')

    def get_context_data(self, **kwargs):
        data = super(WHIncomeAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['whInnerFormset'] = WHIncomeInnerFormSet(self.request.POST)
        else:
            data['whInnerFormset'] = WHIncomeInnerFormSet()
        data['text'] = 'Приходник в склад'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        whinners = context['whInnerFormset']

        with transaction.atomic():
            if whinners.is_valid():
                self.object = form.save(commit=False)
                self.object.added_by = self.request.user
                self.object.save()

                whinners.instance = self.object
                whinners.save()

                return super(WHIncomeAddView, self).form_valid(form)
        print(whinners)
        return self.render_to_response(self.get_context_data())

class WHIncomeEditView(LoginRequiredMixin, UpdateView):
    model = WarehouseOperation
    form_class = WHIncomeForm
    template_name = 'warehouse/forms/wh_income.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('warehouse:wh_operations')

    def get_context_data(self, **kwargs):
        data = super(WHIncomeEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['whInnerFormset'] = WHIncomeInnerFormSet2(self.request.POST, instance=self.object)
        else:
            data['whInnerFormset'] = WHIncomeInnerFormSet2(instance=self.object)
        data['text'] = 'Редактирование приходника в склад'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        whinners = context['whInnerFormset']

        with transaction.atomic():
            if whinners.is_valid():
                self.object = form.save()

                whinners.instance = self.object
                whinners.save()

                return super(WHIncomeEditView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())


class WHConsumptionEditView(LoginRequiredMixin, UpdateView):
    model = WarehouseOperation
    form_class = WHConsumptionForm
    template_name = 'warehouse/forms/wh_consumption.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('warehouse:wh_operations')

    def get_context_data(self, **kwargs):
        data = super(WHConsumptionEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['wHConsumptionFormSet'] = WHConsumptionFormSet2(self.request.POST, instance=self.object)
        else:
            data['wHConsumptionFormSet'] = WHConsumptionFormSet2(instance=self.object)

        data['text'] = 'Редактирование расходника в склад'
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        wHConsumptionFormSet = context['wHConsumptionFormSet']

        with transaction.atomic():
            if wHConsumptionFormSet.is_valid():
                self.object = form.save()

                wHConsumptionFormSet.instance = self.object
                wHConsumptionFormSet.save()
                return super(WHConsumptionEditView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())

@login_required
def operationDelete(request, pk):
    get_object_or_404(WarehouseOperation, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('warehouse:wh_operations')

class WHConsumptionAddView(LoginRequiredMixin, CreateView):
    form_class = WHConsumptionForm
    template_name = 'warehouse/forms/wh_consumption.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('warehouse:wh_operations')

    def get_context_data(self, **kwargs):
        data = super(WHConsumptionAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['wHConsumptionFormSet'] = WHConsumptionFormSet(self.request.POST)
        else:
            data['wHConsumptionFormSet'] = WHConsumptionFormSet()

        data['text'] = 'Расходник в склад'
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        wHConsumptionFormSet = context['wHConsumptionFormSet']

        with transaction.atomic():
            if wHConsumptionFormSet.is_valid():
                self.object = form.save(commit=False)
                self.object.added_by = self.request.user
                self.object.save()

                wHConsumptionFormSet.instance = self.object
                wHConsumptionFormSet.save()
                return super(WHConsumptionAddView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())


class ConsumablesWarehouseView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/viewConsumablesWarehouse.html'

    def get(self, request, *args, **kwargs):
        whConsumption = WarehouseOperation.objects.get(pk=kwargs['pk'])
        wh_income_inner = WarehouseOperationInner.objects.filter(inner=whConsumption)
        context = {
            "id": whConsumption.id,
            "date": whConsumption.date,
            "warehouse": whConsumption.warehouse.title,
            'route': str(whConsumption.route.pk) + " - " + whConsumption.route.country_recipient.name,
            'client': whConsumption.client.fullname,
            'clientID': whConsumption.client.pk,
        }
        whConsumptionRT = []
        for w_i in wh_income_inner:
            whConsumptionRT.append({
                'id': w_i.pk,
                'name': w_i.name.title,
                'category': w_i.category.title+"("+w_i.category.unit+")",
                'count': w_i.sum,
                'price': w_i.price,
                'sum': w_i.sum*w_i.price
            })
            context['whConsumption'] = whConsumptionRT
        context['base_template_name'] = get_base_template_name(self.request.user)
        return render(request, self.template_name, context)

class IncomeWarehouseView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/viewIncomeWarehouse.html'

    def get(self, request, *args, **kwargs):
        whIncome = WarehouseOperation.objects.get(pk=kwargs['pk'])
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

        return render(self.request, self.template_name, context)

class MovingWarehouseView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/viewMovingWarehouse.html'

    def get(self, request, *args, **kwargs):
        whMoving = WarehouseOperation.objects.get(pk=kwargs['pk'])
        wh_inner = WarehouseOperationInner.objects.filter(inner=whMoving)
        context = {
            "id": whMoving.id,
            "date": whMoving.date,
            "to_the_warehouse": whMoving.warehouse.title,
            "from_warehouse": whMoving.from_warehouse.title,
            "whInner": wh_inner,
        }
        return render(request, self.template_name, context)


class IncomeWarehouseCashierView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/pages/viewIncomeWHCashier.html'

    def get(self, request, *args, **kwargs):

        whIncome = WarehouseOperation.objects.get(pk=kwargs['pk'])

        context = {
            "id": whIncome.id,
            "date": str(whIncome.date),
            "wh_article": whIncome.wh_article.name,
            "sumS": whIncome.sum,
            "added_by": whIncome.added_by.first_name + " " + whIncome.added_by.last_name
        }
        return render(request, self.template_name, context)


def selectListName(request):
    if request.is_ajax and request.method == "POST":
        try:
            category_id = request.POST['category_id']

            listName = ListName.objects.filter(category__id=category_id)

            listNameJ = []
            for ln in listName:
                listNameJ.append({'listNameID': ln.pk, 'listNameTitle': ln.title})

            return JsonResponse({'listName': listNameJ}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class WHMovingAddView(LoginRequiredMixin, CreateView):
    form_class = WHMovingForm
    template_name = 'warehouse/forms/wh_moving.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('warehouse:wh_operations')

    def get_context_data(self, **kwargs):
        data = super(WHMovingAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['wHMovingFormSet'] = WHMovingFormSet(self.request.POST)
        else:
            data['wHMovingFormSet'] = WHMovingFormSet()

        data['text'] = 'Добавление перемещения по складам'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        wHMovingFormSet = context['wHMovingFormSet']

        with transaction.atomic():
            if wHMovingFormSet.is_valid():
                self.object = form.save(commit=False)
                self.object.added_by = self.request.user
                self.object.save()

                wHMovingFormSet.instance = self.object
                wHMovingFormSet.save()
                return super(WHMovingAddView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())


class WHMovingEditView(LoginRequiredMixin, UpdateView):
    model = WarehouseOperation
    form_class = WHMovingForm
    template_name = 'warehouse/forms/wh_moving.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('warehouse:wh_operations')

    def get_context_data(self, **kwargs):
        data = super(WHMovingEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['wHMovingFormSet'] = WHMovingFormSet2(self.request.POST, instance=self.object)
        else:
            data['wHMovingFormSet'] = WHMovingFormSet2(instance=self.object)

        data['text'] = 'Редактирование перемещения по складам'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        wHMovingFormSet = context['wHMovingFormSet']

        with transaction.atomic():
            if wHMovingFormSet.is_valid():
                self.object = form.save()

                wHMovingFormSet.instance = self.object
                wHMovingFormSet.save()
                return super(WHMovingEditView, self).form_valid(form)

        return self.render_to_response(self.get_context_data())

def load_routes(request):
    country_id = request.POST['country']
    routes = Route.objects.filter(country_recipient__pk=country_id).order_by('date')
    routesJS = []
    for route in routes:
        routesJS.append({
            'pk': route.pk,
            'text': str(route.idRoute) + '(' + str(route.date.strftime('%Y')) +')',
        })
    return JsonResponse({'routes': routesJS}, status=200)


