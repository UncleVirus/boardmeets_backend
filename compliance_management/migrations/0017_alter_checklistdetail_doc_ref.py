# Generated by Django 3.2.9 on 2022-09-22 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance_management', '0016_alter_checklistdetail_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistdetail',
            name='doc_ref',
            field=models.CharField(blank=True, default='ALTVTVEPNH', max_length=200, null=True),
        ),
    ]
