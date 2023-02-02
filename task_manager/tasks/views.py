from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .models import TasksModel
from .forms import TaskForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django_filters.views import FilterView
from task_manager.tasks.filter import FilterForm
from task_manager.views import AuthPermissionMixin


class TasksMixin(SuccessMessageMixin, AuthPermissionMixin):
    model = TasksModel
    form_class = TaskForm
    success_url = reverse_lazy('tasks')


class Index(TasksMixin, FilterView):
    model = TasksModel
    filterset_class = FilterForm
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class CreateTask(TasksMixin, CreateView):
    template_name = 'tasks/create.html'
    success_message = _('Задача успешно создана')
    
    def form_valid(self, form):
        form.instance.creator = User.objects.get(id=self.request.user.pk)
        return super().form_valid(form)


class UpdateTask(TasksMixin, UpdateView):
    template_name = 'tasks/update.html'
    success_message = 'Задача успешно изменена'


class DeleteTask(SuccessMessageMixin, AuthPermissionMixin, DeleteView):
    model = TasksModel
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/delete.html'
    success_message = 'Задача успешно удалена'

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != self.get_object().creator:
            messages.error(request, _('Задачу может удалить только её автор'), extra_tags='danger')
            return redirect(reverse_lazy('tasks'))
        return super().dispatch(request, *args, **kwargs)


class ViewTask(TasksMixin, DetailView):
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
