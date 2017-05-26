# -*- coding: utf-8 -*-
"""StudyOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

from .settings import MEDIA_ROOT, STATIC_ROOT
#from .settings import MEDIA_ROOT
from users.views import IndexView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    # 首页
    #url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^$', IndexView.as_view(), name="index"),

    # 验证码
    url(r'^captcha/', include('captcha.urls')),

    # 用户相关url配置
    url(r'^user/', include('users.urls', namespace="user")),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),

    # 配置上传文件的访问处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    
    # 生产环境静态文件处理
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
