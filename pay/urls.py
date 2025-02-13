from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.pay_main, name='pay_main'),  # /pay/

    path('details/', views.pay_details, name='pay_details'),
    # path('details/<int:payment_id>/', views.pay_details, name='pay_details'),
    path('cancel/', views.pay_cancel, name='pay_cancel'),
]