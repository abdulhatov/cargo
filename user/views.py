from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user.forms import CustomUserRegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("User successfully saved!!!")
        return redirect("/main")
    else:
	    form = CustomUserRegisterForm()

    return render(request, "register.html", {"form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли в систему как {username}.")
                return redirect("/main")

            else:
                return redirect('systems:users')
        else:
            #messages.error(request, "Invalid username or password.")
            return render(request=request, template_name="login.html", context={"form": form})
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})


def logout(request):
    auth.logout(request)
    return redirect('login')
