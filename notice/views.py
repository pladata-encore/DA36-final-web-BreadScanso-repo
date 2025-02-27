from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Notice
from django.core.paginator import Paginator, EmptyPage

def notice_main(request):
    notices = Notice.objects.all().order_by('-created_at')

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

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'notice/notice_detail.html', {'notice': notice})

def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    return redirect('notice_main')

class NoticeForm(forms.ModelForm):  # forms.py 대신 views.py에 직접 선언
    class Meta:
        model = Notice
        fields = ['title', 'content']

def notice_create(request):
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notice_main')
    else:
        form = NoticeForm()
    return render(request, 'notice/notice_form.html', {'form': form})
