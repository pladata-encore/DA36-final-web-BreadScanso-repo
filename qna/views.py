from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from member.models import QnA


def qna_main(request):
    qnas = QnA.objects.all().order_by('-created_at')

    # 페이지당 항목 수 (고정)
    qnas_per_page = 10

    # 페이지네이션 처리
    paginator = Paginator(qnas, qnas_per_page)

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
        'qnas': qnas,
        'page_obj': page_obj,
        'page_range': page_range,
        'total_qnas': qnas.count(),  # 총 공지사항 수
    }

    return render(request, '../templates/qna/qna_main.html', context)  # 템플릿 파일 경로 지정
