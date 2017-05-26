#/usr/bin/env python
# -*- coding: utf-8 -*-
import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner
from .models import UserProfile


class BaseSetting(object):
    # 主题功能，默认为False
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    # 页面左上角标题,页头
    site_title = u"在线学习后台管理系统"
    # 页面底部公司名,页脚
    site_footer = u"在线学习网"
    # 收起app下的表
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-user'

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fa fa-picture-o'

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
