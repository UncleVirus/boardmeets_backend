# Generated by Django 3.2.9 on 2022-04-05 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meeting_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(blank=True, max_length=100, null=True)),
                ('task_name', models.CharField(max_length=250)),
                ('task_description', models.CharField(max_length=250)),
                ('completion_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('task_status', models.CharField(blank=True, max_length=250, null=True)),
                ('task_priority', models.CharField(blank=True, max_length=250, null=True)),
                ('task_document', models.CharField(blank=True, max_length=200000, null=True)),
                ('doc_ref', models.CharField(blank=True, default='KNN85HE8VS', max_length=200, null=True)),
                ('sendEmail', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meeting_management.meeting')),
                ('task_assignee', models.ManyToManyField(blank=True, related_name='task_assignees', to=settings.AUTH_USER_MODEL)),
                ('task_viewers', models.ManyToManyField(blank=True, related_name='task_viewers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('commentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.tasks')),
            ],
        ),
    ]
