from django.urls import path
from user.views import KakaoLoginAPIView,LogoutView,UserUpdateView
from rest_framework_simplejwt.views import TokenRefreshView
from openapi.views import CCTVFetchView, SafetyFacilityFetchView, SafetyServiceFetchView, DisplayIconView, PoliceOfficeFetchView
from .schema import schema_view
urlpatterns = [
    path('api/auth/kakao-login/', KakaoLoginAPIView.as_view(), name='kakao-login'),#카카오 access_token으로 로그인 (JWT 발급)
    path('api/auth/refresh/',TokenRefreshView.as_view(), name='token-refresh'),#refreshToken으로 accessToken 갱신
    path('api/auth/logout/',LogoutView.as_view(), name='user-logout'),#서버에서 refreshToken 폐기
    path('api/fetch-cctv/', CCTVFetchView.as_view(), name='fetch-cctv'),#GET /api/fetch-cctv/?district_code=sm
    path('api/fetch-police-office/', PoliceOfficeFetchView.as_view(), name='fetch-cctv'),
    path('api/fetch-facility/', SafetyFacilityFetchView.as_view(), name='fetch-facility'),
    path('api/fetch-service/', SafetyServiceFetchView.as_view(), name='fetch-service'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/display-icon/',DisplayIconView.as_view(),name='display-icon'),
    path('api/user/',UserUpdateView.as_view(),name='user-setting'),#accessToken필요
]