from django import forms
from django.core.exceptions import ValidationError

from .models import *
from django.forms import formset_factory, inlineformset_factory
from djangoformsetjs.utils import formset_media_js

my_default_errors = {
    'required': 'Поле обязательно для заполнения',
    'invalid': 'Введите допустимое значение',
}

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('added_by',)
    required_css_class = 'required2'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('added_by',)

    def clean(self):
        cleaned_data = super().clean()
        salary = cleaned_data.get("salary")
        currency = cleaned_data.get("currency")

        if salary:
            if not currency:
                raise ValidationError("Валюта зарплаты не выбрана")

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['id'] = 'summernote'

class AgentOfClientForm(forms.ModelForm):
    required_css_class = 'required2'
    class Meta:
        model = AgentOfClient
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super(AgentOfClientForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs['class'] = 'select2'
        self.fields['description'].widget.attrs['id'] = 'summernote'


class SenderForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['fullname', 'country', 'inn', 'okpo', 'phone', 'address']


class SenderFullForm(forms.ModelForm):
    required_css_class = 'required2'
    class Meta:
        model = Client
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super(SenderFullForm, self).__init__(*args, **kwargs)

        self.fields['country'].widget.attrs['class'] = 'select2'
        self.fields['city'].widget.attrs['class'] = 'select2'
        self.fields['type'].disabled = True


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = 1
        self.fields['clientID'].required = True

class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super(ClientEditForm, self).__init__(*args, **kwargs)
        self.fields['type'].disabled = True
        self.fields['clientID'].disabled = True

class StoreOfClientForm(forms.ModelForm):
    class Meta:
        model = StoreOfClient
        fields = '__all__'
        error_messages = {
            'city': my_default_errors,
            'store': my_default_errors,
            'row': my_default_errors,
            'container': my_default_errors}

    class Media(object):
        js = formset_media_js

    def __init__(self, *arg, **kwarg):
        super(StoreOfClientForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False

class SendersOfClientForm(forms.ModelForm):
    class Meta:
        model = SendersOfClient
        fields = '__all__'

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(SendersOfClientForm, self).__init__(*args, **kwargs)
        self.fields['sender'].queryset = Client.objects.filter(type=2)

StoreOfClientFormset = inlineformset_factory(Client, StoreOfClient, form=StoreOfClientForm, extra=1, can_delete=True)
StoreOfClientFormset2 = inlineformset_factory(Client, StoreOfClient, form=StoreOfClientForm, extra=0, can_delete=True)
SendersOfClientFormset = inlineformset_factory(Client, SendersOfClient, fk_name='client_sender', form=SendersOfClientForm, extra=1, can_delete=True)
SendersOfClientFormset2 = inlineformset_factory(Client, SendersOfClient, fk_name='client_sender', form=SendersOfClientForm, extra=0, can_delete=True)
