from django.shortcuts import render

def notice_main(request):
    return render(request, '../templates/notice/notice_main.html')  # 템플릿 파일 경로 지정
