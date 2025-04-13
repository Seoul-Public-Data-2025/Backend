from django.urls import path
from user.views import KakaoLoginAPIView,LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from openapi.views import CCTVFetchView,PoliceOfficeFetchView
from .schema import schema_view
urlpatterns = [
    path('api/auth/kakao-login/', KakaoLoginAPIView.as_view(), name='kakao_login'),#카카오 access_token으로 로그인 (JWT 발급)
    path('api/auth/refresh/',TokenRefreshView.as_view(), name='token_refresh'),#refreshToken으로 accessToken 갱신
    path('api/auth/logout/',LogoutView.as_view(), name='user_logout'),#서버에서 refreshToken 폐기
    path('api/fetch-cctv/', CCTVFetchView.as_view(), name='fetch-cctv'),#GET /api/fetch-cctv/?district_code=sm
    path('api/fetch-police-office/', PoliceOfficeFetchView.as_view(), name='fetch-cctv'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]