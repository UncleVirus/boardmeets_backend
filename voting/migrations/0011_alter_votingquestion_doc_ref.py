# Generated by Django 3.2.9 on 2022-09-22 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0010_alter_votingquestion_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votingquestion',
            name='doc_ref',
            field=models.CharField(blank=True, default='70CG598K7I', max_length=200, null=True),
        ),
    ]
