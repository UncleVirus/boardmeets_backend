# Generated by Django 3.2.9 on 2022-07-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_alter_votingquestion_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votingquestion',
            name='doc_ref',
            field=models.CharField(blank=True, default='WP49XK8XAJ', max_length=200, null=True),
        ),
    ]
