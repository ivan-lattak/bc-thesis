# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 14:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refactoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='solved_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
