from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from member.models import EventPost
from django.shortcuts import render, get_object_or_404

def event_main(request):
#     search_keyword = self.request.GET.get('q', '')  # 검색어 가져오기
#     event_list = EventPost.objects.order_by('-id')  # 최신순 정렬
#
#     if search_keyword:
#         if len(search_keyword) > 1:
#             search_event_list = event_list.filter(title__icontains=search_keyword)
#             return search_event_list  # 검색 결과 반환
#         else:
#             messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
#
#     return event_list  # 검색어가 없을 경우 전체 목록 반환
    return render(request, '../templates/event/event_main.html')  # 템플릿 파일 경로 지정
#
# def get_context_data(self, **kwargs):
#     search_keyword = self.request.GET.get('q', '')
#
#     if len(search_keyword) > 1 :
#         context['q'] = search_keyword
#
#     return context

def event_detail(request):
    return render(request, 'event/event_detail.html')