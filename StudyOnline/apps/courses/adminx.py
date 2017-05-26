# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_lesson_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums']
    exclude = ['click_nums']
    model_icon = 'fa fa-book'
    list_editable = ['degree', 'desc']
    refresh_times = [3, 5]
    inlines = [LessonInline, CourseResourceInline]
    # 指明某字段采用的样式
    style_fields = {"detail":"ueditor"}
    import_excel = True

    # 重载父类的queryset方法，对列表数据进行过滤
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 重写父类的save_models方法，在保存课程的时候统计对应机构的课程数 
    def save_models(self):
        self.new_obj.save()
        if self.new_obj.course_org:
            course_org = self.new_obj.course_org
            course_org.courses = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    # 重载父类的post方法，获取后台post数据
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums']
    exclude = ['click_nums']
    model_icon = 'fa fa-book'
    inlines = [LessonInline, CourseResourceInline]

    # 对列表数据进行过滤
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-bookmark'

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    model_icon = 'fa fa-video-camera'

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']
    model_icon = 'fa fa-file'

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
