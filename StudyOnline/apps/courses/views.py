# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, Lesson, Video
from operation.models import UserFavorite, UserCourse, CourseComments
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        # 默认最新课程排序
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        
        # 课程关键字搜索
        keywords = request.GET.get("keywords", '')
        if keywords:
            all_courses = all_courses.filter(
                    Q(name__icontains=keywords)|
                    Q(desc__icontains=keywords)|
                    Q(detail__icontains=keywords))

        # 对课程进行热门和参与人数排序
        sort = request.GET.get('sort', "")
        if sort == "hot":
            all_courses = all_courses.order_by("-click_nums")
        elif sort == "students":
            all_courses = all_courses.order_by("-students")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        # Provide Paginator with the request object for complete querystring generation
        # 参数1:要进行分页的列表;参数2:每一页显示的数量(必须传,github这一点有误);
        p = Paginator(all_courses, 3, request=request)
        
        courses = p.page(page)

        return render(request, "course-list.html", {
            "courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "keywords": keywords,
        })

class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加点击数
        course.click_nums += 1
        course.save()
        # 相关课程
        related_course = Course.objects.filter(category=course.category).exclude(id=course_id)[0]

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                has_fav_org = True

        return render(request, "course-detail.html", {
            "course":course,
            "related_course":related_course,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
        })

class CourseVideoView(LoginRequiredMixin, View):
    """
    课程视频页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 如果没有用户学习该课程的记录，则添加
        if not UserCourse.objects.filter(user=request.user, course=course):
            new_user_course = UserCourse(user=request.user, course=course)
            new_user_course.save()
            course.students += 1
            course.save()

        # 获取学过该课程的同学还学过的其他课程
        user_courses = UserCourse.objects.filter(course=course)
        users = [user_course.user for user_course in user_courses]
        other_user_courses = UserCourse.objects.filter(user__in=users).exclude(course=course)
        other_course_ids = [other_user_course.course.id for other_user_course in other_user_courses]
        other_courses = Course.objects.filter(id__in=other_course_ids).order_by("-click_nums")[:3]

        #other_courses = []
        #user_courses = UserCourse.objects.filter(course=course)
        #for user_course in user_courses:
        #    user = user_course.user
        #    other_user_courses = UserCourse.objects.filter(user=user).exclude(course=course)
        #    for other_user_course in other_user_courses:
        #        if other_user_course.course not in other_courses:
        #            other_courses.append(other_user_course.course)
        #other_courses = other_courses[:3]

        current_page = "video"
        return render(request, "course-video.html", {
            "course": course,
            "other_courses": other_courses,
            "current_page": current_page,
            })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 获取学过该课程的同学还学过的其他课程
        other_courses = []
        user_courses = UserCourse.objects.filter(course=course)
        for user_course in user_courses:
            user = user_course.user
            other_user_courses = UserCourse.objects.filter(user=user).exclude(course=course)
            for other_user_course in other_user_courses:
                if other_user_course.course not in other_courses:
                    other_courses.append(other_user_course.course)
        other_courses = other_courses[:3]

        current_page = "comment"
        return render(request, "course-comment.html", {
            "course": course,
            "other_courses": other_courses,
            "current_page": current_page,
            })

    def post(self, request, course_id):
        comments = request.POST.get("comments", "")
        course = Course.objects.get(id=int(course_id))

        if comments:
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course = course
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"评论出错"}', content_type="application/json")


class CoursePlayView(LoginRequiredMixin, View):
    """
    课程播放页
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 如果没有用户学习该课程的记录，则添加
        if not UserCourse.objects.filter(user=request.user, course=course):
            new_user_course = UserCourse(user=request.user, course=course)
            new_user_course.save()
            course.students += 1
            course.save()

        # 获取学过该课程的同学还学过的其他课程
        user_courses = UserCourse.objects.filter(course=course)
        users = [user_course.user for user_course in user_courses]
        other_user_courses = UserCourse.objects.filter(user__in=users).exclude(course=course)
        other_course_ids = [other_user_course.course.id for other_user_course in other_user_courses]
        other_courses = Course.objects.filter(id__in=other_course_ids).order_by("-click_nums")[:3]

        current_page = "video"
        return render(request, "course-play.html", {
            "course": course,
            "other_courses": other_courses,
            "current_page": current_page,
            "video": video,
        })

