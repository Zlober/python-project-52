from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import Users


class RegUserForm(UserCreationForm):

    class Meta:
        model = Users
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
