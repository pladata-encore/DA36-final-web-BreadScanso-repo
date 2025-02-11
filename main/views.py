from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.template.context_processors import request



def index(request):
    context = {'font_size': '20px'}
    return render(request, "main/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 != password2:
            return render(request, 'main/signup.html', {'error': '비밀번호가 일치하지 않습니다.'})

        if User.objects.filter(username=username).exists():
            return render(request, "main/signup.html", {'error': '이미 존재하는 아이디입니다.'})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)  # 자동 로그인
        return redirect("/")  # 메인 페이지로 이동

    return render(request, "main/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "main/login.html", {'error': '아이디 또는 비밀번호가 틀렸습니다.'})

    return render(request, "main/login.html")


# 잠시 주석 처리
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