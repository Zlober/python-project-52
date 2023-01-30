from task_manager.statuses.models import StatusModel
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class StatusForm(ModelForm):
    class Meta:
        model = StatusModel
        fields = (
            'name',
        )
