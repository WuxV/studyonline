# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from StudyOnline.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = u"在线学习网站注册激活链接"
        email_body = u"请点击下面的链接激活你的账号：http://192.168.0.13:8000/active/" + code

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = u"在线学习网站密码重置链接"
        email_body = u"请点击下面的链接重置你的密码：http://192.168.0.13:8000/reset/" + code

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = u"在线学习网站邮箱验证码"
        email_body = u"您的验证码为：" + code

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
