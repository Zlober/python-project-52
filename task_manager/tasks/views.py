from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import TasksModel
from .forms import TaskForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class TasksMixin(SuccessMessageMixin):
    model = TasksModel
    form_class = TaskForm
    success_url = reverse_lazy('tasks')


class Index(TasksMixin, ListView):
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


class DeleteTask(TasksMixin, DeleteView):
    template_name = 'tasks/delete.html'
    success_message = 'Задача успешно удалена'


class ViewTask(TasksMixin, DetailView):
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
