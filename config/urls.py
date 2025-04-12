from django.urls import path
from user.views import KakaoLoginAPIView,LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('auth/kakao-login/', KakaoLoginAPIView.as_view(), name='kakao_login'),#카카오 access_token으로 로그인 (JWT 발급)
    path('auth/refresh/',TokenRefreshView.as_view(), name='token_refresh'),#refreshToken으로 accessToken 갱신
    path('auth/logout/',LogoutView.as_view(), name='user_logout'),#서버에서 refreshToken 폐기
]