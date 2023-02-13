# Generated by Django 3.2.9 on 2022-07-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boardleaders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chairman', models.CharField(max_length=100)),
                ('ceo', models.CharField(max_length=100)),
                ('secretary', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyname', models.CharField(max_length=500)),
                ('serverid', models.CharField(max_length=500)),
                ('licensekey', models.CharField(max_length=500)),
                ('expiryperiod', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Missionstatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('missionstatement', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Orgdescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orgdescription', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Orgname',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orgname', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Sociallinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.CharField(max_length=1000)),
                ('twitter', models.CharField(max_length=1000)),
                ('linkedin', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Vissionstatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vissionstatement', models.CharField(max_length=300)),
            ],
        ),
    ]
