from django.contrib.auth import update_session_auth_hash, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Member  # 모델 가져오기
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .utils import upload_profile_image_to_s3
import traceback
from django.db import connection


# member 메인
def member_main(request):
    return render(request, 'member/member_main.html')  # 템플릿 파일 경로 지정

# 회원 마이페이지
def member_page(request):
    if not request.user.is_authenticated:
        messages.error(request, "로그인이 필요합니다.")
        return redirect("main:login")
    try:
        member = Member.objects.get(user=request.user)
        return render(request, "member/member_page.html", {"member": member})
    except Member.DoesNotExist:
        messages.error(request, "회원 정보가 존재하지 않습니다.")
        return redirect("main:index")


@login_required
@require_http_methods(["GET", "POST"])
def member_edit(request):
    if request.method == "POST":
        try:
            member = request.user.member  # 현재 로그인한 회원 정보 가져오기

            # 회원 정보 업데이트
            member.name = request.POST.get('name')
            member.phone_num = request.POST.get('phone_num')
            member.email = request.POST.get('email')
            member.age_group = request.POST.get('age_group')
            member.sex = request.POST.get('sex')

            # 프로필 이미지 처리
            if 'profile_image' in request.FILES:
                member.profile_image = request.FILES['profile_image']

            member.save()  # 변경 사항 저장

            return JsonResponse({
                'success': True,
                'message': '회원정보가 성공적으로 수정되었습니다.'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    # GET 요청 처리 (회원 정보 페이지 렌더링)
    member = request.user.member

    # 이메일 주소 분리하기
    email_parts = {'id': '', 'domain': ''}
    if member.email and '@' in member.email:
        email_id, email_domain = member.email.split('@', 1)
        email_parts = {'id': email_id, 'domain': email_domain}

    return render(request, 'member/member_edit.html', {
        'member': member,
        'email_parts': email_parts
    })


# 아이디 중복확인
def check_user_id(request):
    user_id = request.GET.get('user_id', '')
    if not user_id:
        return JsonResponse({'available': False, 'message': '아이디를 입력해주세요.'})

    # 최소 길이 체크
    if len(user_id) < 4:
        return JsonResponse({'available': False, 'message': '아이디는 최소 4자 이상이어야 합니다.'})

    # 기존 회원 아이디와 비교
    exists = Member.objects.filter(member_id=user_id).exists()  # Member는 실제 모델명으로 변경해야 함

    if exists:
        return JsonResponse({'available': False, 'message': '이미 사용 중인 아이디입니다.'})
    else:
        return JsonResponse({'available': True, 'message': '사용 가능한 아이디입니다.'})

@login_required
def member_pw(request):
    if request.method == 'POST':
        current_password = request.POST.get('password1')
        new_password = request.POST.get('password2')
        password_confirm = request.POST.get('password3')

        user = request.user

        # 현재 비밀번호 검증
        if not user.check_password(current_password):
            messages.error(request, '현재 비밀번호가 일치하지 않습니다.')
            return render(request, 'member/member_pw.html')

        # 새 비밀번호 검증
        if new_password != password_confirm:
            messages.error(request, '새 비밀번호가 일치하지 않습니다.')
            return render(request, 'member/member_pw.html')

        # 비밀번호 길이 검증
        if len(new_password) < 4 or len(new_password) > 12:
            messages.error(request, '비밀번호는 4~12자리로 입력해주세요.')
            return render(request, 'member/member_pw.html')

        # 현재 비밀번호와 새 비밀번호가 같은지 검증
        if current_password == new_password:
            messages.error(request, '현재 비밀번호와 새 비밀번호가 같습니다.')
            return render(request, 'member/member_pw.html')

        try:
            # 비밀번호 변경
            user.set_password(new_password)
            user.save()

            # 세션 유지를 위한 코드 추가
            update_session_auth_hash(request, user)

            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            # 모달 표시를 위한 context 추가
            return render(request, 'member/member_pw.html', {'show_modal': True})

        except Exception as e:
            messages.error(request, '비밀번호 변경 중 오류가 발생했습니다.')
            return render(request, 'member/member_pw.html')

    # GET 요청 처리
    member = request.user.member  # 또는 해당하는 회원 모델 인스턴스 가져오기
    return render(request, 'member/member_pw.html', {'member': member})

# @login_required
@require_http_methods(["POST"])
def check_password(request):
    data = json.loads(request.body)
    current_password = data.get('current_password')

    is_valid = request.user.check_password(current_password)
    return JsonResponse({'valid': is_valid})

    #    if member_pw(password1, user.password):
    #         password2 = request.POST.get('password2')
    #         password3 = request.POST.get('password3')
    #         if password2 == password3:
    #             user.set_password(password2)
    #             user.save()
    #             auth.login(request, user)
    #             return redirect("main:index")
    #         else:
    #             messages.error(request,'비밀번호가 일치하지않습니다.')
    #     else:
    #         messages.error(request, '비밀번호가 올바르지 않습니다.')
    #         return redirect("member:member_page.html")
    # else:
    #     return render(request, "member:member_page.html")

    # if request.method == "POST":
    #     form = PasswordChangeForm(request.user, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user)
    #         messages.success(request, '새로운 비밀번호로 변경되었습니다.')
    #         return redirect("main:index")
    #     else:
    #         messages.error(request, '비밀번호 변경이 되지않았습니다.')
    # else:
    #     form = PasswordChangeForm(request.user)
    # return render(request, 'member/member_pw.html', {'form': form})


# 회원탈퇴
def member_delete(request):
    # GET 요청 처리
    member = request.user.member
    return render(request, 'member/member_delete.html', {'member': member})

@login_required
def member_delete_detail(request):
    if request.method == 'POST':
        try:
            # 현재 로그인한 사용자의 Member 객체 가져오기
            member = request.user.member  # request.user가 Member 모델과 올바르게 연결되어 있어야 함.
            member_id = member.member_id  # Member 객체에서 member_id 가져오기

            # SQL 쿼리를 사용하여 member_member와 auth_user 테이블에서 삭제
            with connection.cursor() as cursor:
                # member_member 테이블에서 회원 삭제
                sql_member = "DELETE FROM member_member WHERE member_id = %s"
                cursor.execute(sql_member, [member_id])
                deleted_from_member = cursor.rowcount

                # auth_user 테이블에서 사용자 계정 삭제
                sql_user = "DELETE FROM auth_user WHERE username = %s"
                cursor.execute(sql_user, [member_id])
                deleted_from_user = cursor.rowcount

            # 로그아웃 처리
            logout(request)

            # 탈퇴 완료 후 홈으로 이동
            return redirect('main:index')

        except AttributeError:
            # 회원 정보를 찾을 수 없을 경우
            return render(request, 'member/member_delete_detail.html', {'error': '회원 정보를 찾을 수 없습니다.'})
        except Exception as e:
            # 예외 처리
            error_details = traceback.format_exc()
            return render(request, 'member/member_delete_detail.html', {'error': f'삭제 실패: {str(e)}', 'details': error_details})

    return render(request, 'member/member_delete_detail.html')