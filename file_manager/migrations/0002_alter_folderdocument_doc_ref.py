# Generated by Django 3.2.9 on 2022-05-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folderdocument',
            name='doc_ref',
            field=models.CharField(blank=True, default='10B0RWK01O', max_length=200, null=True),
        ),
    ]
