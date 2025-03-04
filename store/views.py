from abc import ABC, abstractmethod
from enum import member

from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.db.models import Q
from member.models import QnA, QnAReply, QuestionForm
from member.models import Member
import json
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# def store_main(request):    // 밑으로 옮길게요 ~~
#     return render(request, 'store/store_main_map.html' )

# 매장페이지 - 회원관리
def member_store(request):
    # 검색 기능 처리
    search_query = request.POST.get('search_input', '')

    if search_query:
        # 검색어가 있을 경우 회원명 기준으로 필터링
        members = Member.objects.filter(name__icontains=search_query)
    else:
        # 검색어가 없을 경우 모든 회원 정보 가져오기
        members = Member.objects.all()

    # 페이지네이션 처리 (10개씩)
    paginator = Paginator(members, 10)
    # 페이지 번호 가져오기, 유효하지 않으면 1 페이지로 설정
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        # 페이지 번호가 범위를 벗어난 경우 마지막 페이지로 설정
        page_obj = paginator.get_page(paginator.num_pages)

    # GET 요청 처리 (member 데이터 가져오기)
    member = request.user.member

    # 하나의 딕셔너리로 합쳐서 전달
    context = {
        'page_obj': page_obj,
        'member': member
    }

    return render(request, 'member/member_store.html', context)


# 회원 정보 업데이트
def update_member_store(request):
    if request.method == 'POST':
        try:
            # POST로 넘어오는 데이터
            data = json.loads(request.body)
            member_id = data.get('member_id')  # 회원 ID
            new_name = data.get('new_name')  # 새로운 회원명
            new_phone_num = data.get('new_phone_num')  # 새로운 휴대폰 번호
            new_email = data.get('new_email')  # 새로운 이메일

            # 유효성 검사
            if not member_id or not new_name or not new_phone_num or not new_email:
                return JsonResponse({'success': False, 'error': 'Invalid data provided'})

            # 회원 존재 여부 확인
            try:
                member = Member.objects.get(member_id=member_id)
            except Member.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Member not found'})

            # 회원 정보 업데이트
            member.name = new_name
            member.phone_num = new_phone_num
            member.email = new_email
            member.save()

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error updating member: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})

def member_store_edit(request):
    return render(request, 'store/member_store_edit.html')  # 회원 정보 수정

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import connection
import json
import traceback

