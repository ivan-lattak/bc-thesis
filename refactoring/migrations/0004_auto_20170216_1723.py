# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refactoring', '0003_auto_20170127_1706'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([('code', 'tests', 'session')]),
        ),
    ]