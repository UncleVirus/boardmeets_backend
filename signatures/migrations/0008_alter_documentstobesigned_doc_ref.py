# Generated by Django 3.2.9 on 2022-09-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signatures', '0007_alter_documentstobesigned_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstobesigned',
            name='doc_ref',
            field=models.CharField(blank=True, default='WWIUZG999V', max_length=200, null=True),
        ),
    ]
