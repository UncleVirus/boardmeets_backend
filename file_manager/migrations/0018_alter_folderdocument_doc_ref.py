# Generated by Django 3.2.9 on 2022-09-22 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0017_alter_folderdocument_doc_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folderdocument',
            name='doc_ref',
            field=models.CharField(blank=True, default='FGCLFZ65RK', max_length=200, null=True),
        ),
    ]
