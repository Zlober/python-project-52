from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import StatusModel
from task_manager.labels.models import LabelModel


class TasksModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    creator = models.CharField(max_length=255)
    executor = models.ForeignKey(Users, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(StatusModel, on_delete=models.PROTECT)
    labels = models.ManyToManyField(LabelModel, through='TaskLabelModel')

    def __str__(self):
        return self.name


class TaskLabelModel(models.Model):
    label = models.ForeignKey(LabelModel, on_delete=models.PROTECT)
    task = models.ForeignKey(TasksModel, on_delete=models.CASCADE)
