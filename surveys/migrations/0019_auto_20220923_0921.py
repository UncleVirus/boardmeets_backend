# Generated by Django 3.2.9 on 2022-09-23 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0018_auto_20220922_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='doc_ref',
            field=models.CharField(blank=True, default='UB96LJWNJ0', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='surveyquestions',
            name='doc_ref',
            field=models.CharField(blank=True, default='4M2Z90ZOWC', max_length=200, null=True),
        ),
    ]
