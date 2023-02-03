from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import LabelModel
from .forms import LabelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.db.models import ProtectedError
from task_manager.views import AuthPermissionMixin


class LabelMixin(SuccessMessageMixin, AuthPermissionMixin):
    model = LabelModel
    form_class = LabelForm
    success_url = reverse_lazy('labels')


class Index(LabelMixin, ListView):
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class CreateLabel(LabelMixin, CreateView):
    template_name = 'labels/create.html'
    success_message = _('Метка успешно создана')


class UpdateLabel(LabelMixin, UpdateView):
    template_name = 'labels/update.html'
    success_message = _('Метка успешно изменена')


class DeleteLabel(DeleteView):
    model = LabelModel
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(self.request, *args, **kwargs)
            messages.success(request, _('Метка успешно удалена'))
            return redirect(reverse_lazy('labels'))
        except ProtectedError:
            messages.error(
                self.request,
                _('Невозможно удалить метку, потому что она используется'),
                extra_tags='danger',
            )
            return redirect(reverse_lazy('labels'))
