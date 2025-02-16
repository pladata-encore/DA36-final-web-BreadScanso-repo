from django.shortcuts import render

def event_main(request):
    return render(request, '../templates/event/event_main.html')  # 템플릿 파일 경로 지정
