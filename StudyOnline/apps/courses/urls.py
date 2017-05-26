# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, CoursePlayView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),       
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),       
    # 课程视频页
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name="course_video"),
    # 课程评论页
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),       
    # 课程播放页
    url(r'^play/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name="course_play"),       
]
