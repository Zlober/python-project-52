from django.test import TestCase
from task_manager.statuses.models import StatusModel
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from task_manager.tasks.models import TasksModel


class TestStatuses(TestCase):

    def setUp(self):
        StatusModel.objects.create(name='status1')
        StatusModel.objects.create(name='status2')
        User.objects.create_user(
            username='user1',
            password='123',
            first_name='user1_first_name',
            last_name='user1_last_name',
        )
        User.objects.create_user(
            username='user2',
            password='123',
            first_name='user1_first_name',
            last_name='user1_last_name',
        )

    def test_statuses_page_view_no_auth(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.',
        )
        self.assertRedirects(response, reverse('login'))

    def test_statuses_page_view(self):
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertEqual(
            len(response.context['statuses']),
            StatusModel.objects.count()
        )

    def test_statuses_page_create(self):
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        response = self.client.post(
            reverse('create_status'),
            {
                'name': 'teststatus'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно создан')
        self.assertEqual(StatusModel.objects.count(), 3)
        status_last = StatusModel.objects.last()
        self.assertEqual(status_last.name, 'teststatus')

    def test_statuses_page_update(self):
        user1 = User.objects.get(username='user1')
        status1 = StatusModel.objects.get(name='status1')
        self.client.force_login(user1)
        response = self.client.get(
            reverse('update_status', kwargs={'pk': status1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        response = self.client.post(
            reverse('update_status', kwargs={'pk': status1.id}),
            {
                'name': 'new_status'
            }
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно изменён')
        self.assertRedirects(response, reverse('statuses'))

    def test_statuses_page_delete(self):
        user1 = User.objects.get(username='user1')
        status1 = StatusModel.objects.get(name='status1')
        self.client.force_login(user1)
        response = self.client.get(
            reverse('delete_status', kwargs={'pk': status1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')
        response = self.client.post(
            reverse('delete_status', kwargs={'pk': status1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удалён')

    def test_statuses_page_delete_used(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        status1 = StatusModel.objects.get(name='status1')
        TasksModel.objects.create(
            name='test_task',
            description='test_description',
            creator=user1,
            statuses=status1,
            executor=user1
        )
        self.client.force_login(user2)
        response = self.client.post(
            reverse('delete_status', kwargs={'pk': status1.id})
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить статус, потому что он используется',
        )
