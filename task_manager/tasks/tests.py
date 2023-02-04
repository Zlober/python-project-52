from django.test import TestCase
from task_manager.statuses.models import StatusModel
from django.urls import reverse
from task_manager.users.models import Users
from django.contrib.messages import get_messages
from task_manager.tasks.models import TasksModel


class TestTasks(TestCase):

    def setUp(self):
        Users1 = Users.objects.create_user(
            username='Users1',
            password='123',
            first_name='Users1_first_name',
            last_name='Users1_last_name',
        )
        Users.objects.create_user(
            username='Users2',
            password='123',
            first_name='Users2_first_name',
            last_name='Users2_last_name',
        )
        status1 = StatusModel.objects.create(name='status1')
        TasksModel.objects.create(
            name='task1',
            description='task1 description',
            creator=Users1.username,
            status=status1,
            executor=Users1

        )

    def test_task_view(self):
        Users1 = Users.objects.get(username='Users1')
        self.client.force_login(Users1)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertEqual(
            len(response.context['tasks']),
            TasksModel.objects.count()
        )

    def test_task_view_no_auth(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        self.assertRedirects(response, reverse('login'))

    def test_task_create(self):
        User1 = Users.objects.get(username='Users1')
        self.client.force_login(User1)
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

    def test_task_create_post(self):
        User1 = Users.objects.get(username='Users1')
        status1 = StatusModel.objects.get(name='status1')
        self.client.force_login(User1)
        response = self.client.post(
            reverse('create_task'),
            {
                'name': 'task_test',
                'description': 'task description',
                'status': status1.id,
                'executor': User1.id,

            }
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')
        self.assertEqual(TasksModel.objects.count(), 2)
        task_last = TasksModel.objects.last()
        self.assertEqual(task_last.name, 'task_test')

    def test_tasks_update_view(self):
        User1 = Users.objects.get(username='Users1')
        self.client.force_login(User1)
        task = TasksModel.objects.first()

        response = self.client.get(
            reverse('update_task', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/update.html')

        response = self.client.post(
            reverse('update_task', kwargs={'pk': task.id}),
            {
                'name': 'update_task',
                'description': 'task_description_updated',
                'status': task.status.id,
                'executor': task.executor.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, "update_task")
        self.assertEqual(task.description, "task_description_updated")
        self.assertRedirects(response, reverse('tasks'))

    def test_task_delete_view(self):
        User1 = Users.objects.get(username='Users1')
        task = TasksModel.objects.last()
        self.client.force_login(User1)
        response = self.client.get(
            reverse('delete_task', args=(task.id,)),
            follow=True
        )
        response = self.client.post(
            reverse('delete_task', kwargs={'pk': task.id})
        )
        self.assertNotContains(response, 'delete_task', status_code=302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(TasksModel.objects.count(), 0)

    def test_task_invalid_delete(self):
        User1 = Users.objects.get(username='Users2')
        task = TasksModel.objects.last()
        self.client.force_login(User1)
        request = self.client.post(
            reverse('delete_task', kwargs={'pk': task.id})
        )
        self.assertRedirects(request, reverse('tasks'))
        self.assertEqual(TasksModel.objects.count(), 1)

    def test_task_statuses_filter(self):
        self.assertEqual(
            TasksModel.objects.filter(status__name="status1").count(),
            1
        )

    def test_task_executor_filter(self):
        self.assertEqual(
            TasksModel.objects.filter(executor__username='Users1').count(),
            1
        )

    def test_own_task_filter(self):
        User1 = Users.objects.get(username='Users1')
        self.assertEqual(
            TasksModel.objects.filter(creator=User1.username).count(),
            1
        )
        self.assertEqual(TasksModel.objects.count(), 1)
