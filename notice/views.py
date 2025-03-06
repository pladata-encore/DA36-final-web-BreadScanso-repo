from lib2to3.fixes.fix_input import context
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Notice
from django.http import JsonResponse
from django.utils.html import strip_tags
from .forms import NoticeForm
from bs4 import BeautifulSoup
import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import uuid


# 소비자 화면 공지사항 페이지
def notice_main(request):
    # pinned=1을 먼저, 그 다음 notice_id로 오름차순 정렬
    notices = Notice.objects.all().order_by('-pinned', 'notice_id')

    # 페이지당 항목 수 (고정)
    notices_per_page = 10

    # 페이지네이션 처리
    paginator = Paginator(notices, notices_per_page)

    # 페이지 번호 가져오기
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    # 페이지 객체 가져오기
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 페이지 범위 계산
    max_pages = 5
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + max_pages - 1)

    if end_page - start_page + 1 < max_pages and start_page > 1:
        start_page = max(1, end_page - max_pages + 1)

    page_range = range(start_page, end_page + 1)

    context = {
        'notices': notices,
        'page_obj': page_obj,
        'page_range': page_range,
        'total_notices': notices.count(),  # 총 공지사항 수
    }

    return render(request, 'notice/notice_main.html', context)

# ---------------------------------------------------------------------------- #
# 소비자 화면 공지사항 상세 페이지
def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, notice_id=notice_id)
    return render(request, 'notice/notice_detail.html', {'notice': notice})

# ---------------------------------------------------------------------------- #
# 점주용 공지사항 페이지 (로그인 필요)
@login_required
def notice_store(request):
    member = request.user.member
    notices = Notice.objects.all().order_by('-pinned', 'notice_id')

    # member.store 값에 따라 해당 store의 공지사항만 필터링
    if member.store:
        notices = notices.filter(store=member.store)
    else:
        # member.store가 없는 경우 notice_store에서는 접근 불가, notice_main으로 리다이렉트
        return redirect('notice_main')

    # 검색 기능 추가
    search_query = request.GET.get('search', '')
    if search_query:
        notices = notices.filter(title__icontains=search_query)

    # 페이지당 항목 수 (고정)
    notices_per_page = 10

    # 페이지네이션 처리
    paginator = Paginator(notices, notices_per_page)

    # 페이지 번호 가져오기
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    # 페이지 객체 가져오기
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 페이지 범위 계산
    max_pages = 5
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + max_pages - 1)

    if end_page - start_page + 1 < max_pages and start_page > 1:
        start_page = max(1, end_page - max_pages + 1)

    page_range = range(start_page, end_page + 1)

    context = {
        'notices': notices,
        'page_obj': page_obj,
        'page_range': page_range,
        'total_notices': notices.count(),  # 총 공지사항 수
        'member': member,
        'search_query': search_query,  # 검색어 템플릿에 전달
    }
    return render(request, 'notice/notice_store.html', context)

# ---------------------------------------------------------------------------- #
# 관리자 페이지 공지사항 상세 페이지
@login_required
def notice_info(request, notice_id):
    member = request.user.member
    notice = get_object_or_404(Notice, notice_id=notice_id)

    context = {
        'notice': notice,
        'member': member
    }
    return render(request, 'notice/notice_info.html', context)

# ---------------------------------------------------------------------------- #
# 점주용 공지사항 글쓰기 페이지
@login_required
def notice_write(request):
    member = request.user.member
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            if not member:
                return JsonResponse({"success": False, "message": "Member 객체가 존재하지 않습니다."})

            content_html = form.cleaned_data['content']
            notice.content = content_html
            notice.member = member
            notice.store = member.store
            notice.save()
            return redirect('notice_info', notice_id=notice.notice_id)
    else:
        form = NoticeForm()

    context = {
        'form': form,
        'member': member
    }
    return render(request, 'notice/notice_write.html', context)

