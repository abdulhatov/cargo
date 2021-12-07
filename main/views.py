from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from .forms import *
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from route.views import get_base_template_name
from .filters import *
from django.core.paginator import Paginator
from route.models import ReceptionTransmission, Route
from .models import Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'extends/index.html'

    def get_template_names(self):
        if self.request.user.role == 2:
            template_name = 'extends/index_sub_admin.html'
        elif self.request.user.role == 3:
            template_name = 'extends/index_operator.html'
        elif self.request.user.role == 4:
            template_name = 'extends/index_accountant.html'
        elif self.request.user.role == 5:
            template_name = 'extends/index_agent.html'
        elif self.request.user.role == 6:
            template_name = 'extends/index_client.html'
        else:
            template_name = self.template_name
        return [template_name]

    def get_context_data(self, **kwargs):
        rt = ReceptionTransmission.objects.count()
        route = Route.objects.count()
        recipient = Client.objects.filter(type=1).count()
        sender = Client.objects.filter(type=2).count()

        return {
            "rt": rt,
            'route': route,
            'recipient': recipient,
            'sender': sender
        }

class Products(LoginRequiredMixin, TemplateView):
    template_name = 'main/pages/products.html'
    def get(self, request, *args, **kwargs):

        if request.user.role == 1:
            qs = Product.objects.all()
        else:
            qs = Product.objects.filter(added_by=request.user)

        f = ProductFilter(request.GET, queryset=qs)

        paginator = Paginator(f.qs, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class ProductAddView(LoginRequiredMixin, CreateView):
    template_name = 'main/forms/product.html'
    form_class = ProductsForm

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('main:products')

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            data = super(ProductAddView, self).get_context_data(**kwargs)
            data['text'] = "Добавление продукта"
            data['base_template_name'] = get_base_template_name(self.request.user)
            return data
        else:
            return redirect('login')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.object = form.save(commit=False)
            self.object.added_by = self.request.user
            self.object.save()
            return super(ProductAddView, self).form_valid(form)
        else:
            return redirect('login')

@login_required
def deleteProduct(request, pk):
    get_object_or_404(Product, pk=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('main:products')


class ProductEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/forms/product.html"
    model = Product
    form_class = ProductsForm

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('main:products')

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            data = super(ProductEditView, self).get_context_data(**kwargs)
            data['text'] = "Редактирование продукта"
            data['base_template_name'] = get_base_template_name(self.request.user)
            return data
        return redirect('login')

@login_required
def add_sender(request):
    if request.is_ajax and request.method == "POST":
        form = SenderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.added_by = request.user
            instance.type = 2
            instance.save()
            return JsonResponse({"pk": instance.pk, "fullname": instance.fullname}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=401)
    return JsonResponse({"error": "error"}, status=400)

@login_required
def load_senders(request):
    if request.is_ajax and request.method == "POST":
        senders = Client.objects.filter(type=2)

        sendersJ = []
        for s in senders:
            sendersJ.append({'pk': s.pk, 'fullname': s.fullname})

        return JsonResponse({'senders': sendersJ}, status=200)
    return JsonResponse({"error": 'error'}, status=400)


class SenderAddView(LoginRequiredMixin, CreateView):
    form_class = SenderForm
    template_name = 'main/forms/client.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('main:senders')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.object = form.save(commit=False)
            self.object.added_by = self.request.user
            self.object.save()
            return super(SenderAddView, self).form_valid(form)
        else:
            return redirect('login')

class SenderEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/forms/sender_edit.html"
    model = Client
    form_class = SenderFullForm

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('main:clients')

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            data = super(SenderEditView, self).get_context_data(**kwargs)
            data['base_template_name'] = get_base_template_name(self.request.user)
            return data
        else:
            return redirect('login')

class ClientListView(LoginRequiredMixin, TemplateView):
    template_name = 'main/pages/clients.html'
    def get(self, request, *args, **kwargs):

        if request.user.role == 1:
            qs = Client.objects.all()
        else:
            qs = Client.objects.filter(added_by=request.user)

        f = ClientFilter(request.GET, queryset=qs)

        paginator = Paginator(f.qs, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})



class ClientAddView(LoginRequiredMixin, CreateView):
    form_class = ClientForm
    template_name = 'main/forms/client.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('main:clients')

    def get_context_data(self, **kwargs):
        data = super(ClientAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['storeformset'] = StoreOfClientFormset2(self.request.POST)
            data['senderformset'] = SendersOfClientFormset2(self.request.POST)
        else:
            data['storeformset'] = StoreOfClientFormset2()
            data['senderformset'] = SendersOfClientFormset2()
            data['senders_form'] = SenderForm()

        data["text"] = 'Добавление клиента'
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            context = self.get_context_data()
            storeformset = context['storeformset']
            senderformset = context['senderformset']

            with transaction.atomic():
                if storeformset.is_valid() and senderformset.is_valid():
                    self.object = form.save(commit=False)
                    self.object.added_by = self.request.user
                    self.object.save()

                    storeformset.instance = self.object
                    storeformset.save()

                    senderformset.instance = self.object
                    senderformset.save()

                    return super(ClientAddView, self).form_valid(form)

            return self.render_to_response(self.get_context_data())
        else:
            return redirect('login')

class ClientEditView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientEditForm
    template_name = 'main/forms/client.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('main:clients')

    def get_context_data(self, **kwargs):
        data = super(ClientEditView, self).get_context_data(**kwargs)

        if self.request.POST:
            data['storeformset'] = StoreOfClientFormset2(self.request.POST, instance=self.object)
            data['senderformset'] = SendersOfClientFormset2(self.request.POST, instance=self.object)

        else:
            data['storeformset'] = StoreOfClientFormset2(instance=self.object)
            data['senderformset'] = SendersOfClientFormset2(instance=self.object)
            data['senders_form'] = SenderForm()

        data["text"] = 'Редактирование клиента'
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        storeformset = context['storeformset']
        senderformset = context['senderformset']

        with transaction.atomic():
            if storeformset.is_valid() and senderformset.is_valid():
                self.object = form.save()

                storeformset.instance = self.object
                storeformset.save()

                senderformset.instance = self.object
                senderformset.save()
                return super(ClientEditView, self).form_valid(form)
        return self.render_to_response(self.get_context_data())

@login_required
def delete_client(request, pk):
    get_object_or_404(Client, id=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('main:clients')

class EmployeeListView(LoginRequiredMixin, TemplateView):
    template_name = 'main/pages/employees.html'
    def get(self, request, *args, **kwargs):
        if request.user.role == 1:
            qs = Employee.objects.all()
        else:
            qs = Employee.objects.filter(added_by=request.user)

        f = EmployeeFilter(request.GET, queryset=qs)
        paginator = Paginator(f.qs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class EmployeeAdd(LoginRequiredMixin, CreateView):
    form_class = EmployeeForm
    template_name = 'main/forms/employee.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('main:employees')

    def get_context_data(self, **kwargs):
        data = super(EmployeeAdd, self).get_context_data(**kwargs)
        data['text'] = "Добавление сотрудника"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.added_by = self.request.user
        self.object.save()
        return super(EmployeeAdd, self).form_valid(form)

class EmployeeEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/forms/employee.html"
    model = Employee
    form_class = EmployeeForm

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('main:employees')

    def get_context_data(self, **kwargs):
        data = super(EmployeeEditView, self).get_context_data(**kwargs)
        data['text'] = "Редактирование сотрудника"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

@login_required
def delete_employee(request, pk):
    get_object_or_404(Employee, id=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('main:employees')


class AgentOfClients(LoginRequiredMixin, TemplateView):
    template_name = 'main/pages/contrageny.html'
    def get(self, request, *args, **kwargs):
        if request.user.role == 1:
            qs = AgentOfClient.objects.all()
        else:
            qs = AgentOfClient.objects.filter(added_by=request.user)

        f = AgentOfClientFilter(request.GET, queryset=qs)
        paginator = Paginator(f.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj,
                                                    'base_template_name': get_base_template_name(request.user)})

class AgentOfClientAddView(LoginRequiredMixin, CreateView):
    template_name = 'main/forms/contrageny.html'
    form_class = AgentOfClientForm

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('main:contrageny')

    def get_context_data(self, **kwargs):
        data = super(AgentOfClientAddView, self).get_context_data(**kwargs)
        data['text'] = "Добавление контрагента"

        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.added_by = self.request.user
        self.object.save()
        return super(AgentOfClientAddView, self).form_valid(form)

class AgentOfClientEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/forms/contrageny.html"
    model = AgentOfClient
    form_class = AgentOfClientForm

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('main:contrageny')

    def get_context_data(self, **kwargs):
        data = super(AgentOfClientEditView, self).get_context_data(**kwargs)
        data['text'] = "Редактирование контрагента"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

@login_required
def delete_agenty(request, pk):
    get_object_or_404(AgentOfClient, id=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('main:contrageny')

