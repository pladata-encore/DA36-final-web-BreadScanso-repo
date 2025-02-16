from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import request


# 예진님 코드 참고용
# def kiosk_main(request):
#     return render(request, 'kiosk/kiosk_main.html')  # kiosk_main 템플릿 파일 경로 지정

# 메인 설정
def index(request):
    # context = {'font_size': '20px'}
    return render(request, "main/index.html")

# 아이디 중복 체크 - 나중에 기능 추가로 사용할 예정
def check_user_id(request):
    user_id = request.GET.get('user_id', '')
    exists = User.objects.filter(username=user_id).exists()
    return JsonResponse({"exists": exists})

# 회원가입 설정
def signup(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = request.POST['username']
        phone_num = request.POST['phone_num']
        email = request.POST['email']

        # 비밀번호 확인
        if password1 != password2:
            return render(request, 'main/signup.html', {'error': '비밀번호가 일치하지 않습니다.'})

        # 아이디 중복 확인
        if User.objects.filter(username=user_id).exists():
            return render(request, "main/signup.html", {'error': '이미 존재하는 아이디입니다.'})

        # 회원 생성
        user = User.objects.create_user(user_id=user_id, password=password1, email=email)

        # 자동 로그인
        login(request, user)

        return JsonResponse({"success": True})  # 성공 응답

    # 메인 페이지로 이동
    return render(request, "main/signup.html")

# 로그인 설정
def login(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        password = request.POST['password']
        user = authenticate(request, user_id=user_id, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "main/login.html", {'error': '아이디 또는 비밀번호가 틀렸습니다.'})

    return render(request, "main/login.html")

# ID/PW 찾기 설정
def login_find(request):
    if request.method == "POST":
        username = request.POST['username']
        phone_num = request.POST['phone_num']
        email = request.POST['email']
        user = authenticate(request, username=username, phone_num=phone_num, email=email)

    return render(request, "main/login_find.html")

# 잠시 주석 처리

# 회원가입 설정
# else:
#     return JsonResponse({"exists": False}) # 사용 가능한 아이디

# def signup(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # 회원가입 후 자동 로그인
#             return redirect("/")  # 회원가입 후 메인 페이지로 이동
#     else:
#         form = UserCreationForm()
#     return render(request, "main/signup.html", {"form": form})