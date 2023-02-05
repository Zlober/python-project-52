import django_filters
from task_manager.statuses.models import StatusModel
from task_manager.labels.models import LabelModel
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import Users
from django import forms


class FilterForm(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label=_('Статус'),
        queryset=StatusModel.objects.all(),
    )
    executor = django_filters.ModelChoiceFilter(
        label=_('Исполнитель'),
        queryset=Users.objects.all(),
    )
    labels = django_filters.ModelChoiceFilter(
        label=_('Метка'),
        queryset=LabelModel.objects.all(),
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        widget=forms.CheckboxInput,
        method='check_self_tasks',
    )

    def check_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset
