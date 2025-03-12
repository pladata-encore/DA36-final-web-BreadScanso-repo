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
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import secrets
from django.shortcuts import render, redirect
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from kiosk.models import PaymentInfo


from django.http import JsonResponse
from django.contrib.auth.models import User
from member.models import Member
import re



# member 메인
def member_main(request):
    return render(request, 'member/member_main.html')  # 템플릿 파일 경로 지정

# # 회원 마이페이지
# def member_page(request):
#     if not request.user.is_authenticated:
#         messages.error(request, "로그인이 필요합니다.")
#         return redirect("main:login")
#     try:
#         member = Member.objects.get(user=request.user)
#         return render(request, "member/member_page.html", {"member": member})
#     except Member.DoesNotExist:
#         messages.error(request, "회원 정보가 존재하지 않습니다.")
#         return redirect("main:index")
# 회원 마이페이지
def member_page(request):
    if not request.user.is_authenticated:
        messages.error(request, "로그인이 필요합니다.")
        return redirect("main:login")

    try:
        # 기존 코드 유지
        member = Member.objects.get(user=request.user)
        return render(request, "member/member_page.html", {"member": member})

    except Member.DoesNotExist:
        # 소셜 로그인된 사용자의 Member 자동 생성
        member = Member.objects.create(
            user=request.user,
            member_id=request.user.username,
            name=request.user.first_name or request.user.username,
            email=request.user.email,
            phone_num='',
            member_type='normal'
        )

        messages.success(request, "회원 정보가 자동으로 생성되었습니다.")
        return render(request, "member/member_page.html", {"member": member})


