# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import re

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})

class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

class UserImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UserSendEmailCodeForm(forms.Form):
    email = forms.EmailField(required=True)

class UserUpdateEmailForm(forms.Form):
    email = forms.EmailField(required=True)
    code = forms.CharField(required=True)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'email', 'birthday', 'address', 'mobile']

    #def clean_mobile(self):
    #    """
    #    验证手机号码是否合法
    #    """
    #    mobile = self.cleaned_data['mobile']
    #    pattern = u"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
    #    if re.match(pattern, mobile):
    #        return mobile
    #    else:
    #        raise forms.ValidationError(u"手机号码不正确", code="mobile_invalid")
