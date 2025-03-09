from django.contrib.auth.decorators import login_required
from member.models import EventPost
from django.shortcuts import render, redirect, get_object_or_404
from .utils import upload_content_to_s3
from django.core.checks import messages


def event_main(request):
    member = request.user.member
    events = EventPost.objects.all()

    return render(request, 'event/event_main.html', {"member": member, "events": events})

# 메인홈 - 이벤트상세페이지
def event_detail(request, event_id):
    event = get_object_or_404(EventPost, pk=event_id)  # 해당 event_id의 제품을 가져옴
    return render(request, 'event/event_detail.html', {'event': event})

    # member = request.user.member
    # events = EventPost.objects.all()
    #
    # # POST 요청에 의한 이벤트 추가 또는 수정 로직이 필요하다면 이 부분을 추가하세요.
    # if request.method == 'POST':
    #     event_detail = request.FILES.get('event_detail')  # 파일 업로드
    #
    #     # S3에 업로드된 이미지의 URL 처리
    #     if event_detail:
    #         event_detail_url = upload_content_to_s3(event_detail)  # 파일을 S3에 업로드하고 URL 반환
    #     else:
    #         event_detail_url = None
    #
    #     # 이벤트 등록 (추가/수정 로직)
    #     try:
    #         event = EventPost.objects.create(
    #             event_detail=event_detail_url,  # S3 URL 저장
    #         )
    #         event.save()
    #
    #         messages.success(request, "이벤트가 성공적으로 저장되었습니다.")
    #         return redirect('store:store_event')  # 이벤트 목록 페이지로 리다이렉트
    #     except Exception as e:
    #         messages.error(request, f"이벤트 저장 중 오류 발생: {e}")
    # return render(request, 'event/event_detail.html', {"member": member, "events": events})


# # 메인홈 - 이벤트
# def event_main(request):
#     member = request.user.member
#     events = EventPost.objects.all()
#
#     content = None  # 기본값 설정 (초기화)
#
#     if request.method == 'POST':
#         title = request.POST.get('title')  # 폼 데이터에서 이벤트명
#         show = 'show' in request.POST  # 체크박스 값
#         finish = 'finish' in request.POST  # 체크박스 값
#         store = request.POST.get('store')  # 숨겨진 store 값
#         content = request.FILES.get('content')  # 파일 업로드
#
#
#     return render(request, '../templates/event/event_main.html', {"member": member, "events": events})


# # 메인홈 - 이벤트
# def event_main(request):
#     member = request.user.member
#     events = EventPost.objects.all()
#
#
#     if request.method == 'POST':
#         title = request.POST.get('title')  # 폼 데이터에서 이벤트명
#         show = 'show' in request.POST  # 체크박스 값
#         finish = 'finish' in request.POST  # 체크박스 값
#         store = request.POST.get('store')  # 숨겨진 store 값
#         content = request.FILES.get('content')  # 파일 업로드
#
#     # S3에 프로필 이미지 업로드 후 URL 저장
#     content= upload_content_to_s3(content) if content else None
#
#     return render(request, '../templates/event/event_main.html',{"member": member, "events": events})