@login_required
@require_http_methods(["GET", "POST"])
def member_edit(request):
    if request.method == "POST":
        try:
            member = request.user.member
            user = request.user  # auth_user 테이블의 user 객체

            current_member_id = member.member_id  # 기존 아이디
            new_user_id = request.POST.get('user_id')  # 새로 입력한 아이디
            new_user_email = request.POST.get('email')

            # 다른 필드 데이터 먼저 저장
            name = request.POST.get('name')
            phone_num = request.POST.get('phone_num')
            email = request.POST.get('email')
            age_group = request.POST.get('age_group')
            sex = request.POST.get('sex')

            # ID 변경이 있는 경우
            if current_member_id != new_user_id:
                # 중복 체크
                if Member.objects.filter(member_id=new_user_id).exclude(member_id=current_member_id).exists():
                    return JsonResponse({'success': False, 'error': '이미 사용 중인 아이디입니다.'}, status=400)

                # 기존 Member 객체를 백업
                member_data = {
                    'name': name,
                    'phone_num': phone_num,
                    'email': email,
                    'age_group': age_group,
                    'sex': sex,
                    'total_spent': member.total_spent,
                    'points': member.points,
                    'visit_count': member.visit_count,
                    'last_visited': member.last_visited,
                    'profile_image': member.profile_image,
                    'store': member.store,
                    'store_num': member.store_num,
                    'earning_rate': member.earning_rate,
                    'store_address': member.store_address,
                    'store_time': member.store_time,
                    'store_notes': member.store_notes,
                    'member_type': member.member_type,
                    'member_password': member.member_password
                }

                # 기존 Member 삭제
                member.delete()

                # User 모델 업데이트
                user.username = new_user_id
                user.email = new_user_email
                user.save()

                # 새 Member 생성
                new_member = Member.objects.create(
                    user=user,
                    member_id=new_user_id,
                    **member_data
                )

                # 프로필 이미지 업데이트
                if 'profile_image' in request.FILES and request.FILES['profile_image']:
                    try:
                        profile_url = upload_profile_image_to_s3(request.FILES['profile_image'])
                        new_member.profile_image = profile_url
                        new_member.save()
                    except Exception as e:
                        return JsonResponse({'success': False, 'error': f"프로필 이미지 업로드 중 오류: {str(e)}"}, status=400)

            else:
                # ID 변경이 없는 경우는 일반 업데이트
                member.name = name
                member.phone_num = phone_num
                member.email = email
                member.age_group = age_group
                member.sex = sex

                # User 모델의 이메일도 업데이트 (추가된 부분)
                user.email = email
                user.save()

                # 프로필 이미지 업데이트
                if 'profile_image' in request.FILES and request.FILES['profile_image']:
                    try:
                        profile_url = upload_profile_image_to_s3(request.FILES['profile_image'])
                        member.profile_image = profile_url
                    except Exception as e:
                        return JsonResponse({'success': False, 'error': f"프로필 이미지 업로드 중 오류: {str(e)}"}, status=400)

                member.save()

            return JsonResponse({
                'success': True,
                'message': '회원정보가 성공적으로 수정되었습니다.'
            })

        except Exception as e:
            print(f"Error in member_edit: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    # GET 요청 처리
    member = request.user.member

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
    user_id = request.GET.get('user_id', '').strip()

    # 아이디 유효성 검사 (영문 소문자 + 숫자, 4~12자리)
    if not re.match(r'^[a-z0-9]{4,12}$', user_id):
        return JsonResponse({"valid": False, "message": "아이디는 영문 소문자와 숫자로 4~12자리여야 합니다."})

    # 현재 로그인한 사용자의 아이디인 경우
    if request.user.is_authenticated:
        if request.user.username == user_id or request.user.member.member_id == user_id:
            return JsonResponse({"valid": True, "message": "현재 사용 중인 아이디입니다."})

    # 기존 회원 아이디와 비교
    exists = User.objects.filter(username=user_id).exists() or Member.objects.filter(member_id=user_id).exists()

    if exists:
        return JsonResponse({"valid": False, "message": "이미 사용 중인 아이디입니다."})

    return JsonResponse({"valid": True, "message": "사용 가능한 아이디입니다."})

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

# @login_required
# def member_delete_detail(request):
#     if request.method == 'POST':
#         try:
#             # 현재 로그인한 사용자의 Member 객체 가져오기
#             member = request.user.member  # request.user가 Member 모델과 올바르게 연결되어 있어야 함.
#             member_id = member.member_id  # Member 객체에서 member_id 가져오기
#
#             # SQL 쿼리를 사용하여 member_member와 auth_user 테이블에서 삭제
#             with connection.cursor() as cursor:
#                 # # 소셜 계정 먼저 삭제
#                 # sql_social = "DELETE FROM socialaccount_socialaccount WHERE user_id = (SELECT id FROM auth_user WHERE username = %s)"
#                 # cursor.execute(sql_social, [member_id])
#                 # deleted_from_social = cursor.rowcount
#
#                 # member_member 테이블에서 회원 삭제
#                 sql_member = "DELETE FROM member_member WHERE member_id = %s"
#                 cursor.execute(sql_member, [member_id])
#                 deleted_from_member = cursor.rowcount
#
#                 # auth_user 테이블에서 사용자 계정 삭제
#                 sql_user = "DELETE FROM auth_user WHERE username = %s"
#                 cursor.execute(sql_user, [member_id])
#                 deleted_from_user = cursor.rowcount
#
#             # 로그아웃 처리
#             logout(request)
#
#             # 탈퇴 완료 후 홈으로 이동
#             return redirect('main:index')
#
#         except AttributeError:
#             # 회원 정보를 찾을 수 없을 경우
#             return render(request, 'member/member_delete_detail.html', {'error': '회원 정보를 찾을 수 없습니다.'})
#         except Exception as e:
#             # 예외 처리
#             error_details = traceback.format_exc()
#             return render(request, 'member/member_delete_detail.html', {'error': f'삭제 실패: {str(e)}', 'details': error_details})
#
#     return render(request, 'member/member_delete_detail.html')

@login_required
def member_delete_detail(request):
    if request.method == 'POST':
        try:
            # 현재 로그인한 사용자 정보 가져오기
            user = request.user

            try:
                # 소셜 계정 삭제 (있는 경우에만)
                SocialAccount = apps.get_model('socialaccount', 'SocialAccount')
                SocialAccount.objects.filter(user=user).delete()
            except ImportError:
                # socialaccount 앱이 없는 경우 무시
                pass

            # member_member 테이블에서 삭제
            Member.objects.filter(user=user).delete()

            # auth_user 테이블에서 사용자 삭제
            user.delete()

            # 로그아웃 처리
            logout(request)

            # 탈퇴 완료 후 홈으로 이동
            messages.success(request, '회원 탈퇴가 완료되었습니다.')
            return redirect('main:index')

        except Exception as e:
            # 예외 처리
            messages.error(request, f'탈퇴 중 오류가 발생했습니다: {str(e)}')
            return redirect('main:index')

    # GET 요청의 경우
    return render(request, 'member/member_delete_detail.html')

@login_required
def mypoint(request):
    member = request.user.member # 로그인한 회원 정보 가져오기

    # 현재 로그인한 회원(member_id) 기준으로 결제 내역 조회
    member_payments = PaymentInfo.objects.filter(member=member).order_by("-pay_at")

    # 페이지네이션 (10개씩 표시)
    paginator = Paginator(member_payments, 10)  # 한 페이지당 10개씩
    page_number = request.GET.get("page")  # 현재 페이지 번호 가져오기

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)  # 유효하지 않은 페이지 번호라면 첫 페이지로 이동

    return render(request, "member/member_mypoint.html", {"member": member, "page_obj": page_obj})