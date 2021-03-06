# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 15:21
from __future__ import unicode_literals
import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='last_dislike_at',
        ),
        migrations.RemoveField(
            model_name='like',
            name='last_like_at',
        ),
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True,
                                       default=datetime.datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='titledimage',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='titledimage',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
