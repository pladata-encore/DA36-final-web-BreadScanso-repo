from django.shortcuts import render

def brand_main(request):
    member = None  # 기본값을 None으로 설정

    if request.user.is_authenticated:  # 로그인한 경우에만 가져오기
        member = request.user.member

    # 하나의 딕셔너리로 합쳐서 전달
    context = {
        'member': member
    }
    return render(request, '../templates/brand/brand_main.html', context)  # 템플릿 파일 경로 지정
