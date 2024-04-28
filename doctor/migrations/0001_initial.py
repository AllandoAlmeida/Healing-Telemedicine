# Generated by Django 5.0.4 on 2024-04-28 16:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OpenDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('scheduled', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('zidCode', models.CharField(max_length=15)),
                ('street', models.CharField(max_length=100)),
                ('neighborhood', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('register_geral', models.ImageField(upload_to='rgs')),
                ('medical_identity_card', models.ImageField(upload_to='mic')),
                ('photo', models.ImageField(upload_to='fotos_profil')),
                ('description', models.TextField(blank=True, null=True)),
                ('query_value', models.FloatField(default=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('specialty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='doctor.specialties')),
            ],
        ),
    ]