@require_http_methods(["POST"])
def delete_member_store(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            member_ids = data.get("member_ids", [])

            if not member_ids:
                return JsonResponse({
                    "success": False,
                    "message": "삭제할 회원을 선택해주세요."
                })

            with connection.cursor() as cursor:
                # 먼저 member_member 테이블에서 삭제
                sql_member = "DELETE FROM member_member WHERE member_id IN (%s)" % ','.join(['%s'] * len(member_ids))
                cursor.execute(sql_member, member_ids)
                deleted_from_member = cursor.rowcount

                # auth_user 테이블에서도 삭제
                sql_user = "DELETE FROM auth_user WHERE username IN (%s)" % ','.join(['%s'] * len(member_ids))
                cursor.execute(sql_user, member_ids)
                deleted_from_user = cursor.rowcount

            return JsonResponse({
                "success": True,
                "message": f"{deleted_from_member}명의 회원 정보 및 {deleted_from_user}명의 사용자 계정이 삭제되었습니다."
            })

        except Exception as e:
            error_details = traceback.format_exc()
            return JsonResponse({
                "success": False,
                "message": f"삭제 실패: {str(e)}",
                "details": error_details
            })

    return JsonResponse({"success": False, "message": "잘못된 요청입니다."})


# @require_http_methods(["POST"])
# def delete_member_store(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)  # JSON 데이터 파싱
#             member_ids = data.get("member_ids", [])
#
#             if not member_ids:
#                 return JsonResponse({
#                     "success": False,
#                     "message": "삭제할 회원을 선택해주세요."
#                 })
#
#             # 직접 SQL 쿼리 실행하여 member_member 테이블에서만 삭제
#             from django.db import connection
#
#             with connection.cursor() as cursor:
#                 # 테이블 이름과 필드 이름을 정확하게 사용
#                 # 여러 회원을 삭제할 때는 IN 절 사용
#                 sql = "DELETE FROM member_member WHERE member_id IN (%s)" % ','.join(['%s'] * len(member_ids))
#                 cursor.execute(sql, member_ids)
#                 row_count = cursor.rowcount
#
#             return JsonResponse({"success": True, "message": f"{row_count}명의 회원이 삭제되었습니다."})
#         except Exception as e:
#             import traceback
#             error_details = traceback.format_exc()
#             return JsonResponse({
#                 "success": False,
#                 "message": f"삭제 실패: {str(e)}",
#                 "details": error_details
#             })
#
#     return JsonResponse({"success": False, "message": "잘못된 요청입니다."})
# # 회원 삭제
# @require_http_methods(["POST"])
# def delete_member_store(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)  # JSON 데이터 파싱
#             member_ids = data.get("member_ids", [])
#
#             if not member_ids:
#                 return JsonResponse({
#                     "success": False,
#                     "message": "삭제할 회원을 선택해주세요."
#                 })
#
#             deleted_count, _ = Member.objects.filter(member_id__in=member_ids).delete()
#
#             return JsonResponse({"success": True, "message": f"선택한 회원이 삭제되었습니다."})
#         except Exception as e:
#             return JsonResponse({"success": False, "message": f"삭제 실패: {str(e)}"})
#
#     return JsonResponse({"success": False, "message": "잘못된 요청입니다."})

def store_home_edit(request):
    # GET 요청 처리 (member 데이터 가져오기)
    member = request.user.member
    return render(request, 'store/store_home_edit.html', {"member": member})  # 홈 화면 수정

def about_breadscanso_edit(request):
    # GET 요청 처리 (member 데이터 가져오기)
    member = request.user.member
    return render(request, 'store/about_breadscanso_edit.html', {"member": member})  # 브랜드 소개


def store_main(request):
    members = Member.objects.filter(member_type='manager')

    stores = [
        {
            'store': member.store,
            'store_name': dict(member._meta.get_field('store').choices).get(member.store, ''),
            'store_address': member.store_address,
            'store_time': member.store_time,
            'store_num' : member.store_num,
            'store_notes': member.store_notes,  # HTML 포함
        }
        for member in members
    ]
    first_store_name = stores[0]['store_name'] if stores else ''
    context = {
        'stores': json.dumps(stores, ensure_ascii=False),  # JSON 변환 후 전달
        # 'store_name': [store['store_name'] for store in stores],
        'store_name': first_store_name,
    }
    return render(request, 'store/store_main_map.html', context)


def store_map(request):
    member = request.user.member
    store = member.store
    store_name = dict(member._meta.get_field('store').choices).get(store[0], '')
    store_address = member.store_address
    store_time = member.store_time
    store_num = member.store_num
    store_notes = member.store_notes

    context = {
        'member': member,
        'store': store,
        'store_name': store_name,
        'store_address': store_address,
        'store_time': store_time,
        'store_num': store_num,
        'store_notes': store_notes,
    }

    return render(request, 'store/store_map.html', context)  # 매장 안내

@csrf_exempt  # CSRF 검사를 비활성화
@login_required  # 로그인한 사용자만 접근 가능
def store_map_edit(request):
    # POST 요청 처리 (AJAX로 받은 데이터를 저장)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            store_address = data.get('store_address')
            store_time = data.get('store_time')
            store_num = data.get('store_num')
            store_notes = data.get('store_notes')

            member = request.user.member
            member.store_address = store_address
            member.store_time = store_time
            member.store_num = store_num
            member.store_notes = store_notes
            member.save()
            return JsonResponse({'status': 'success', 'message': '변경사항이 저장되었습니다.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # GET 요청 시 기존 매장의 정보 제공!
    member = request.user.member
    store_address = member.store_address
    store_time = member.store_time
    store_num = member.store_num
    store_notes = member.store_notes

    context = {
        'member': member,
        'store_address': store_address,
        'store_time': store_time,
        'store_num': store_num,
        'store_notes': store_notes,
    }
    return render(request, 'store/store_map_edit.html', context)

def store_event(request):
    member = request.user.member
    return render(request, 'store/store_event.html', {"member": member})  # 이벤트

def store_event_edit(request):
    member = request.user.member
    return render(request, 'store/store_event_edit.html', {"member": member})  # 이벤트 수정

def store_account(request):
    member = request.user.member
    return render(request, 'store/store_account.html', {"member": member})  # 매장정보

