from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm


class LoginView(View):
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("submissions:upload-optical-pia-submission")
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        context = {}
        if login_form.is_valid():
            user = authenticate(**login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect("submissions:upload-optical-pia-submission")
            else:
                context["error_message"] = "Invalid credentials"

        return render(request, self.template_name, context)
