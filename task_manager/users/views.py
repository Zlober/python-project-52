from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.models import User
from task_manager.users import forms
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.views import AuthPermissionMixin, PermissionMixin
from django.db.models import ProtectedError


class UserMixin(SuccessMessageMixin, AuthPermissionMixin, PermissionMixin):
    model = User
    form_class = forms.RegUserForm
    success_url = '/users'
    url_redirect = 'users'


class Index(ListView):
    context_object_name = 'users'
    template_name = 'users/index.html'
    model = User


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/reg.html'
    form_class = forms.RegUserForm
    success_message = _('Пользователь успешно зарегистрирован')

    def get_success_url(self):
        return reverse_lazy('login')


class UpdateUser(UserMixin, UpdateView):
    template_name = 'users/update.html'
    success_message = _('Пользователь успешно изменён')


class DeleteUser(UserMixin, DeleteView):
    template_name = 'users/delete.html'

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('Пользователь успешно удалён'))
            return redirect(reverse_lazy('users'))
        except ProtectedError:
            messages.error(self.request, _('Невозможно удалить пользователя, потому что он используется'), extra_tags='danger')
            return redirect(reverse_lazy('users'))

