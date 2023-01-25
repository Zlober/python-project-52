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


class PermissionMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('Вы не авторизованы! Пожалуйста, выполните вход.'), extra_tags='danger')
            return redirect('users')
        elif request.user.id != kwargs.get('pk'):
            messages.error(request, _('У вас нет прав для изменения другого пользователя.'), extra_tags='danger')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UpdateUser(SuccessMessageMixin, PermissionMixin, UpdateView):
    model = User
    template_name = 'users/update.html'
    form_class = forms.RegUserForm
    success_message = _('Пользователь успешно изменён')
    success_url = '/users'


class DeleteUser(SuccessMessageMixin, PermissionMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_message = _('Пользователь успешно удалён')
    success_url = '/users'
