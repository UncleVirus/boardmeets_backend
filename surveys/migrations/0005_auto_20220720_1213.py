# Generated by Django 3.2.9 on 2022-07-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_auto_20220720_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='doc_ref',
            field=models.CharField(blank=True, default='3B4M7LJHFU', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='surveyquestions',
            name='doc_ref',
            field=models.CharField(blank=True, default='DNTF3XSN8K', max_length=200, null=True),
        ),
    ]
