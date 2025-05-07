from django.urls import path,include
from user.views import KakaoLoginAPIView, LogoutView, UserUpdateDeleteView
from relation.views import RelationRequestView, RelationApproveView, RelationParentListView, RelationChildListView, ResendNotificationView, RelationUpdateNameView, RelationDeleteView,FCMTestView
from user.views import KakaoLoginAPIView,LogoutView,HealthCheckView
from rest_framework_simplejwt.views import TokenRefreshView
from openapi.views import CCTVFetchView, SafetyFacilityFetchView, SafetyServiceFetchView, DisplayIconView, PoliceOfficeFetchView
from .schema import schema_view
from django.urls import path
from sim.views import sse_stream, ChildLocationView, ChildDisconnectView
urlpatterns = [
    path('',HealthCheckView.as_view(),name='health-check'),
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
    path('api/relation-request/', RelationRequestView.as_view(),name='relation-request'),
    path('api/relation-resend/', ResendNotificationView.as_view(), name='relation-resend'),
    path('api/relation-approve/', RelationApproveView.as_view(), name='relation-approve'), # fcm 연동으로 relation_id 포함한 실시간 알림 날려야 함
    path('api/relation-parent-list/', RelationParentListView.as_view(),name='relation-parent-list'),
    path('api/relation-child-list/', RelationChildListView.as_view(),name='relation-child-list'),
    path('api/relation-update/',RelationUpdateNameView.as_view(),name='relation-update-name'),
    path('api/relation-delete/',RelationDeleteView.as_view(),name='relation-delete'),
    path('api/user/',UserUpdateDeleteView.as_view(),name='user-update-delete'),#accessToken필요
    path('test-fcm/',FCMTestView.as_view(),name='fcm-test'),
    # sim/urls.py
    path('events/child/<str:uid>/', sse_stream),  # SSE 엔드포인트
    path('api/child-location/', ChildLocationView.as_view()),
    path('api/child-disconnection/', ChildDisconnectView.as_view())
]