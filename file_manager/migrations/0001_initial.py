# Generated by Django 3.2.9 on 2022-04-05 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file_manager.folder')),
                ('permissions', models.ManyToManyField(blank=True, related_name='permissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FolderDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('doc_name', models.CharField(max_length=200)),
                ('doc_ref', models.CharField(blank=True, default='W397A6959L', max_length=200, null=True)),
                ('type', models.CharField(choices=[('LINK', 'LINK'), ('VIDEO', 'VIDEO'), ('FILE', 'FILE')], default='FILE', max_length=50)),
                ('doc_file', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_manager.folder')),
            ],
        ),
    ]
