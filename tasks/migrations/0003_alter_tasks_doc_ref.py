# Generated by Django 3.2.9 on 2022-05-20 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_tasks_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='doc_ref',
            field=models.CharField(blank=True, default='1YIYMF82BN', max_length=200, null=True),
        ),
    ]