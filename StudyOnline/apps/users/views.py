# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserProfileForm
from .forms import UserImageUploadForm, UserSendEmailCodeForm, UserUpdateEmailForm
from utils.email_send import send_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserFavorite, UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher

# Create your views here.


# 重定义验证用户存在方法
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        banners = Banner.objects.order_by("index")
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "orgs": orgs,
        })


class ActiveUserView(View):
    """
    用户激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for recode in all_records:
                email = recode.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "url_error.html")
        #return render(request, "login.html")


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {"register_form": register_form, "msg":"用户已存在"})

            password = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()

            send_email(email, "register")
            return render(request, "send_success.html")
        else:
            return render(request, "register.html", {"register_form": register_form})
            

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # 重定向到首页
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg":"用户未激活"})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        # 重定向到首页
        return HttpResponseRedirect(reverse("index"))


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # FIXME 判断email是否在用户表中
            send_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetPwdView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for recode in all_records:
                email = recode.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "url_error.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserCenterInfoView(LoginRequiredMixin, View):
    """
    个人中心信息页
    """
    def get(self, request):
        user_profile = UserProfile.objects.get(id=request.user.id)
        return render(request, "usercenter-info.html", {
            "user": user_profile,
        })

    def post(self, request):
        user_form = UserProfileForm(request.POST, instance=request.user)
        print json.dumps(user_form.errors)
        if user_form.is_valid():
            user_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_form.errors), content_type="application/json")

class UserImageUploadView(LoginRequiredMixin, View):
    """
    用户头像修改
    """
    def post(self, request):
        user_form = UserImageUploadForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"failure", "msg":"修改出错"}', content_type="application/json")


class UserPwdUpdateView(LoginRequiredMixin, View):
    """
    个人中心密码修改
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"failure", "msg":"两次密码不一致"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()

            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


class UserSendEmailCodeView(LoginRequiredMixin, View):
    """
    个人中心发送邮箱验证码
    """
    def post(self, request):
        email_form = UserSendEmailCodeForm(request.POST)
        if email_form.is_valid():
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email):
                return HttpResponse('{"status":"failure", "msg":"邮箱已存在"}', content_type="application/json")

            send_email(email, "update_email")
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(email_form.errors), content_type="application/json")



class UserUpdateEmailView(LoginRequiredMixin, View):
    """
    个人中心修改邮箱
    """
    def post(self, request):
        email_form = UserUpdateEmailForm(request.POST)
        if email_form.is_valid():
            email = request.POST.get("email")
            code = request.POST.get("code")
            all_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
            if all_records:
                for recode in all_records:
                    user = request.user
                    user.email = email
                    user.save()
                    return HttpResponse('{"status":"success"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"failure", "msg":"邮箱或验证码错误"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(email_form.errors), content_type="application/json")


class UserMyCoursesView(View):
    """
    个人中心我的课程页
    """
    def get(self, request):
        return render(request, "usercenter-mycourse.html", {})


class UserMyFavCoursesView(View):
    """
    个人中心我的收藏课程页
    """
    def get(self, request):
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        course_ids = [fav_course.fav_id for fav_course in user_fav_courses]
        courses = Course.objects.filter(id__in=course_ids)
        return render(request, "usercenter-fav-course.html", {
            "courses": courses,
        })


class UserMyFavOrgsView(View):
    """
    个人中心我的收藏机构页
    """
    def get(self, request):
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        org_ids = [fav_org.fav_id for fav_org in user_fav_orgs]
        orgs = CourseOrg.objects.filter(id__in=org_ids)
        return render(request, "usercenter-fav-org.html", {
            "orgs": orgs,
        })


class UserMyFavTeachersView(View):
    """
    个人中心我的收藏教师页
    """
    def get(self, request):
        user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_ids = [fav_teacher.fav_id for fav_teacher in user_fav_teachers]
        teachers = Teacher.objects.filter(id__in=teacher_ids)
        return render(request, "usercenter-fav-teacher.html", {
            "teachers": teachers,
        })


class UserMyMsgView(View):
    """
    个人中心我的消息页
    """
    def get(self, request):
        personal_msgs = UserMessage.objects.filter(user=int(request.user.id)).order_by("-add_time")
        # 将未读消息改为已读
        for msg in personal_msgs:
            if msg.has_read == False:
                msg.has_read = True
                msg.save()

        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        
        p = Paginator(personal_msgs, 5, request=request)
        personal_msgs = p.page(page)

        return render(request, "usercenter-message.html", {
            "personal_msgs": personal_msgs,
        })

# 全局404处理函数
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

# 全局500处理函数
def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
