# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-05 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0002_task_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='event_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
