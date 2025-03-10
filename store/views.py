from abc import ABC, abstractmethod
from enum import member

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.db.models import Q
from member.models import QnA, QnAReply, QuestionForm
from member.models import Member, EventPost
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import traceback
from django.views.decorators.http import require_POST
from event.utils import upload_content_to_s3




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
    member = None  # 기본값을 None으로 설정

    if request.user.is_authenticated:  # 로그인한 경우에만 가져오기
        member = request.user.member

    context = {
        'stores': json.dumps(stores, ensure_ascii=False),  # JSON 변환 후 전달
        # 'store_name': [store['store_name'] for store in stores],
        'store_name': first_store_name,
        'member': member
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



# 시스템설정 - 이벤트
def store_event(request):
    member = request.user.member

    # 정렬 조건
    sort_by = request.GET.get("sort_by", "event_id")
    sort_order = request.GET.get("sort_order", "asc")

    # 정렬 방식 지정
    if sort_order == "desc":
        sort_by = f"-{sort_by}"

    # 필터링 (진행중 / 종료)
    show_filter = request.GET.get("show", '')
    finish_filter = request.GET.get("finish", '')

    events = EventPost.objects.all()

    if show_filter:
        events = events.filter(show=show_filter == "1")
    if finish_filter:
        events = events.filter(finish=finish_filter == "1")

    # 페이지네이션 처리 (10개씩)
    paginator = Paginator(events, 10)
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
        page_obj = paginator.get_page(paginator.num_pages)

    # 정렬 적용
    events = events.order_by(sort_by)

    # GET 요청 처리 (member 데이터 가져오기)
    context = {
        'member': member,
        'events': page_obj,
        'page_obj': page_obj,  # 페이지네이션된 events 객체를 전달
        'show_filter': show_filter,
        'finish_filter': finish_filter,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }

    return render(request, 'store/store_event.html', context)

@require_POST
def delete_store_event(request):
    try:
        data = json.loads(request.body)
        event_ids = data.get("event_ids", [])

        if not event_ids:
            return JsonResponse({"success": False, "message": "삭제할 이벤트를 선택해주세요."})

        with connection.cursor() as cursor:
            placeholders = ','.join(['%s'] * len(event_ids))
            sql = f"DELETE FROM member_eventpost WHERE event_id IN ({placeholders})"
            cursor.execute(sql, event_ids)
            connection.commit()

        return JsonResponse({"success": True, "message": f"{cursor.rowcount}개의 이벤트가 삭제되었습니다."})

    except Exception as e:
        return JsonResponse({"success": False, "message": f"삭제 실패: {str(e)}"})


def store_event_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')  # 폼 데이터에서 이벤트명
        show = 'show' in request.POST  # 체크박스 값
        finish = 'finish' in request.POST  # 체크박스 값
        store = request.POST.get('store')  # 숨겨진 store 값
        content = request.FILES.get('content')  # 파일 업로드(기본형)
        event_detail = request.FILES.get('event_detail')  # 파일 업로드(상세페이지용)

        # S3에 프로필 이미지 업로드 후 URL 저장
        if content:
            content_url = upload_content_to_s3(content)  # 파일을 S3에 업로드하고 URL 반환
        if event_detail:
            event_detail_url = upload_content_to_s3(event_detail)
        else:
            content_url = None
            event_detail_url = None

        # 데이터 검증 (기본적으로 제목만 필수로 받음)
        if not title:
            messages.error(request, "이벤트명은 필수입니다.")
            return redirect('store:store_event_add')

        # 모델 객체 생성 후 저장
        try:
            event = EventPost.objects.create(
                title=title,
                store=store,
                content=content_url,  # S3 URL 저장
                event_detail=event_detail_url,  # S3 URL 저장
                show=show,
                finish=finish
            )
            event.save()
            messages.success(request, "이벤트가 성공적으로 저장되었습니다.")
            return redirect('store:store_event')  # 이벤트 목록 페이지로 리다이렉트
        except Exception as e:
            messages.error(request, f"이벤트 저장 중 오류 발생: {e}")
            return redirect('store:store_event_add')

    return render(request, 'store/store_event_add.html')

# # 시스템설정 - 이벤트 신규등록
# def store_event_add(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')  # 폼 데이터에서 이벤트명
#         show = 'show' in request.POST  # 체크박스 값
#         finish = 'finish' in request.POST  # 체크박스 값
#         store = request.POST.get('store')  # 숨겨진 store 값
#         content = request.FILES.get('content')  # 파일 업로드
#
#         # S3에 프로필 이미지 업로드 후 URL 저장
#         content = upload_content_to_s3(content) if content else None
#
#         # 데이터 검증 (기본적으로 제목만 필수로 받음)
#         if not title:
#             messages.error(request, "이벤트명은 필수입니다.")
#             return redirect('store:store_event_add')
#
#         # 모델 객체 생성 후 저장
#         try:
#             events = EventPost.objects.create(
#                 title=title,
#                 store=store,
#                 content=content,
#                 show=show,
#                 finish=finish
#             )
#             events.save()
#             messages.success(request, "이벤트가 성공적으로 저장되었습니다.")
#             return redirect('store:store_event')  # 이벤트 목록 페이지로 리다이렉트
#         except Exception as e:
#             messages.error(request, f"이벤트 저장 중 오류 발생: {e}")
#             return redirect('store:store_event_add')
#     return render(request, 'store/store_event_add.html')

# # 시스템설정 - 이벤트 신규등록 저장
# @require_http_methods(["POST"])
# def evnet_save(request):
#     if request.method == "POST":
#         # show, finish 체크박스 여부
#         show = request.POST.get("show") == "on"
#         finish = request.POST.get("finish") == "on"
#
#         # 기본 제품 정보
#         title = request.POST.get("title")
#         store = request.user.member.store # 로그인한 사용자의 member.store 정보 가져옴
#
#
#         # S3
#         event_image_url = None
#         if 'event_image' in request.FILES:
#             try:
#                 event_image_url = upload_event_image_to_s3(request.FILES['event_image'])
#             except Exception as e:
#                 return render(request, 'menu/menu_add.html', {
#                     'error': f'이미지 업로드 중 오류가 발생했습니다: {str(e)}'
#                 })
#
#         # 제품 정보 입력 검수
#         if not all([title, store]):
#             return render(request, 'menu/menu_add.html', {
#                 'error': '기본 정보의 모든 필드를 입력해주세요.'
#             })
#
#         try:
#             event = EventPost(
#                 event_id=member.event_id,
#                 show=show,
#                 finish=finish,
#                 title=title,
#                 content=content_url
#             )
#             event.save()
#
#
#             return redirect('menu_store_menu_info', event_id=member.event_id)
#
#         except Exception as e:
#             return render(request, 'menu/menu_add.html', {
#                 'error': f'저장 중 오류가 발생했습니다: {str(e)}'
#             })
#     else:
#         return render(request, 'store/store_event_add.html')
#
# # 이벤트 삭제
# @require_http_methods(["POST"])
# def event_delete(request):
#     try:
#         # 요청 데이터 파싱
#         data = json.loads(request.body)
#         event_ids = data.get("event_ids", [])
#
#         if not event_ids:
#             return JsonResponse({
#                 "success": False,
#                 "message": "삭제할 항목이 없습니다."
#             })
#
#         deleted_count, _ = Event.objects.filter(event_id__in=event_id).delete()
#
#         # 삭제 결과 반환
#         if deleted_count > 0:
#             return JsonResponse({
#                 "success": True,
#             })
#         else:
#             return JsonResponse({
#                 "success": False,
#             })
#
#     except json.JSONDecodeError:
#         return JsonResponse({
#             "success": False,
#             "message": "잘못된 요청 데이터입니다."
#         })
#     except Exception as e:
#         return JsonResponse({
#             "success": False,
#             "message": "서버 오류가 발생했습니다."
#         })


def store_account(request):
    member = request.user.member
    return render(request, 'store/store_account.html', {"member": member})  # 매장정보


