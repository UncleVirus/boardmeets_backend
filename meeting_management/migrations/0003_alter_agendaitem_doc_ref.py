# Generated by Django 3.2.9 on 2022-05-20 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_management', '0002_alter_agendaitem_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendaitem',
            name='doc_ref',
            field=models.CharField(blank=True, default='YYFFRXDHQX', max_length=200, null=True),
        ),
    ]
