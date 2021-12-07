import datetime

from django import forms
from .models import *
from django.forms import DateInput
from django.forms import inlineformset_factory
from djangoformsetjs.utils import formset_media_js
from route.models import Route

my_default_errors = {
    'required': 'Поле обязательно для заполнения',
    'invalid': 'Введите допустимое значение',
}

class CashBoxForm(forms.ModelForm):
    required_css_class = 'required2'
    class Meta:
        model = CashBox
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CashBoxForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['id'] = 'summernote'


class ArticlesForm(forms.ModelForm):
    required_css_class = 'required2'
    class Meta:
        model = Articles
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArticlesForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['id'] = 'summernote'

class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {'dateFrom': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'dateTo': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SalaryEditForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {'dateFrom': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'dateTo': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}

    def __init__(self, *args, **kwargs):
        super(SalaryEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['readonly'] = True

class SalaryCurrencyForm(forms.ModelForm):
    class Meta:
        model = SalaryCurrency
        fields = '__all__'
        error_messages = {
            'currency': my_default_errors,
            'curs': my_default_errors}

    def __init__(self, *args, **kwargs):
        super(SalaryCurrencyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Media(object):
        js = formset_media_js

class SalaryCurrencyEditForm(forms.ModelForm):
    class Meta:
        model = SalaryCurrency
        fields = '__all__'
        error_messages = {
            'currency': my_default_errors,
            'curs': my_default_errors}

    def __init__(self, *args, **kwargs):
        super(SalaryCurrencyEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.disabled = True

    class Media(object):
        js = formset_media_js


class SalaryInnerForm(forms.ModelForm):
    class Meta:
        model = SalaryInner
        fields = '__all__'
        widgets = {
            "debt": forms.NumberInput(attrs={'oninput': 'salaryDebt(this.id);'}),
            "oklad": forms.NumberInput(attrs={'oninput': 'salaryOklad(this.id);'}),
            "premiums": forms.NumberInput(attrs={'oninput': 'salaryPremiums(this.id);'}),
            "other": forms.NumberInput(attrs={'oninput': 'salaryOther(this.id);'}),
            "interest": forms.NumberInput(attrs={'oninput': 'salaryInterest(this.id);'}),
            "issuance": forms.NumberInput(attrs={'oninput': 'salaryIssuance(this.id);'}),
        }

        error_messages = {
            'debt': my_default_errors,
            'oklad': my_default_errors,
            "premiums": my_default_errors,
            "other": my_default_errors,
            "interest": my_default_errors,
            "issuance": my_default_errors,
            "fine": my_default_errors,
            "advance": my_default_errors,
            "services": my_default_errors,
            "totalSL": my_default_errors,
            "remainder": my_default_errors,
            "total": my_default_errors
        }

    def __init__(self, *args, **kwargs):
        super(SalaryInnerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control p-lg-0'

        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['totalSL'].widget.attrs['readonly'] = True
        self.fields['advance'].widget.attrs['readonly'] = True
        self.fields['fine'].widget.attrs['readonly'] = True
        self.fields['remainder'].widget.attrs['readonly'] = True

    class Media(object):
        js = formset_media_js

SalaryCurrencyFormset = inlineformset_factory(Salary, SalaryCurrency, form=SalaryCurrencyForm, extra=0)
SalaryCurrencyEditFormset = inlineformset_factory(Salary, SalaryCurrency, form=SalaryCurrencyEditForm, extra=0)
SalaryInnerFormset0 = inlineformset_factory(Salary, SalaryInner, form=SalaryInnerForm, extra=0)

class  IncomeClientForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'article', 'currency', 'route', 'client', 'description', 'type', 'sum', 'type2']
        widgets = {'date': DateInput(attrs={'type': 'datetime-local'}, format=('%Y-%m-%d %H:%M')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(IncomeClientForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Articles.objects.filter(type=1)
        self.fields['article'].required = True
        self.fields['type'].initial = 1
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 1
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['client'].required = True
        self.fields['sum'].widget.attrs['readonly'] = True

class IncomeClientInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['check', 'client', 'route', 'sum', 'article']
        widgets = {
            'sum': forms.NumberInput(attrs={'oninput': 'controllerSum();'}),
        }
        error_messages = {
            'check': my_default_errors,
            'client': my_default_errors,
            'route': my_default_errors,
            'sum': my_default_errors,
            'article': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(IncomeClientInnerForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Articles.objects.filter(type=1)
        self.empty_permitted = False
        self.fields['article'].required = True


IncomeClientInnerFormset = inlineformset_factory(Operations, OperationsInner, form=IncomeClientInnerForm, extra=1, can_delete=True)
IncomeClientInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=IncomeClientInnerForm, extra=0, can_delete=True)

#___________________________________________________________________________________________________________

class  IncomeCounterpartyForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'article', 'currency', 'route', 'agent', 'description', 'type', 'sum', 'type2']

        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(IncomeCounterpartyForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Articles.objects.filter(type=1)
        self.fields['type'].initial = 1
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 2
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['agent'].required = True
        self.fields['article'].required = True
        self.fields['sum'].widget.attrs['readonly'] = True

class IncomeCounterpartyInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['check', 'route', 'sum', 'article']
        widgets = {
            'sum': forms.NumberInput(attrs={'oninput': 'controllerSum();'}),
        }
        error_messages = {
            'check': my_default_errors,
            'route': my_default_errors,
            'sum': my_default_errors,
            'article': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(IncomeCounterpartyInnerForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Articles.objects.filter(type=1)
        self.empty_permitted = False
        self.fields['article'].required = True

IncomeCounterpartyInnerFormset = inlineformset_factory(Operations, OperationsInner, form=IncomeCounterpartyInnerForm, extra=1, can_delete=True)
IncomeCounterpartyInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=IncomeCounterpartyInnerForm, extra=0, can_delete=True)
#----------------------------------------------------------------------------------------

class IncomeVariousForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = [ 'cash', 'article', 'currency', 'route', 'various', 'description', 'type', 'sum', 'type2']

        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(IncomeVariousForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Articles.objects.filter(type=1)
        self.fields['type'].initial = 1
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 3
        self.fields['various'].required = True
        self.fields['article'].required = True
        self.fields['sum'].widget.attrs['readonly'] = True

class IncomeVariousInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['check', 'client', 'route', 'sum', 'article']
        widgets = {
            'sum': forms.NumberInput(attrs={'oninput': 'controllerSum();'}),
        }
        error_messages = {
            'check': my_default_errors,
            'client': my_default_errors,
            'route': my_default_errors,
            'sum': my_default_errors,
            'article': my_default_errors
        }
    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(IncomeVariousInnerForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Articles.objects.filter(type=1)
        self.empty_permitted = False
        self.fields['article'].required = True

IncomeVariousInnerFormset = inlineformset_factory(Operations, OperationsInner, form=IncomeVariousInnerForm, extra=1, can_delete=True)
IncomeVariousInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=IncomeVariousInnerForm, extra=0, can_delete=True)

#--------------------------------------------------------------------------------------------------------

class ConsumptionEmployeeForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'currency', 'route', 'employee', 'sum', 'description', 'type', 'type2']
        widgets = {
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(ConsumptionEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['type'].initial = 2
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 4
        self.fields['employee'].required = True


class ConsumptionEmployeeInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['count', 'price', 'sum', 'article', 'note']
        widgets = {
            'count': forms.NumberInput(attrs={'oninput': 'controllerSum_count(this.id);'}),
            'price': forms.NumberInput(attrs={'oninput': 'controllerSum_price(this.id);'}),
        }
        error_messages = {
            'count': my_default_errors,
            'price': my_default_errors,
            'sum': my_default_errors,
            'article': my_default_errors,
            'note': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(ConsumptionEmployeeInnerForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Articles.objects.filter(type=2)
        self.fields['sum'].widget.attrs['readonly'] = True
        self.empty_permitted = False
        self.fields['article'].required = True


ConsumptionEmployeeInnerFormset = inlineformset_factory(Operations, OperationsInner, form=ConsumptionEmployeeInnerForm, extra=1, can_delete=True)
ConsumptionEmployeeInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=ConsumptionEmployeeInnerForm, extra=0, can_delete=True)

#_____________________________________________________________________________________________

class ConsumptionAgentForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'currency', 'route', 'agent', 'description', 'sum', 'type', 'type2']
        widgets = {
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(ConsumptionAgentForm, self).__init__(*args, **kwargs)
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['type'].initial = 2
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 5
        self.fields['agent'].required = True

class ConsumptionAgentInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['count', 'price', 'sum', 'article', 'note']
        widgets = {
            'count': forms.NumberInput(attrs={'oninput': 'controllerSum_count(this.id);'}),
            'price': forms.NumberInput(attrs={'oninput': 'controllerSum_price(this.id);'}),
        }
        error_messages = {
            'count': my_default_errors,
            'price': my_default_errors,
            'sum': my_default_errors,
            'article': my_default_errors,
            'note': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(ConsumptionAgentInnerForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['article'].queryset = Articles.objects.filter(type=2)
        self.fields['article'].required = True


ConsumptionAgentInnerFormset = inlineformset_factory(Operations, OperationsInner, form=ConsumptionAgentInnerForm, extra=1, can_delete=True)
ConsumptionAgentInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=ConsumptionAgentInnerForm, extra=0, can_delete=True)

#_____________________________________________________________________________________________

class ConsAgentClientForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'currency', 'route', 'agentClient', 'sum', 'description', 'type', 'type2']

        widgets = {
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(ConsAgentClientForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = 2
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 6
        self.fields['agentClient'].required = True
        self.fields['sum'].widget.attrs['readonly'] = True



class ConsAgentClientInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['count', 'price', 'sum', 'article', 'note']
        widgets = {
            'count': forms.NumberInput(attrs={'oninput': 'controllerSum_count(this.id);'}),
            'price': forms.NumberInput(attrs={'oninput': 'controllerSum_price(this.id);'}),
        }
        error_messages = {
            'count': my_default_errors,
            'price': my_default_errors,
            'sum': my_default_errors,
            'article': my_default_errors,
            'note': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(ConsAgentClientInnerForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['article'].queryset = Articles.objects.filter(type=2)
        self.fields['article'].required = True


ConsAgentClientInnerFormset = inlineformset_factory(Operations, OperationsInner, form=ConsAgentClientInnerForm, extra=1, can_delete=True)
ConsAgentClientInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=ConsAgentClientInnerForm, extra=0, can_delete=True)

#_____________________________________________________________________________________________

class ConsVariousForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'currency', 'route', 'various', 'description', 'sum', 'type', 'type2']
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(ConsVariousForm, self).__init__(*args, **kwargs)
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['type'].initial = 2
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 7
        self.fields['various'].required = True


class ConsVariousInnerForm(forms.ModelForm):

    class Meta:
        model = OperationsInner
        fields = ['count', 'price', 'sum', 'article', 'note']
        widgets = {
            'count': forms.NumberInput(attrs={'oninput': 'controllerSum_count(this.id);'}),
            'price': forms.NumberInput(attrs={'oninput': 'controllerSum_price(this.id);'}),
        }
        error_messages = {
            'count': my_default_errors,
            'price': my_default_errors,
            'sum': my_default_errors,
            'article': my_default_errors,
            'note': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(ConsVariousInnerForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['article'].queryset = Articles.objects.filter(type=2)
        self.fields['article'].required = True


ConsVariousInnerFormset = inlineformset_factory(Operations, OperationsInner, form=ConsVariousInnerForm, extra=1, can_delete=True)
ConsVariousInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=ConsVariousInnerForm, extra=0, can_delete=True)

#_____________________________________________________________________________________________

class PaymentStatementAgentForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'currency', 'article', 'description', 'type', 'sum', 'type2']
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(PaymentStatementAgentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['type'].initial = 3
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 8
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['article'].required = True
        self.fields['article'].queryset = Articles.objects.filter(type=2)

class PaymentStatementEmployeeForm(forms.ModelForm):

    class Meta:
        model = Operations
        fields = ['cash', 'currency', 'article', 'description', 'type', 'sum', 'type2']
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(PaymentStatementEmployeeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['sum'].widget.attrs['readonly'] = True
        self.fields['type'].initial = 3
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 9
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['article'].required = True
        self.fields['article'].queryset = Articles.objects.filter(type=2)

class PSEmployeeInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['employee', 'sum']
        widgets = {
            'sum': forms.NumberInput(attrs={'oninput': 'controllerSum();'}),
        }
        error_messages = {
            'employee': my_default_errors,
            'sum': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(PSEmployeeInnerForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['employee'].required = True

PSEmployeeInnerFormset = inlineformset_factory(Operations, OperationsInner, form=PSEmployeeInnerForm, extra=1, can_delete=True)
PSEmployeeInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=PSEmployeeInnerForm, extra=0, can_delete=True)

class PSAgentInnerForm(forms.ModelForm):
    class Meta:
        model = OperationsInner
        fields = ['agent', 'sum']
        widgets = {
            'sum': forms.NumberInput(attrs={'oninput': 'controllerSum();'}),
        }
        error_messages = {
            'agent': my_default_errors,
            'sum': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *args, **kwargs):
        super(PSAgentInnerForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['agent'].required = True


PSAgentInnerFormset = inlineformset_factory(Operations, OperationsInner, form=PSAgentInnerForm, extra=1, can_delete=True)
PSAgentInnerFormset2 = inlineformset_factory(Operations, OperationsInner, form=PSAgentInnerForm, extra=0, can_delete=True)

#_____________________________________________________________________________________________

class CashMovingForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = ['cash', 'cash_sender', 'currency', 'sum', 'description', 'type', 'type2']
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(CashMovingForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = 4
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['type2'].initial = 10
        self.fields['type2'].widget = forms.HiddenInput()
        self.fields['cash_sender'].required = True
        self.fields['sum'].required = True

# -----------------------------------------------------------------------------------------------------
class WorkPayForm(forms.Form):
    route = forms.ModelMultipleChoiceField(queryset=Route.objects.all(), label='Должности')
    dateFrom = forms.DateField(label='Дата От', widget=forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')))
    dateTo = forms.DateField(label='Дата До', widget=forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')))

    inspection = forms.FloatField(initial=12.0)
    packing = forms.FloatField(initial=36.0)

    def __init__(self, *args, **kwargs):
        super(WorkPayForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# -----------------------------------------------------------------------------------------------------
class LoadingPayForm(forms.Form):
    route = forms.ModelMultipleChoiceField(queryset=Route.objects.all(), label='Должности')
    dateFrom = forms.DateField(label='Дата От', widget=forms.DateInput(attrs={'type': 'date'},
                                                                       format=('%Y-%m-%d')))
    dateTo = forms.DateField(label='Дата До', widget=forms.DateInput(attrs={'type': 'date'},
                                                                     format=('%Y-%m-%d')))

    loading = forms.FloatField(initial=15.0)

    def __init__(self, *args, **kwargs):
        super(LoadingPayForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
#-------------------------------------------------------------------------------------------------------------