from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from task_manager.users import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class Index(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/index.html', {'users': users})


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/reg.html'
    form_class = forms.RegUserForm
    success_message = _('Пользователь успешно зарегистрирован')

    def get_success_url(self):
        return reverse('login')


class PermissionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, level=messages.ERROR, extra_tags='danger',
                                 message=self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(self, *args, **kwargs)


class UpdateUser(PermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/update.html'
    form_class = forms.RegUserForm
    success_message = _('Пользователь успешно изменён')
    success_url = '/users'
    permission_denied_message = _('Вы не авторизованы! Пожалуйста, выполните вход.')
    if UpdateView.pk_url_kwarg == UpdateView.


class DeleteUser(PermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_message = _('Пользователь успешно удалён')
    success_url = '/users'
    permission_denied_message = _('Вы не авторизованы! Пожалуйста, выполните вход.')
