# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite

# Create your views here.

class OrgView(View):
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 计算机构的课程数和学习人数
        for org in all_orgs:
            #org.courses = org.course_set.all().count()
            students_list = [course.students for course in org.course_set.all()]
            org.students = sum(students_list)
            org.save()

        # 课程机构关键字搜索
        keywords = request.GET.get("keywords", '')
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords))

        # 城市
        all_cities = CityDict.objects.all()

        # 对课程机构进行城市筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        
        # 对课程机构进行类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        
        # 对课程机构进行学生人数和课程数排序
        sort = request.GET.get('sort', "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-courses")

        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        # Provide Paginator with the request object for complete querystring generation
        # 参数1:要进行分页的列表;参数2:每一页显示的数量(必须传,github这一点有误);
        p = Paginator(all_orgs, 5, request=request)
        
        orgs = p.page(page)
        
        return render(request, "org-list.html", {
            "orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "keywords": keywords,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type="application/json")


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 机构点击量加1
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]
        current_page = "home"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        
        return render(request, "org-detail-homepage.html", {
                "all_courses":all_courses,
                "all_teachers":all_teachers,
                "course_org":course_org,
                "current_page":current_page,
                "has_fav":has_fav,
            })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        current_page = "course"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        return render(request, "org-detail-course.html", {
                "all_courses":all_courses,
                "course_org":course_org,
                "current_page":current_page,
                "has_fav":has_fav,
            })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = "desc"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        return render(request, "org-detail-desc.html", {
                "course_org":course_org,
                "current_page":current_page,
                "has_fav":has_fav,
            })


class OrgTeacherView(View):
    """
    机构教师列表页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        return render(request, "org-detail-teachers.html", {
                "all_teachers":all_teachers,
                "course_org":course_org,
                "has_fav":has_fav,
            })

class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        
        # 判断是否已收藏
        fav_exist = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if fav_exist:
            # 如果已收藏，则表示用户取消收藏
            fav_exist.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) != 0 and int(fav_type) != 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()
        rank_teachers = all_teachers.order_by("-click_nums")[:3]

        # 课程教师关键字搜索
        keywords = request.GET.get("keywords", '')
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords)|
                    Q(work_company__icontains=keywords)|
                    Q(work_position__icontains=keywords))

        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        # 对教师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        # Provide Paginator with the request object for complete querystring generation
        # 参数1:要进行分页的列表;参数2:每一页显示的数量(必须传,github这一点有误);
        p = Paginator(all_teachers, 3, request=request)
        
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "teachers": teachers,    
            "teacher_nums": teacher_nums,
            "rank_teachers": rank_teachers,
            "sort": sort,
            "keywords": keywords,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        rank_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        # 教师点击量加1
        teacher.click_nums += 1
        teacher.save()

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher_id), fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org_id), fav_type=2):
                has_fav_org = True
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "rank_teachers": rank_teachers,
            "has_fav_teacher": has_fav_teacher,
            "has_fav_org": has_fav_org,
        })
