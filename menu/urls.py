from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.menu_main, name='menu_main'),  # 소비자 메뉴 메인 페이지
    path('product_detail/<int:item_id>', views.product_detail, name='menu_product_detail'),  # 각 메뉴 상세 페이지
    path('store/', views.menu_store, name='menu_store'),  # 점주 메뉴관리 페이지
    path('store/menu_add', views.menu_add, name='menu_add'),  # 점주 메뉴 신규등록 페이지
    path('store/menu_save', views.menu_save, name="menu_save"), # 점주 메뉴 신규 등록 api
    path('store/menu_delete/', views.menu_delete, name="menu_delete"), # 점주 메뉴 삭제 api
    path('store/menu_info/<int:item_id>/', views.menu_store_menu_info, name='menu_store_menu_info'),  # 제품별 관리 상세 페이지
    path('store/menu_edit/<int:item_id>/', views.menu_store_menu_edit, name='menu_store_menu_edit'),  # 제품별 수정 페이지
    path('store/new_menu_guide/<int:item_id>/', views.menu_store_new_menu_guide, name='menu_store_new_menu_guide'),  # 신규 메뉴 학습 가이드 페이지
    path('store/new_menu_learn/<int:item_id>/', views.menu_store_new_menu_learn, name='menu_store_new_menu_learn'),  # 신규 메뉴 학습 페이지

]
