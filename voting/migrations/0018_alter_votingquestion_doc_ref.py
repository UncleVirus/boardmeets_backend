# Generated by Django 3.2.9 on 2022-09-22 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0017_alter_votingquestion_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votingquestion',
            name='doc_ref',
            field=models.CharField(blank=True, default='6EFZSDYVRK', max_length=200, null=True),
        ),
    ]
