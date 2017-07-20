# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from __future__ import absolute_import 

import os
import django

from celery import Celery,platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudyOnline.settings')
django.setup()

app = Celery('users')
platforms.C_FORCE_ROOT = True

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
