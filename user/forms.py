from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _

class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'cash_box', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Имя:"
        self.fields['last_name'].label = "Фамилия:"
        self.fields['phone'].label = "Телефон:"
        self.fields['email'].label = "Email:"
        self.fields['cash_box'].label = "Касса:"
        self.fields['role'].label = "Роль пользователя:"
        self.fields['password1'].label = "Пароль:"
        self.fields['password2'].label = "Подтверждение пароля:"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone',)

class PassWordCangeForm(PasswordChangeForm):
    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
        'password_mismatch': _('The two password fields didn’t match.'),

    }
