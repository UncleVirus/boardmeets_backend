# Generated by Django 3.2.9 on 2023-01-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0019_alter_votingquestion_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votingquestion',
            name='doc_ref',
            field=models.CharField(blank=True, default='5D1XEE3WFS', max_length=200, null=True),
        ),
    ]
