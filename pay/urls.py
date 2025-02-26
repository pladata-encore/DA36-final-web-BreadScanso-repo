from django.urls import path
from . import views  # views.py에서 함수 가져오기

# namespace 지정
app_name = 'pay'

urlpatterns = [
    path('', views.pay_main, name='pay_main'),  # /pay/

    path('details/<int:payment_id>/', views.pay_details, name='pay_details'),

    path('cancel/', views.pay_cancel, name='pay_cancel'),

    path('member/', views.pay_member, name='pay_member'),

    path('member/cancel/', views.pay_member_cancel, name='pay_member_cancel'),

    path('member/details/', views.pay_member_details, name='pay_member_details'),
    # path('member/details/<int:payment_id>/', views.pay_member_details, name='pay_member_details'),

]