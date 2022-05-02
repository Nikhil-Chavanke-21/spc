# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-20 20:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.BinaryField()),
                ('filename', models.CharField(max_length=100, null=True)),
                ('filetype', models.CharField(max_length=50, null=True)),
                ('md5sum', models.CharField(max_length=32, null=True)),
                ('date_upload', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]