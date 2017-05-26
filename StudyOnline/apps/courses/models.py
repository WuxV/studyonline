# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org =  models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    detail = UEditorField(default='', width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/", verbose_name=u'课程详情')
    degree = models.CharField(max_length=2, verbose_name=u'难度', choices=(("cj",u"初级"), ("zj",u"中级"), ("gj",u"高级")))
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    teacher =  models.ForeignKey(Teacher, verbose_name=u"课程讲师", null=True, blank=True)
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default="", max_length=20, verbose_name=u"课程类别")
    course_needs = models.CharField(default="", max_length=300, verbose_name=u"课程须知")
    what_can_learn = models.CharField(default="", max_length=300, verbose_name=u"能学到什么")
    Announcement = models.CharField(default="", max_length=100, verbose_name=u"课程公告")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否是轮播图")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_nums(self):
        # 获取课程对应的章节数
        return self.lesson_set.all().count()
    get_lesson_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</a>")
    go_to.short_description = "跳转"

    def get_learn_users(self):
        # 获取学习课程的用户
        return self.usercourse_set.all().order_by("-add_time")[:5]

    def get_all_lessons(self):
        # 获取课程的所有章节
        return self.lesson_set.all()

    def get_all_courseresource(self):
        # 获取课程的所有资源
        return self.courseresource_set.all()

    def get_all_comments(self):
        # 获取课程的所有评论
        return self.coursecomments_set.all().order_by("-add_time")


class BannerCourse(Course):
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = u"轮播课程"
        # 表示不是新建表,目的是在admin后台显示不同类型的课程
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.course.name + '.' + self.name

    def get_all_videos(self):
        # 获取章节的所有视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    url = models.CharField(default="", max_length=200, verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.lesson.name + '.' + self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.course.name + '.' + self.name
