# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from __future__ import absolute_import

from celery import task

from utils import email_send
from utils.email_send import send_email

@task
def asy_send_email(email, send_type):
    return send_email(email, send_type)
