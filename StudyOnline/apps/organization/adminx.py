# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import xadmin

from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-home'

class CourseOrgAdmin(object):
    list_display = ['name', 'click_nums', 'fav_nums', 'courses', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    # fk:foreign key,作用是当此model是另一个model的外键,以ajax加载的方式,即成为搜索，而不是默认的下拉
    #relfield_style = 'fk-ajax'

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
