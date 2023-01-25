from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class Login(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = _('Вы залогинены')
    success_url = '/'

    def get_success_url(self):
        return reverse_lazy('index')


class Logout(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('Вы разлогинены'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('index')

