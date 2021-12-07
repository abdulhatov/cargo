from django.forms import ModelForm, DateInput
from .models import *
from django import forms
from djangoformsetjs.utils import formset_media_js
from route.models import Direction
from django.forms import formset_factory, inlineformset_factory

my_default_errors = {
    'required': 'Поле обязательно для заполнения',
    'invalid': 'Введите допустимое значение',
}

class AddListForm(ModelForm):
    required_css_class = 'required2'
    class Meta:
        model = AddList
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddListForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['id'] = 'summernote'

class CategoryNameForm(ModelForm):
    required_css_class = 'required2'

    class Meta:
        model = CategoryName
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryNameForm, self).__init__(*args, **kwargs)
        self.fields['unit'].widget.attrs['class'] = 'select2'

class ListNameForm(ModelForm):
    required_css_class = 'required2'

    class Meta:
        model = ListName
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ListNameForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'select2'

# --------------------------------------------------------------------

class WHIncomeForm(forms.ModelForm):
    class Meta:
        model = WarehouseOperation
        fields = ['date', 'warehouse', 'wh_article', 'sum', 'type']
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}

    def __init__(self, *args, **kwargs):
        super(WHIncomeForm, self).__init__(*args, **kwargs)
        self.fields['wh_article'].queryset = Articles.objects.filter(type=1)
        self.fields['type'].initial = 1
        self.fields['type'].widget = forms.HiddenInput()

        self.fields['wh_article'].required = True
        self.fields['sum'].widget.attrs['readonly'] = True

class WHIncomeInnerForm(forms.ModelForm):
    class Meta:
        model = WarehouseOperationInner
        fields = '__all__'
        widgets = {'category': forms.Select(attrs={'onchange': 'SetListName(this.id);'}),
                   'sum': forms.NumberInput(attrs={'oninput': 'controllerSumWarehouse();'})}

        error_messages = {
            'category': my_default_errors,
            'name': my_default_errors,
            'sum': my_default_errors,
            'price': my_default_errors}

    def __init__(self, *arg, **kwarg):
        super(WHIncomeInnerForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False
        self.fields['price'].required = True

    class Media(object):
        js = formset_media_js

WHIncomeInnerFormSet = inlineformset_factory(WarehouseOperation, WarehouseOperationInner,
                                             form=WHIncomeInnerForm, extra=1, can_delete=True)
WHIncomeInnerFormSet2 = inlineformset_factory(WarehouseOperation, WarehouseOperationInner,
                                              form=WHIncomeInnerForm, extra=0, can_delete=True)


# --------------------------------------------------------------------
class WHConsumptionForm(ModelForm):
    class Meta:
        model = WarehouseOperation
        exclude = ('from_warehouse', 'added_by')
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}

    def __init__(self, *args, **kwargs):
        super(WHConsumptionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['wh_article'].queryset = Articles.objects.filter(type=2)
        self.fields['type'].initial = 2
        self.fields['type'].widget = forms.HiddenInput()

        self.fields['wh_article'].required = True
        self.fields['route'].required = True
        self.fields['sum'].widget.attrs['readonly'] = True

class WHConsumptionInnerForm(forms.ModelForm):
    class Meta:
        model = WarehouseOperationInner
        fields = '__all__'
        widgets = {'category': forms.Select(attrs={'onchange': 'SetListName(this.id);'}),
                   'sum': forms.NumberInput(attrs={'oninput': 'controllerSumWarehouse();'})}
        error_messages = {
            'category': my_default_errors,
            'name': my_default_errors,
            'sum': my_default_errors,
            'price': my_default_errors
        }
    def __init__(self, *arg, **kwarg):
        super(WHConsumptionInnerForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False
        self.fields['price'].required = True

    class Media(object):
        js = formset_media_js

WHConsumptionFormSet = inlineformset_factory(WarehouseOperation, WarehouseOperationInner,
                                             form=WHConsumptionInnerForm, extra=1, can_delete=True)
WHConsumptionFormSet2 = inlineformset_factory(WarehouseOperation, WarehouseOperationInner,
                                              form=WHConsumptionInnerForm, extra=0, can_delete=True)

# --------------------------------------------------------------------

class WHMovingForm(ModelForm):
    class Meta:
        model = WarehouseOperation
        fields = ['date', 'warehouse', 'from_warehouse', 'sum', 'type']
        widgets = {'date': DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}

    def __init__(self, *args, **kwargs):
        super(WHMovingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['type'].initial = 3
        self.fields['type'].widget = forms.HiddenInput()

        self.fields['sum'].widget.attrs['readonly'] = True

class WHMovingInnerForm(forms.ModelForm):
    class Meta:
        model = WarehouseOperationInner
        exclude = ('price', )
        widgets = {'category': forms.Select(attrs={'onchange': 'SetListName(this.id);'}),
                   'sum': forms.NumberInput(attrs={'oninput': 'controllerSumWarehouse();'})}
        error_messages = {
            'category': my_default_errors,
            'name': my_default_errors,
            'sum': my_default_errors
        }

    class Media(object):
        js = formset_media_js

    def __init__(self, *arg, **kwarg):
        super(WHMovingInnerForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False



WHMovingFormSet = inlineformset_factory(WarehouseOperation, WarehouseOperationInner, form=WHMovingInnerForm, extra=1, can_delete=True)
WHMovingFormSet2 = inlineformset_factory(WarehouseOperation, WarehouseOperationInner, form=WHMovingInnerForm, extra=0, can_delete=True)

# --------------------------------------------------------------------

Operation_CHOICES = (
    ("1", "Приходник"),
    ("2", "Расходник"),
    ("3", "Перемещение"))

class WHReportForm(forms.Form):
    warehouse = forms.ModelChoiceField(queryset=AddList.objects.all(), label='Склад')
    naming = forms.ModelChoiceField(queryset=ListName.objects.all(), label='Наименование')
    operation = forms.ChoiceField(choices=Operation_CHOICES, label="Операция")
    dateFrom = forms.DateField(label="Дата ОТ", widget=DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')))
    dateTo = forms.DateField(label="Дата ДО", widget=DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')))


class BagReportForm(forms.Form):
    warehouse = forms.ModelChoiceField(queryset=AddList.objects.all())
    operation = forms.ChoiceField(choices=Operation_CHOICES)
    direction = forms.ModelChoiceField(queryset=Direction.objects.all(), required=False)
    dateFrom = forms.DateField(widget=DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')))
    dateTo = forms.DateField(widget=DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')))
    routeFrom = forms.ChoiceField(choices='', required=False)
    routeTo = forms.ChoiceField(choices='', required=False)

class OstatokForm(forms.Form):
    warehouse = forms.ModelChoiceField(queryset=AddList.objects.all())
