from django.shortcuts import render

def qna_main(request):
    return render(request, '../templates/qna/qna_main.html')  # 템플릿 파일 경로 지정
