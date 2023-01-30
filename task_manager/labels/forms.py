from django import forms
from .models import LabelModel
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):
    class Meta:
        model = LabelModel
        fields = (
            'name',
        )
        labels = {
            'name': _('Имя')
        }
