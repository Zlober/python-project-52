from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import StatusForm
from .models import StatusModel
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from task_manager.views import AuthPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class StatusesMixin(SuccessMessageMixin, AuthPermissionMixin):
    model = StatusModel
    form_class = StatusForm
    success_url = '/statuses/'


class Index(StatusesMixin, ListView):
    model = StatusModel
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreateStatus(StatusesMixin, CreateView):
    template_name = 'statuses/create.html'
    success_message = _('Статус успешно создан')


class UpdateStatus(StatusesMixin, UpdateView):
    template_name = 'statuses/update.html'
    success_message = _('Статус успешно изменён')


class DeleteStatus(StatusesMixin, DeleteView):
    template_name = 'statuses/delete.html'
    success_message = _('Статус успешно удалён')
