from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Member  # 모델 가져오기
import json


# member 메인
def member_main(request):
    return render(request, 'member/member_main.html')  # 템플릿 파일 경로 지정

# 매장페이지 - 회원관리
def member_store(request):
    members = Member.objects.all() # 모든 회원 정보 가져오기
    return render(request, 'member/member_store.html', {'members': members})

# 매장페이지 - 회원관리 내 회원정보 수정
@csrf_exempt
def update_member(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            member_id = data.get("member_id")
            name = data.get("name")
            phone_num = data.get("phone_num")
            email = data.get("email")

            member = Member.objects.get(member_id=member_id)
            member.name = name
            member.phone_num = phone_num
            member.email = email
            member.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

# 마이페이지 - 회원정보
def member_page(request):
    return render(request, 'member/member_page.html')

# 마이페이지 - 회원정보수정
def member_edit(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        username = request.POST['username']
        phone_num = request.POST['phone_num']
        email = request.POST['email']

        # 아이디 중복 확인
        if User.objects.filter(username=user_id).exists():
            return render(request, "member/member_edit.html", {'error': '이미 존재하는 아이디입니다.'})

            return JsonResponse({"success": True})  # 성공 응답

    # 회원정보수정 페이지로 이동
    return render(request, 'member/member_edit.html')

# 마이페이지- 비밀번호변경
def member_pw(request):
    return render(request, 'member/member_pw.html')

# 마이페이지 - 회원탈퇴
def member_delete(request):
    return render(request, 'member/member_delete.html')

# 마이페이지 - 회원탈퇴사유 입력
def member_delete_detail(request):
    return render(request, 'member/member_delete_detail.html')