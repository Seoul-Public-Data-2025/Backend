import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import KakaoTokenSerializer
from django.contrib.auth import get_user_model
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
logger = logging.getLogger(__name__)

User=get_user_model()

class KakaoLoginAPIView(TokenObtainPairView):
    serializer_class = KakaoTokenSerializer
    @swagger_auto_schema(
        operation_summary="카카오 로그인",
        operation_description="카카오 accessToken을 이용해 JWT 토큰을 발급받습니다. 이미 가입된 이메일이면 로그인, 없으면 새로 생성.",
        request_body=KakaoTokenSerializer,
        responses={
            200: openapi.Response(
                description="로그인 성공",
                examples={
                    "application/json": {
                        "success": True,
                        "result": {
                            "accessToken": "jwt_access_token",
                            "refreshToken": "jwt_refresh_token"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Invalid data"
                    }
                }
            ),
            401: openapi.Response(
                description="카카오 토큰 유효하지 않음",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Invalid or expired access token"
                    }
                }
            ),
        },
        tags=["Auth"]
    )
    def post(self, request, *args, **kwargs):
        # 확인용
        print("🟢 headers:", request.headers)
        print("🟢 content_type:", request.content_type)
        print("🟢 body:", request.body)  # 원본 요청 raw 보기
        print("🟢 request.data:", request.data)  # DRF가 파싱한 데이터
        logger.info(f"[카카오 로그인 요청] {request.data}")
        # 확인용_end
        
        serializer = self.get_serializer(data=request.data)

        # 먼저 이메일 중복을 검사
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:  # 이메일 중복이 있을 경우
            # JWT 리프레시 토큰 발급
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'result': {
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                }
            }, status=status.HTTP_200_OK)

        # 이메일 중복이 없으면 시리얼라이저 유효성 검사를 진행
        if not serializer.is_valid():  # serializer 유효성 검사를 먼저 실행
            return Response({
                'success': False,
                'message': 'Invalid data'
            }, status=status.HTTP_400_BAD_REQUEST)

        access_token = serializer.validated_data['accessToken']
        
        # 카카오 액세스 토큰 유효성 검사
        token_check_url = "https://kapi.kakao.com/v1/user/access_token_info"
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        try:
            kakao_response = requests.get(url=token_check_url, headers=headers)
            kakao_response.raise_for_status()  # status_code 200이 아니면 예외 발생
            data = kakao_response.json()

            # 새 사용자 생성
            user = User.objects.create(email=email)
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'result': {
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                }
            }, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as http_err:
            if kakao_response.status_code == 401:  # access token이 유효하지 않은 경우 401에러 발생
                return Response({
                    'success': False,
                    'message': 'Invalid or expired access token'
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:  # 필수 인자가 포함되지 않은 경우나 호출 인자값의 데이터 타입이 적절하지 않거나 허용된 범위를 벗어난 경우
                return Response({
                    'success': False,
                    'message': f'HTTP error occurred: {http_err}',
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as req_err:  # 카카오 서버 요청 오류, 혹은 유저 생성 및 jwt토큰 발급 오류
            return Response({
                'success': False,
                'message': f'Request failed: {req_err}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")  # 요청에서 Refresh Token 가져오기
            if not refresh_token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 추가

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
