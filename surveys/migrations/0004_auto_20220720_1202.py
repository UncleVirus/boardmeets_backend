# Generated by Django 3.2.9 on 2022-07-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_auto_20220520_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='doc_ref',
            field=models.CharField(blank=True, default='F0404M1VQI', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='surveyquestions',
            name='doc_ref',
            field=models.CharField(blank=True, default='CWILSOJVVY', max_length=200, null=True),
        ),
    ]