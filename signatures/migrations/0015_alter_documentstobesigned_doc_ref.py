# Generated by Django 3.2.9 on 2022-09-22 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signatures', '0014_alter_documentstobesigned_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstobesigned',
            name='doc_ref',
            field=models.CharField(blank=True, default='EE7NA8O0RI', max_length=200, null=True),
        ),
    ]
