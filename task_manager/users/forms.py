from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )
        help_texts = {
            'username': _('Обязательное поле. Не более 150 символов. '
                          'Только буквы, цифры и символы @/./+/-/_.'),
        }
