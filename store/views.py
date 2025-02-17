from django.shortcuts import render

def store_main(request):
    return render(request, 'store/store_main.html')  # /store/

def store_home_edit(request):
    return render(request, 'store/store_home_edit.html')  # 홈 화면 수정

def about_breadscanso_edit(request):
    return render(request, 'store/about_breadscanso_edit.html')  # 브랜드 소개

def store_map(request):
    return render(request, 'store/store_map.html')  # 매장 안내

def event_edit(request):
    return render(request, 'store/event_edit.html')  # 이벤트

def community_notice(request):
    return render(request, 'store/community_notice.html')  # 커뮤니티/공지사항

def community_qna(request):
    return render(request, 'store/community_qna.html')  # 커뮤니티/qna

def store_account(request):
    return render(request, 'store/store_account.html')  # 매장정보


