# Generated by Django 3.2.9 on 2022-09-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0007_auto_20220922_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='doc_ref',
            field=models.CharField(blank=True, default='UZG6R36ROT', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='surveyquestions',
            name='doc_ref',
            field=models.CharField(blank=True, default='KUPTR3AFZR', max_length=200, null=True),
        ),
    ]
