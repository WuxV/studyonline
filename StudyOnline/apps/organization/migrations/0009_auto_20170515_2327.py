# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-15 23:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20170515_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=18, verbose_name='\u6559\u5e08\u5e74\u9f84'),
        ),
    ]
