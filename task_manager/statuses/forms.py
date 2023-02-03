from task_manager.statuses.models import StatusModel
from django.forms import ModelForm


class StatusForm(ModelForm):
    class Meta:
        model = StatusModel
        fields = (
            'name',
        )
