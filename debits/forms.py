from django import forms
from .models import *
from django.forms import formset_factory, inlineformset_factory
from djangoformsetjs.utils import formset_media_js
from django.forms import ModelChoiceField
from route.models import Direction, Route

my_default_errors = {
    'required': 'Поле обязательно для заполнения',
    'invalid': 'Введите допустимое значение',
}

class ClientContrAgentsForm(forms.ModelForm):
    class Meta:
        model = ClientContrAgents
        exclude = ('added_by',)
        widgets = {'more_info': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(ClientContrAgentsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class IncomeDebitsForm(forms.ModelForm):
    class Meta:
        model = IncomeDebits
        exclude = ('added_by',)
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})
                   }

    def __init__(self, *args, **kwargs):
        super(IncomeDebitsForm, self).__init__(*args, **kwargs)
        self.fields['wh_article'].queryset = Articles.objects.filter(type=1)
        self.fields['sum'].widget.attrs['readonly'] = True


class IncomeDebitsInnerForm(forms.ModelForm):
    class Meta:
        model = IncomeDebitsInner
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={"onchange": "SetRoute(this.id)", "data-toggle": "tooltip", "data-placement": "top",
                                          "title": ""}),
            'sum': forms.NumberInput(attrs={'oninput': 'controllerDebitsSum();'}),
        }
        error_messages = {
            'check': my_default_errors,
            'client': my_default_errors,
            'route': my_default_errors,
            'sum': my_default_errors
        }

    def __init__(self, *arg, **kwarg):
        super(IncomeDebitsInnerForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False

    class Media(object):
        js = formset_media_js + (
            # Здесь другие носители формы
        )
IncomeDebitsInnerFormset = inlineformset_factory(IncomeDebits, IncomeDebitsInner, form=IncomeDebitsInnerForm, extra=1, can_delete=True)
IncomeDebitsInnerFormset2 = inlineformset_factory(IncomeDebits, IncomeDebitsInner, form=IncomeDebitsInnerForm, extra=0, can_delete=True)


class IncomeDEForm(forms.ModelForm):
    class Meta:
        model = IncomeDebits
        exclude = ('added_by',)
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d')),
                   'description': forms.Textarea(attrs={'id': 'summernote'})}

    def __init__(self, *args, **kwargs):
        super(IncomeDEForm, self).__init__(*args, **kwargs)
        self.fields['wh_article'].queryset = Articles.objects.filter(type=1)
        #self.fields['agent'].widget.attrs['readonly'] = True
        self.fields['agent'].disabled = True
        self.fields['sum'].widget.attrs['readonly'] = True

class IDIEForm(forms.ModelForm):
    class Meta:
        model = IncomeDebitsInner
        fields = '__all__'
        widgets = {
            'client': forms.Select(
                attrs={"onchange": "SetRoute(this.id)", "data-toggle": "tooltip", "data-placement": "top",
                       "title": ""}),
            'sum': forms.NumberInput(attrs={'oninput': 'controllerDebitsSum();'}),
        }

    def __init__(self, *args, **kwargs):
        super(IDIEForm, self).__init__(*args, **kwargs)
        #self.fields['client'].widget.attrs['readonly'] = True
        #self.fields['client'].disabled = True

    class Media(object):
        js = formset_media_js + (
            # Здесь другие носители формы
        )
IDIEditFormSet = inlineformset_factory(IncomeDebits, IncomeDebitsInner, form=IDIEForm, extra=1, can_delete=True)
IDIEditFormSet2 = inlineformset_factory(IncomeDebits, IncomeDebitsInner, form=IDIEForm, extra=0, can_delete=True)

# -------------------------------------------- SEARCH --------------------------------------------------

class RouteModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return str(obj.idRoute) + "(" + str(obj.date.strftime('%Y')) + ")"

class ClientReportForm(forms.Form):
    direction = forms.ModelChoiceField(queryset=Direction.objects.all(),
                                       widget=forms.Select(attrs={'onchange': 'SetRoute(this.id);'}))
    routeFrom = RouteModelChoiceField(queryset=Route.objects.all())
    routeTo = RouteModelChoiceField(queryset=Route.objects.all())
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    def __init__(self, *args, **kwargs):
        super(ClientReportForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control select2'

# def getChoices():
#     routes = Route.objects.all()
#     choices = []
#     choices.append((-1, '---------'))
#     for route in routes:
#         choices.append((route.pk, route.__str__()))
#     return choices

class ReportForm(forms.Form):
    direction = forms.ModelChoiceField(queryset=Direction.objects.all(),
                                       widget=forms.Select(attrs={'onchange': 'SetRoute2(this.id);'}))
    route = forms.MultipleChoiceField(choices=[], required=False)
    agent = forms.ModelChoiceField(queryset=ClientContrAgents.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'