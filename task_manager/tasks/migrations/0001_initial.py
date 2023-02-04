# Generated by Django 4.1.6 on 2023-02-04 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labels', '0001_initial'),
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLabelModel',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')
                 ),
                ('label', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to='labels.labelmodel')
                 ),
            ],
        ),
        migrations.CreateModel(
            name='TasksModel',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')
                 ),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('creator', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('executor', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    to=settings.AUTH_USER_MODEL)
                 ),
                ('labels', models.ManyToManyField(
                    through='tasks.TaskLabelModel',
                    to='labels.labelmodel')
                 ),
                ('status', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to='statuses.statusmodel')
                 ),
            ],
        ),
        migrations.AddField(
            model_name='tasklabelmodel',
            name='task',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='tasks.tasksmodel'
            ),
        ),
    ]
