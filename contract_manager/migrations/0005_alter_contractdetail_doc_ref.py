# Generated by Django 3.2.9 on 2022-07-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_manager', '0004_alter_contractdetail_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractdetail',
            name='doc_ref',
            field=models.CharField(blank=True, default='PYH52AWJ7O', max_length=200, null=True),
        ),
    ]
