from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from route.views import get_base_template_name
from user.forms import CustomUserRegisterForm, CustomUserChangeForm, PassWordCangeForm
from .forms import *
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import render, redirect

class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'systems/pages/users.html'
    def get(self, request, *args, **kwargs):
        f = UserFilter(request.GET, queryset=User.objects.all())
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'form': f.form,
                                                    'page_obj': page_obj})

class UserAddView(LoginRequiredMixin, TemplateView):
    user_add_form = CustomUserRegisterForm
    template_name = 'systems/forms/user_add.html'

    def get(self, request, *args, **kwargs):
        form = self.user_add_form()
        context = {'form': form, }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.user_add_form(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(self.request, "Запись успешно добавлена")
            return redirect('systems:users')
        context = {'form': form}
        return render(request, self.template_name, context)

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'systems/forms/user_profile.html'

    def get_success_url(self):
        messages.success(self.request, "Ваш профиль был успешно обновлен")
        return reverse_lazy('main:home_page')

    def get_context_data(self, **kwargs):
        data = super(UserProfileView, self).get_context_data(**kwargs)
        data['base_template_name'] = get_base_template_name(self.request.user)
        return data

class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserRegisterForm
    template_name = 'systems/forms/user_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Запись под номером " + str(self.object.pk) + " была успешно отредактирована")
        return reverse_lazy('systems:users')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PassWordCangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = PassWordCangeForm(request.user)

    return render(request, 'systems/forms/change_password.html',
                  {'form': form,
                   'base_template_name': get_base_template_name(request.user)})

@login_required
def delete_user(request, pk):
    get_object_or_404(User, id=pk).delete()
    messages.success(request, 'Запись под номером ' + str(pk) + ' была успешно удалена')
    return redirect('systems:users')