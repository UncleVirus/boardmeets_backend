# Generated by Django 3.2.9 on 2023-01-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signatures', '0019_alter_documentstobesigned_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstobesigned',
            name='doc_ref',
            field=models.CharField(blank=True, default='10I7KXQT91', max_length=200, null=True),
        ),
    ]
