from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import StatusForm
from .models import StatusModel
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from task_manager.views import AuthPermissionMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import ProtectedError


class StatusesMixin(SuccessMessageMixin, AuthPermissionMixin):
    model = StatusModel
    form_class = StatusForm
    success_url = '/statuses/'


class Index(StatusesMixin, ListView):
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreateStatus(StatusesMixin, CreateView):
    template_name = 'statuses/create.html'
    success_message = _('Статус успешно создан')


class UpdateStatus(StatusesMixin, UpdateView):
    template_name = 'statuses/update.html'
    success_message = _('Статус успешно изменён')


class DeleteStatus(DeleteView):
    model = StatusModel
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('Статус успешно удалён'))
            return redirect(reverse_lazy('statuses'))
        except ProtectedError:
            messages.error(self.request, _('Невозможно удалить статус, потому что он используется'), extra_tags='danger')
            return redirect(reverse_lazy('statuses'))
