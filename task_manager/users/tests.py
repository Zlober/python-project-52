from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from task_manager.tasks.models import TasksModel
from task_manager.users.models import Users
from task_manager.statuses.models import StatusModel


class TestUser(TestCase):

    def setUp(self):
        Users.objects.create_user(
            username='user1',
            first_name='user1_first_name',
            last_name='user1_last_name',
            password='123',
        )
        Users.objects.create_user(
            username='user2',
            password='321',
            first_name='user2_first_name',
            last_name='user2_last_name',
        )

    def test_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertEqual(len(response.context['users']), Users.objects.count())

    def test_reg_user_page(self):
        response = self.client.get(reverse('reg_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/reg.html')

    def test_reg_user_post(self):
        response = self.client.post(
            reverse('reg_user'),
            {
                'username': 'user3',
                'first_name': 'user3_first_name',
                'last_name': 'user3_last_name',
                'password1': 'user3@123',
                'password2': 'user3@123',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Пользователь успешно зарегистрирован'
        )
        user = Users.objects.last()
        self.assertEqual(user.username, 'user3')
        self.assertEqual(user.first_name, 'user3_first_name')
        self.assertEqual(user.last_name, 'user3_last_name')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_page_post(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'user1',
                'password': '123',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы залогинены')

    def test_user_no_auth_update_page(self):
        user1 = Users.objects.get(username='user1')
        response = self.client.get(
            reverse('update_user', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_user_no_permission_update_page(self):
        user1 = Users.objects.get(username='user1')
        user2 = Users.objects.get(username='user2')
        self.client.force_login(user1)
        response = self.client.get(
            reverse('update_user', kwargs={'pk': user2.id})
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'У вас нет прав для изменения другого пользователя.',
        )

    def test_user_success_update_page(self):
        user1 = Users.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.get(
            reverse('update_user', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_user_success_delete_page(self):
        user1 = Users.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.get(
            reverse('delete_user', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_user_success_delete_page_post(self):
        user1 = Users.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.post(
            reverse('delete_user', kwargs={'pk': user1.id}),
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удалён')

    def test_user_no_auth_delete_page(self):
        user1 = Users.objects.get(username='user1')
        response = self.client.post(
            reverse('delete_user', kwargs={'pk': user1.id}),
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.',
        )

    def test_user_no_permission_delete_page(self):
        user1 = Users.objects.get(username='user1')
        user2 = Users.objects.get(username='user2')
        self.client.force_login(user1)
        response = self.client.post(
            reverse('delete_user', kwargs={'pk': user2.id}),
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'У вас нет прав для изменения другого пользователя.',
        )

    def test_user_applied_task(self):
        user1 = Users.objects.get(username='user1')
        status1 = StatusModel.objects.create(name='status1')
        TasksModel.objects.create(
            name='test_task',
            description='test_description',
            creator=user1,
            status=status1,
            executor=user1
        )
        self.client.force_login(user1)
        response = self.client.post(
            reverse('delete_user', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить пользователя, потому что он используется',
        )
