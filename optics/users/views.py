from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import render, redirect
from django.views import View

from optics.users.forms import LoginForm


class LoginView(View):
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboards:submissions_dashboard")
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        context = {}
        if login_form.is_valid():
            user = authenticate(**login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect("dashboards:submissions_dashboard")
            else:
                context["error_message"] = "Invalid credentials"

        return render(request, self.template_name, context)


class LogoutView(DjangoLogoutView):
    template_name = "users/login.html"
    next_page = "users:login"
