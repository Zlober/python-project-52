from django import forms
from .models import TasksModel
from task_manager.statuses.models import StatusModel
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    work_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = TasksModel
        fields = [
            'name',
            'description',
            'statuses',
            'work_user',
        ]
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'statuses': _('Статус'),
            'work_user': _('Исполнитель'),
        }
