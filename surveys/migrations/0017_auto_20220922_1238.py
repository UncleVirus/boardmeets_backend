# Generated by Django 3.2.9 on 2022-09-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0016_auto_20220922_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='doc_ref',
            field=models.CharField(blank=True, default='63YTT9ZOOL', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='surveyquestions',
            name='doc_ref',
            field=models.CharField(blank=True, default='LWDRESLUY8', max_length=200, null=True),
        ),
    ]
