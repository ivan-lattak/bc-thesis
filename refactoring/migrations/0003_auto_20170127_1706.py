# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refactoring', '0002_solution_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='exercise',
        ),
        migrations.AddField(
            model_name='exercise',
            name='original_tests',
            field=models.TextField(default='NEW FIELD PLACEHOLDER'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solution',
            name='tests',
            field=models.TextField(default='NEW FIELD PLACEHOLDER'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TestCase',
        ),
    ]
