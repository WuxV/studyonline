# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-14 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20170513_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Announcement',
            field=models.CharField(default='', max_length=100, verbose_name='\u8bfe\u7a0b\u516c\u544a'),
        ),
    ]
