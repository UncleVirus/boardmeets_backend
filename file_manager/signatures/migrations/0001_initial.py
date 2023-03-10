# Generated by Django 3.2.9 on 2022-04-05 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(max_length=200000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentsToBeSigned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature_title', models.CharField(blank=True, max_length=250)),
                ('open_date', models.DateTimeField(null=True)),
                ('close_date', models.DateTimeField(null=True)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('document', models.CharField(blank=True, max_length=200000, null=True)),
                ('doc_ref', models.CharField(blank=True, default='19V6XCNK7S', max_length=200, null=True)),
                ('status', models.CharField(default='Draft', max_length=250)),
                ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file_manager.folder')),
                ('signers', models.ManyToManyField(blank=True, related_name='doc_signers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentSignatureAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xfdf_string', models.TextField(default='')),
                ('is_to_sign', models.BooleanField(default=False)),
                ('signed_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('signature_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signatures.documentstobesigned')),
                ('signer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
