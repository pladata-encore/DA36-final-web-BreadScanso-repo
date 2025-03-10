from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from member.models import Member
from django.contrib import messages
import re
from .utils import upload_profile_image_to_s3
import random
import string
from menu.models import Item

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.urls import reverse


def index(request):
    member = None  # 기본값을 None으로 설정

    if request.user.is_authenticated:  # 로그인한 경우에만 가져오기
        member = request.user.member

    # 하나의 딕셔너리로 합쳐서 전달
    context = {
        'member': member
    }
    return render(request, "main/index.html", context)

def signup(request):
    if request.method == "POST":
        member_id = request.POST.get('user_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        phone_num = request.POST.get('phone_num')
        email = request.POST.get('email')
        age_group = request.POST.get('age_group')
        sex = request.POST.get('sex')
        profile = request.FILES.get("profile")

        # User 모델에 회원 생성
        user = User.objects.create_user(username=member_id, email=email, password=password1)

        # S3에 프로필 이미지 업로드 후 URL 저장
        profile_url = upload_profile_image_to_s3(profile) if profile else None

        # Member 모델에 회원 정보 저장 + User 연결
        member = Member.objects.create(
            user=user,
            member_id=member_id,
            name=name,
            phone_num=phone_num,
            email=email,
            age_group=age_group,
            sex=sex,
            profile_image=profile_url
        )

        login(request, user)
        messages.success(request, f"{name}님, 회원가입이 완료되었습니다! 환영합니다. 🎉")
        return redirect("main:index")

    return render(request, "main/signup.html")


def user_login(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        user = authenticate(request, username=user_id, password=password)

        if user is not None:
            login(request, user)

            try:
                member = Member.objects.get(user=user)

                # 로그인한 사용자 정보를 세션에 저장
                request.session['member_type'] = member.member_type
                request.session['store'] = member.store
                request.session['earning_rate'] = str(float(member.earning_rate))
                return redirect("main:index")

            except Member.DoesNotExist:
                messages.error(request, "회원 정보가 없습니다.")
                return redirect("main:login")
        else:
            messages.error(request, "아이디 또는 비밀번호가 틀렸습니다.")
            return redirect("main:login")

    return render(request, "main/login.html")



def user_logout(request):
    if request.method == "POST":  # post 요청만 허용
        logout(request)
        request.session.flush()  # 세션 삭제
        return redirect("main:index")
    return HttpResponseNotAllowed(["POST"]) # get 허용 안 함


def check_user_id(request):
    member_id = request.GET.get('user_id', '').strip()

    # 아이디 유효성 검사 (영소문자+숫자 4~12자리)
    if not re.match(r'^[a-z0-9]{4,12}$', member_id):
        return JsonResponse({"valid": False, "message": "아이디는 영소문자+숫자 4~12자리여야 합니다."})

    # DB에서 중복 확인
    exists = User.objects.filter(username=member_id).exists() or Member.objects.filter(member_id=member_id).exists()

    if exists:
        return JsonResponse({"valid": False, "message": "이미 사용 중인 아이디입니다."})

    return JsonResponse({"valid": True, "message": "사용 가능한 아이디입니다."})


def generate_temp_password(length=10):
    """랜덤한 임시 비밀번호 생성"""
    characters = string.ascii_letters + string.digits  # 알파벳(대소문자) + 숫자 포함
    return ''.join(random.choices(characters, k=length))


def login_find(request):
    if request.method == "POST":
        username = request.POST.get('username')
        phone_num = request.POST.get('phone_num')
        email = request.POST.get('email')

        try:
            member = Member.objects.get(name=username, phone_num=phone_num, email=email)

            try:
                user = User.objects.get(username=member.member_id)

                temp_password = generate_temp_password()
                user.set_password(temp_password)
                user.save()

                return render(request, "main/login_find.html", {
                    "found_id": member.member_id,
                    "temp_password": temp_password,  # 새로운 비밀번호를 템플릿에 전달
                    "username": username,
                    "phone_num": phone_num,
                    "email": email,
                })

            except User.DoesNotExist:
                messages.error(request, "회원 정보는 존재하지만, 계정 정보(auth_user)를 찾을 수 없습니다.")
                return render(request, "main/login_find.html")

        except Member.DoesNotExist:
            messages.error(request, "일치하는 회원 정보가 없습니다.")
            return render(request, "main/login_find.html")

    return render(request, "main/login_find.html")


def store_signup(request):
    if request.method == "POST":
        member_id = request.POST.get('user_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        phone_num = request.POST.get('phone_num')
        email = request.POST.get('email')
        age_group = request.POST.get('age_group')
        sex = request.POST.get('sex')
        profile = request.FILES.get("profile")

        # User 모델에 회원 생성
        user = User.objects.create_user(username=member_id, email=email, password=password1)

        # S3에 프로필 이미지 업로드 후 URL 저장
        profile_url = upload_profile_image_to_s3(profile) if profile else None

        # Member 모델에 회원 정보 저장 + User 연결
        member = Member.objects.create(
            user=user,
            member_id=member_id,
            name=name,
            phone_num=phone_num,
            email=email,
            age_group=age_group,
            sex=sex,
            profile_image=profile_url
        )
        return redirect('store:member_store')
    member = request.user.member

    return render(request, "main/store_signup.html", {'member': member})

def google_login(request):
    # google 로그인 URL로 직접 리다이렉트
    return redirect('/accounts/google/login/')

def naver_login(request):
    # naver 로그인 URL로 직접 리다이렉트
    return redirect('/accounts/naver/login/')

# 메인홈-product 신제품 가져오기 코드 - 안나옴/일단보류
# def product(request):
#         new_items = Item.objects.filter(is_new=True)[:3]  # 신제품 중 3개만 가져오기
#
#         context = {
#             'new_items': new_items,
#         }
#         return render(request, "menu/menu_main.html", context)
