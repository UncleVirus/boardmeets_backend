# Generated by Django 3.2.9 on 2022-09-22 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_manager', '0011_alter_contractdetail_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractdetail',
            name='doc_ref',
            field=models.CharField(blank=True, default='7RFTOO15BV', max_length=200, null=True),
        ),
    ]
