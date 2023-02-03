from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.labels.models import LabelModel
from django.urls import reverse
from django.contrib.messages import get_messages
from task_manager.tasks.models import TasksModel, TaskLabelModel
from task_manager.statuses.models import StatusModel


class TestLabels(TestCase):
    def setUp(self):
        User.objects.create_user(username='user1', password='123')
        LabelModel.objects.create(name='label1')
        LabelModel.objects.create(name='label2')

    def test_labels_view(self):
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['labels']),
            LabelModel.objects.count()
        )

    def test_label_create(self):
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.post(
            reverse('create_labels'),
            {'name': "label3"}
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно создана')
        self.assertEqual(LabelModel.objects.last().name, "label3")
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(LabelModel.objects.count(), 3)

    def test_label_update(self):
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)
        label = LabelModel.objects.last()
        response = self.client.post(
            reverse('update_labels', kwargs={'pk': label.id}),
            {'name': 'label_updated'})
        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, "label_updated")
        self.assertRedirects(response, reverse('labels'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно изменена')

    def test_label_delete(self):
        label = LabelModel.objects.last()
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)
        response = self.client.get(
            reverse('delete_labels', args=(label.id,)), follow=True
        )
        response = self.client.post(
            reverse('delete_labels', kwargs={'pk': label.id})
        )
        self.assertNotContains(response, 'delete_labels', status_code=302)
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(LabelModel.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')

    def test_task_with_label_delete(self):
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)
        label1 = LabelModel.objects.get(name='label1')
        task = TasksModel.objects.create(
            name='task1',
            creator=user1,
            description='test_task_description',
            statuses=StatusModel.objects.create(name='status1'),
            work_user=user1,
        )
        TaskLabelModel.objects.create(
            task=task,
            label=label1,
        )

        response = self.client.post(
            reverse('delete_labels', kwargs={'pk': label1.id})
        )
        self.assertEqual(LabelModel.objects.count(), 2)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Невозможно удалить метку, потому что она используется')
