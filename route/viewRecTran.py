from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
from .views import get_base_template_name
from django.urls import reverse, reverse_lazy
import json
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import SenderForm

class ReceptionTransmissionAddView(LoginRequiredMixin, CreateView):
    form_class = ReceptionTransmissionForm
    template_name = 'route/forms/reception_transmission.html'

    def get_success_url(self):
        messages.success(self.request, "Запись успешно добавлена")
        return reverse_lazy('route:list_rt')

    def get_context_data(self, **kwargs):
        data = super(ReceptionTransmissionAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['inspectors'] = InspectorFormSet(self.request.POST)
            data['packers'] = PackerFormSet(self.request.POST)
            data['products'] = ProductPFormSet2(self.request.POST)
            data['services'] = ServicesFormSet(self.request.POST)
            data['pogr'] = self.request.POST['services_set-1-count']
            data['currency_recipient'] = self.request.POST['currency_recipient']
            data['currency_Som'] = self.request.POST['currency_Som']

            data['bag_number_count'] = self.request.POST['bag_number_count']
            data['count_sum'] = self.request.POST['count_sum']
            data['weight_sum'] = self.request.POST['weight_sum']

        else:
            data['inspectors'] = InspectorFormSet()
            data['packers'] = PackerFormSet()
            data['senders_form'] = SenderForm()
            data['products'] = ProductPFormSet2()
            data['currency_recipient'] = ""
            data['currency_Som'] = "0.0"

            data['bag_number_count'] = "0"
            data['count_sum'] = "0"
            data['weight_sum'] = "0.0"

            initial_service = []
            for i in range(0, 8):
                initial_service.append({'service': i,
                                        'count': 0,
                                        'priceIV': 0.00,
                                        'status': False,
                                        'priceSom': 0.00,
                                        'sumPriseIV': 0.00,
                                        'sumSom': 0.00})
            data['services'] = ServicesFormSet(initial=initial_service)

        data['text'] = "Добавление Акта Прием / Передач"
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inspectors = context['inspectors']
        packers = context['packers']
        products = context['products']
        services = context['services']
        pogr = int(context['pogr'])

        with transaction.atomic():
            if inspectors.is_valid() and packers.is_valid() and products.is_valid() and services.is_valid():
                try:
                    self.object = form.save(commit=False)
                    self.object.operator = self.request.user
                    self.object.pogr = pogr
                    self.object.save()

                    inspectors.instance = self.object
                    inspectors.save()

                    packers.instance = self.object
                    packers.save()

                    products.instance = self.object
                    products.save()

                    services.instance = self.object
                    services.save()
                    return super(ReceptionTransmissionAddView, self).form_valid(form)
                except Exception as e:
                    print(e)
                    messages.error(self.request, 'Произошла ошибка!')
        print(products.non_form_errors())
        return self.render_to_response(self.get_context_data())

class ReceptionTransmissionEditView(LoginRequiredMixin, UpdateView):
    model = ReceptionTransmission
    form_class = ReceptionTransmissionForm
    template_name = 'route/forms/reception_transmission.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('route:list_rt')

    def get_context_data(self, **kwargs):
        data = super(ReceptionTransmissionEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['inspectors'] = InspectorFormSet(self.request.POST, instance=self.object)
            data['packers'] = PackerFormSet(self.request.POST, instance=self.object)
            data['products'] = ProductPFormSet(self.request.POST, instance=self.object)
            data['services'] = ServicesFormSet(self.request.POST, instance=self.object)
            data['pogr'] = self.request.POST['services_set-1-count']
            data['currency_recipient'] = self.request.POST['currency_recipient']
            data['currency_Som'] = self.request.POST['currency_Som']

            data['bag_number_count'] = self.request.POST['bag_number_count']
            data['count_sum'] = self.request.POST['count_sum']
            data['weight_sum'] = self.request.POST['weight_sum']

        else:
            data['inspectors'] = InspectorFormSet2(instance=self.object)
            data['packers'] = PackerFormSet2(instance=self.object)
            data['products'] = ProductPFormSet2(instance=self.object)
            data['services'] = ServicesFormSet2(instance=self.object)
            data['currency_recipient'] = self.object.route.currency_recipient.name
            data['currency_Som'] = self.object.route.currency_Som

            bN = []
            countSum = 0
            weightSum = 0

            obj = ProductP.objects.filter(recTranID=self.object)
            for ob in obj:
                if ob.bag_number not in bN:
                    bN.append(ob.bag_number)
                countSum = countSum + ob.count
                weightSum = weightSum + ob.weight

            data['bag_number_count'] = len(bN)
            data['count_sum'] = countSum
            data['weight_sum'] = weightSum

        data['text'] = 'Редактирование Акта Прием / Передач'
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inspectors = context['inspectors']
        packers = context['packers']
        products = context['products']
        services = context['services']
        pogr = int(context['pogr'])

        with transaction.atomic():
            if inspectors.is_valid() and packers.is_valid() and products.is_valid() and services.is_valid():
                self.object = form.save(commit=False)
                self.object.operator = self.request.user
                self.object.pogr = pogr
                self.object.save()

                inspectors.instance = self.object
                inspectors.save()

                packers.instance = self.object
                packers.save()

                products.instance = self.object
                products.save()

                services.instance = self.object
                services.save()
                return super(ReceptionTransmissionEditView, self).form_valid(form)
        return self.render_to_response(self.get_context_data())


