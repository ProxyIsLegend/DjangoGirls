from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView


def home_page(request):
    context = {}

    return render(request, "index.html", context)


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse("profile"))
            else:
                context['error'] = "Логин или пароль неправильные"

        return render(request, self.template_name, context)


class ProfilePage(TemplateView):
    template_name = "registration/profile.html"


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}

        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_again = request.POST.get('password_again')

            if len(username) != 0 and len(email) != 0 and len(password):
                if password == password_again:
                    User.objects.create_user(username, email, password)
                    return redirect(reverse("login"))
                else:
                    context['error'] = "Пароли должны совпадать"
            else:
                context['error'] = "Все поля должны быть заполнены"

        return render(request, self.template_name, context)


