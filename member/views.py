from django.shortcuts import render

def member_main(request):
    return render(request, '../templates/member/member_main.html')  # 템플릿 파일 경로 지정
