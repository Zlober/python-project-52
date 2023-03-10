from django import forms
from .models import TasksModel
from task_manager.users.models import Users
from task_manager.labels.models import LabelModel
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=Users.objects.all(),
        required=False,
        label=_('Исполнитель'),
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=LabelModel.objects.all(),
        required=False,
        label=_('Метки'),
    )

    class Meta:
        model = TasksModel
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels',
        ]
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
        }
