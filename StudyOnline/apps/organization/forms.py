# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import re

from django import forms

from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        pattern = u"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if re.match(pattern, mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码不正确", code="mobile_invalid")
