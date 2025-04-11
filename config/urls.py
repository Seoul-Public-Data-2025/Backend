from django.urls import path
from user.views import KakaoLoginAPIView

urlpatterns = [
    path('api/auth/kakao/login/', KakaoLoginAPIView.as_view(), name='kakao_login'),
]