# ---------------------------------------------------------------------------- #
# 점주용 공지사항 글쓰기 삭제 api
def notice_delete(request):
    if request.method == "POST":
        try:
            # JSON 데이터는 request.body에서 가져옴
            raw_data = request.body.decode('utf-8')
            if not raw_data:
                return JsonResponse({'success': False, 'message': '요청 본문이 비어 있습니다.'})

            # JSON 파싱
            try:
                data = json.loads(raw_data)
                notice_ids = data.get('notice_ids')
                if not notice_ids:
                    return JsonResponse({'success': False, 'message': 'notice_ids가 제공되지 않았습니다.'})
                if not isinstance(notice_ids, list):
                    return JsonResponse({'success': False, 'message': 'notice_ids는 리스트 형식이어야 합니다.'})
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': '유효하지 않은 JSON 형식입니다.'})

            # 삭제 로직
            deleted_count, _ = Notice.objects.filter(notice_id__in=notice_ids).delete()
            if deleted_count > 0:
                return JsonResponse({'success': True, 'message': f'{deleted_count}개의 공지사항이 삭제되었습니다.'})
            else:
                return JsonResponse({'success': False, 'message': '삭제할 공지사항이 존재하지 않습니다.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'서버 오류: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'POST 요청만 허용됩니다.'})

# ---------------------------------------------------------------------------- #
# 점주용 공지사항 글쓰기 저장 api
@login_required
def notice_save(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            notice_id = data.get("notice_id")
            pinned = data.get("pinned", False)
            title = data.get("title")
            content = data.get("content")
            store = data.get("store")
            notice_image = data.get("notice_image")  # Base64 데이터

            if not title or not content:
                return JsonResponse({"success": False, "message": "제목과 내용을 입력해주세요."})

            member = request.user.member
            if not member:
                return JsonResponse({"success": False, "message": "Member 객체가 존재하지 않습니다."})

            now = timezone.now()
            if notice_id:  # 수정
                notice = get_object_or_404(Notice, notice_id=notice_id)
                notice.pinned = pinned
                notice.title = title
                notice.content = content
                notice.store = store if store in ["A", "B"] else member.store
                notice.updated_at = now
                if notice_image:
                    notice.notice_image = base64.b64decode(notice_image.split(',')[1])
                notice.save()
            else:  # 신규 생성
                notice = Notice.objects.create(
                    pinned=pinned,
                    title=title,
                    content=content,
                    store=store if store in ["A", "B"] else member.store,
                    member=member,
                    created_at=now,
                    updated_at=now,
                    view_count=0,
                    notice_image=base64.b64decode(notice_image.split(',')[1]) if notice_image else None
                )

            return JsonResponse({"success": True, "notice_id": notice.notice_id})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "POST 요청만 허용됩니다."})

# ---------------------------------------------------------------------------- #
# 공지사항 내용 수정
@login_required
def notice_edit(request, notice_id):
    member = request.user.member
    notice = get_object_or_404(Notice, notice_id=notice_id)

    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            content_html = form.cleaned_data['content']
            notice.content = content_html
            notice.member = member
            notice.store = member.store
            notice.updated_at = timezone.now()
            notice.save()
            return redirect('notice_info', notice_id=notice.notice_id)
    else:
        form = NoticeForm(instance=notice)

    context = {
        'form': form,
        'notice_id': notice_id,
        'member': member,
    }
    return render(request, 'notice/notice_edit.html', context)

# ---------------------------------------------------------------------------- #
# # summernote 에서 s3 로 이미지 업로드 api
# @csrf_exempt
# def upload_image_to_s3(request):
#     if request.method == "POST" and request.FILES.get("file"):
#         file = request.FILES["file"]
#         file_name = f"images/{uuid.uuid4()}_{file.name}"
#
#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#             region_name=settings.AWS_S3_REGION_NAME
#         )
#
#         s3_client.upload_fileobj(
#             file,
#             settings.AWS_STORAGE_BUCKET_NAME,
#             file_name,
#             ExtraArgs={'ACL': 'public-read'}
#         )
#
#         file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
#         return JsonResponse({"location": file_url})
#     return JsonResponse({"error": "Invalid request"}, status=400)