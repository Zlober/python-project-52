from django.contrib.auth.models import User


class Users(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
