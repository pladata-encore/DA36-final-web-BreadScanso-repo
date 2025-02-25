from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.kiosk_main, name='kiosk_main'),  # /kiosk/ 메인 페이지
    path('products/', views.products, name='products'),  # 상품 안내 페이지
    path('member/', views.member, name='member'),  # 회원 확인 페이지
    path('phonenumber/', views.phonenumber, name='phonenumber'),  # 전화번호 입력 페이지
    path('usepoint/', views.usepoint, name='usepoint'),  # 포인트 사용 페이지
    path('payment_method/', views.payment_method, name='payment_method'),  # 결제 방식 페이지
    path('payment_completed/', views.payment_completed, name='payment_completed'),  # 결제 완료/영수증 페이지
    path('phonenumber/check-phone/', views.check_phone_number, name='check_phone_number'),
    path("update_points/", views.update_points, name="update_points"),
    path("complete_payment/", views.complete_payment, name="complete_payment"),
]




