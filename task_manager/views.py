from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
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


class AuthPermissionMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('Вы не авторизованы! Пожалуйста, выполните вход.'),
                extra_tags='danger'
            )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class PermissionMixin(View):
    msg = _('У вас нет прав для изменения другого пользователя.')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != kwargs.get('pk'):
            messages.error(request, self.msg, extra_tags='danger')
            return redirect(self.url_redirect)
        return super().dispatch(request, *args, **kwargs)
