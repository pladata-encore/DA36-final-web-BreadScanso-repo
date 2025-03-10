from django.contrib.auth.decorators import login_required
from member.models import EventPost
from django.shortcuts import render, redirect, get_object_or_404
from .utils import upload_content_to_s3
from django.core.checks import messages


def event_main(request):
    member = None  # 기본값을 None으로 설정

    if request.user.is_authenticated:  # 로그인한 경우에만 가져오기
        member = request.user.member

    events = EventPost.objects.all()

    context = {
        'member': member,
        'events': events,
    }

    return render(request, 'event/event_main.html', context)

# 메인홈 - 이벤트상세페이지
def event_detail(request, event_id):
    event = get_object_or_404(EventPost, pk=event_id)  # 해당 event_id의 제품을 가져옴
    member = None  # 기본값을 None으로 설정

    if request.user.is_authenticated:  # 로그인한 경우에만 가져오기
        member = request.user.member
    context = {
        'member': member,
        'event': event,
    }
    return render(request, 'event/event_detail.html', context)


