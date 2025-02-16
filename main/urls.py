from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views

# namespace 지정
app_name = 'main'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="main/login.html"), name="login"),  # 로그인 경로
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),  # 로그아웃 경로
    path("signup/", views.signup, name="signup"),  # 회원가입 경로
    path("login_find/", views.login_find, name="login_find"),  # ID/PW 찾기 경로

]