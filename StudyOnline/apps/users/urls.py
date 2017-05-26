# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.conf.urls import url, include

from .views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, UserCenterInfoView
from .views import UserImageUploadView, UserPwdUpdateView, UserSendEmailCodeView, UserUpdateEmailView
from .views import UserMyCoursesView, UserMyFavCoursesView, UserMyFavOrgsView, UserMyFavTeachersView, UserMyMsgView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name="reset_pwd"),
    url(r'^modify/$', ModifyPwdView.as_view(), name="modify_pwd"),
    
    # 个人中心信息页
    url(r'^info/$', UserCenterInfoView.as_view(), name="user_info"),

    # 用户上传头像
    url(r'^image/upload/$', UserImageUploadView.as_view(), name="user_image"),

    # 个人中心修改密码
    url(r'^update/pwd/$', UserPwdUpdateView.as_view(), name="user_pwd"),

    # 个人中心发送邮箱验证码
    url(r'^sendemail/code/$', UserSendEmailCodeView.as_view(), name="user_code"),

    # 个人中心修改邮箱
    url(r'^update/email/$', UserUpdateEmailView.as_view(), name="user_email"),

    # 个人中心我的课程页
    url(r'^mycourses/$', UserMyCoursesView.as_view(), name="mycourse"),

    # 个人中心我的收藏课程页
    url(r'^myfav/courses/$', UserMyFavCoursesView.as_view(), name="myfav_course"),

    # 个人中心我的收藏机构页
    url(r'^myfav/orgs/$', UserMyFavOrgsView.as_view(), name="myfav_org"),

    # 个人中心我的收藏教师页
    url(r'^myfav/teachers/$', UserMyFavTeachersView.as_view(), name="myfav_teacher"),

    # 个人中心我的消息页
    url(r'^mymsg/$', UserMyMsgView.as_view(), name="mymsg"),
]
