# Generated by Django 3.2.9 on 2022-07-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signatures', '0004_alter_documentstobesigned_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstobesigned',
            name='doc_ref',
            field=models.CharField(blank=True, default='52TYTQQPBF', max_length=200, null=True),
        ),
    ]
