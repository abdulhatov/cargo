from django import forms
from .models import *
from django.forms import ModelForm, DateInput, BaseFormSet
from django.forms import formset_factory, inlineformset_factory
from djangoformsetjs.utils import formset_media_js

my_default_errors = {
    'required': 'Поле обязательно для заполнения',
    'invalid': 'Введите допустимое значение',
}

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'status': forms.CheckboxInput(attrs={"data-off-color": "danger",
                                                        "data-on-color": "success",
                                                        "data-on-text": "открыт",
                                                        "data-off-text": "закрыт"}),

                   'control_status': forms.CheckboxInput(attrs={"data-off-color":"danger",
                                                                "data-on-color":"success",
                                                                "data-on-text":"закрыт",
                                                                "data-off-text": "открыт"}),

                   'status_places': forms.CheckboxInput(attrs={"data-off-color": "danger",
                                                               "data-on-color": "success",
                                                               "data-on-text": "открыт",
                                                               "data-off-text": "закрыт"})
                   }

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget.attrs['id'] = 'summernote'



class RouteUpdateForm(forms.ModelForm):
    class Meta:
        model = Route
        exclude = ('idRoute',)
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'status': forms.CheckboxInput(attrs={"data-off-color": "danger",
                                                        "data-on-color": "success",
                                                        "data-on-text": "открыт",
                                                        "data-off-text": "закрыт"}),

                   'control_status': forms.CheckboxInput(attrs={"data-off-color": "danger",
                                                        "data-on-color": "success",
                                                        "data-on-text": "открыт",
                                                        "data-off-text": "закрыт"}),

                   'status_places': forms.CheckboxInput(attrs={"data-off-color": "danger",
                                                        "data-on-color": "success",
                                                        "data-on-text": "открыт",
                                                        "data-off-text": "закрыт"})
                   }

    def __init__(self, *args, **kwargs):
        super(RouteUpdateForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget.attrs['id'] = 'summernote'

class ReceptionTransmissionForm(forms.ModelForm):
    class Meta:
        model = ReceptionTransmission
        exclude = ('services', 'history', 'operator', 'pogr')
        widgets = {'dateRT': DateInput(attrs={'type': 'datetime-local'}, format=('%Y-%m-%d %H:%M')),
                   # 'route': forms.Select(attrs={'onchange': 'jsFunction();'})
                   }

    def __init__(self, *args, **kwargs):
        super(ReceptionTransmissionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['route'].queryset = Route.objects.filter(status=True)
        self.fields['sender'].queryset = Client.objects.filter(type=2)
        self.fields['recipient'].queryset = Client.objects.filter(type=1)
        self.fields['paid'].widget.attrs['readonly'] = True
        self.fields['remainder'].widget.attrs['readonly'] = True

class RegistrationForm(forms.ModelForm):
    required_css_class = 'required2'
    class Meta:
        model = Registration
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['id'] = 'summernote'

class DirectionsForm(forms.ModelForm):
    required_css_class = 'required2'

    class Meta:
        model = Direction
        fields = '__all__'


class CurrencyForm(forms.ModelForm):
    required_css_class = 'required2'
    class Meta:
        model = Currency
        fields = '__all__'
        required_css_class = 'required2'

class FinancialReportForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Direction.objects.all(), to_field_name='pk', label='Направление',
                                     widget=forms.Select(attrs={'onchange': 'DirectionOnChange(this.value);'}))
    routeFrom = forms.ChoiceField(choices='', label='Рейс От')
    routeTo = forms.ChoiceField(choices='', label='Рейс До')
    registration = forms.ModelChoiceField(queryset=Registration.objects.all(), label='Место оформления')


class LoaderForm(forms.ModelForm):
    class Meta:
        model = Loader
        fields = '__all__'

    class Media(object):
        js = formset_media_js

LoaderFormSet = inlineformset_factory(Route, Loader, form=LoaderForm, extra=0, can_delete=True)

class InspectorForm(forms.ModelForm):
    class Meta:
        model = Inspector
        exclude = ('share',)

    class Media(object):
        js = formset_media_js + (
            # Здесь другие носители формы
        )

InspectorFormSet = inlineformset_factory(ReceptionTransmission, Inspector, form=InspectorForm, extra=1, can_delete=True)

InspectorFormSet2 = inlineformset_factory(ReceptionTransmission, Inspector, form=InspectorForm,
                                          extra=0, can_delete=True)

class PackerForm(forms.ModelForm):
    class Meta:
        model = Packer
        exclude = ('share',)

    class Media(object):
        js = formset_media_js

PackerFormSet = inlineformset_factory(ReceptionTransmission, Packer, form=PackerForm, extra=1, can_delete=True)

PackerFormSet2 = inlineformset_factory(ReceptionTransmission, Packer, form=PackerForm, extra=0, can_delete=True)

class ProductPForm(forms.ModelForm):
    class Meta:
        model = ProductP
        fields = '__all__'
        exclude = ()
        widgets = {
            'bag_number': forms.NumberInput(attrs={'oninput': 'CounterBagNumber();', 'onblur': 'onblurBagNumber(this.id)'}),
            'count': forms.NumberInput(attrs={'oninput': 'CounterCount();'}),
            'weight': forms.NumberInput(attrs={'oninput': 'CounterWeight();'}),
        }
        error_messages = {
            'product': my_default_errors,
            'bag_number': my_default_errors,
            'count': my_default_errors,
            'weight': my_default_errors,
        }

    def __init__(self, *args, **kwargs):
        super(ProductPForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    class Media(object):
        js = formset_media_js

ProductPFormSet = inlineformset_factory(ReceptionTransmission, ProductP, form=ProductPForm,
                                        extra=0,
                                        min_num=1,
                                        max_num=100,
                                        validate_min=True,
                                        can_delete=True)

ProductPFormSet2 = inlineformset_factory(ReceptionTransmission, ProductP, form=ProductPForm,
                                         min_num=1, extra=0, validate_min=True, can_delete=True)


class ServicesForm(forms.ModelForm):
    priceSom = forms.FloatField(widget=forms.NumberInput(attrs={'oninput': 'EventPriceSom(this.id);'}),
                                initial=0.0, required=True, error_messages=my_default_errors)
    sumPriseIV = forms.FloatField(initial=0.0, required=True)
    sumSom = forms.FloatField(initial=0.0, required=True)
    class Meta:
        model = Services
        fields = '__all__'
        exclude = ()
        widgets = {
            'count': forms.NumberInput(attrs={'oninput': 'ControllerSum();'}),
            'priceIV': forms.NumberInput(attrs={'oninput': 'EventPriceIV(this.id);'}),
            'status': forms.CheckboxInput(attrs={'onchange': 'ControllerSum();',
                                                 "data-off-color": "default",
                                                 "data-on-color": "success",
                                                 "data-on-text": "Оплачен",
                                                 "data-off-text": "Не оплачен"})
        }
        error_messages = {
            'service': my_default_errors,
            'count': my_default_errors,
            'priceIV': my_default_errors
        }

    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Media(object):
        js = formset_media_js

ServicesFormSet = inlineformset_factory(ReceptionTransmission, Services, form=ServicesForm, extra=8)
ServicesFormSet2 = inlineformset_factory(ReceptionTransmission, Services, form=ServicesForm, extra=0)

class ServicePriceForm(ModelForm):
    class Meta:
        model = ServicePrice
        fields = '__all__'
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}

    def __init__(self, *args, **kwargs):
        super(ServicePriceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = '__all__'
        exclude = ()
        error_messages = {
            'service': my_default_errors,
            'country': my_default_errors,
            'currency': my_default_errors,
            'price': my_default_errors
        }


    def __init__(self, *args, **kwargs):
        super(PriceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Media(object):
        js = formset_media_js

PriceFormSet = inlineformset_factory(ServicePrice, Price, form=PriceForm, extra=1, can_delete=True)
PriceFormSet2 = inlineformset_factory(ServicePrice, Price, form=PriceForm, extra=0, can_delete=True)

class NumberOfPlacesForm(forms.ModelForm):
    class Meta:
        model = NumberOfPlaces
        exclude = ('route',)
        error_messages = {
            'agent': {
                'required': 'Агент не выбран',
                'invalid': 'Введите допустимое значение'},
            'unloading': {
                'required': 'Цена разгрузки должна быть числом',
                'invalid': 'Цена разгрузки должна быть числом'}
        }

    def __init__(self, *args, **kwargs):
        super(NumberOfPlacesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-sm p-lg-0  fs-6'

        self.fields['recipient'].widget = forms.HiddenInput()

NumberOfPlacesFormSet = formset_factory(NumberOfPlacesForm, extra=0)