# Generated by Django 3.2.9 on 2022-09-12 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_tasks_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='doc_ref',
            field=models.CharField(blank=True, default='BA7AEF4LLZ', max_length=200, null=True),
        ),
    ]
