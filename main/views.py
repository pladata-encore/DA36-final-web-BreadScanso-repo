from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from member.models import Member
from django.contrib import messages

def index(request):
    return render(request, "main/index.html")

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

        if password1 != password2:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'main/signup.html', {'user_id': member_id, 'name': name, 'phone_num': phone_num, 'email': email})

        if User.objects.filter(username=member_id).exists() or Member.objects.filter(member_id=member_id).exists():
            messages.error(request, '이미 존재하는 아이디입니다.')
            return render(request, "main/signup.html", {'user_id': member_id, 'name': name, 'phone_num': phone_num, 'email': email})

        # User 모델에 회원 생성
        user = User.objects.create_user(username=member_id, email=email, password=password1)

        # Member 모델에 회원 정보 저장 + User 연결
        member = Member.objects.create(
            user=user,
            member_id=member_id,
            name=name,
            phone_num=phone_num,
            email=email,
            age_group=age_group,
            sex=sex
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
            return redirect("/")
        else:
            messages.error(request, "아이디 또는 비밀번호가 틀렸습니다.")
            return redirect("main:login")

    return render(request, "main/login.html")

def user_logout(request):
    if request.method == "POST":  # post 요청만 허용!!!!1
        logout(request)
        request.session.flush()  # 세션 삭제!!!!
        return redirect("/")
    return HttpResponseNotAllowed(["POST"]) # get 허용 안 함 !!!!!


def check_user_id(request):
    member_id = request.GET.get('user_id', '')
    exists = User.objects.filter(username=member_id).exists() or Member.objects.filter(member_id=member_id).exists()
    return JsonResponse({"exists": exists})

def login_find(request):
    if request.method == "POST":
        username = request.POST.get('username')
        phone_num = request.POST.get('phone_num')
        email = request.POST.get('email')

        try:
            member = Member.objects.get(name=username, phone_num=phone_num, email=email)
            messages.success(request, f"회원님의 아이디는 {member.member_id} 입니다.")
            return redirect("main:login_find")
        except Member.DoesNotExist:
            messages.error(request, "일치하는 회원 정보가 없습니다.")
            return redirect("main:login_find")

    return render(request, "main/login_find.html")
