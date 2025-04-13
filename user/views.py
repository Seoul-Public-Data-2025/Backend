import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import KakaoTokenSerializer
from django.contrib.auth import get_user_model

User=get_user_model()

class KakaoLoginAPIView(TokenObtainPairView):
    serializer_class = KakaoTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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
            user,created=User.objects.get_or_create(
                email=serializer.validated_data['email'],#requset로 왔었던 이메일로 저장하기
                #email=data['id'] 카카오 accessToken검증 api의 response로 온 카카오 메일을 저장하기
            )
            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            return Response({
                'success':True,
                'result':{
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                    'user_id': user.email
                }
            }, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as http_err:
            if kakao_response.status_code == 401:#access token이 유효하지 않은 경우 401에러 발생
                return Response({
                    'success': False,
                    'result':{
                        'error': 'Invalid or expired access token'
                    }
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:#필수 인자가 포함되지 않은 경우나 호출 인자값의 데이터 타입이 적절하지 않거나 허용된 범위를 벗어난 경우
                return Response({
                    'success': False,
                    'result':{
                        'error': f'HTTP error occurred: {http_err}',
                        'status_code': kakao_response.status_code
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as req_err:#카카오 서버 요청 오류, 혹은 유저 생성 및 jwt토큰 발급 오류
            return Response({
                'success': False,
                'result':{
                        'error': f'Request failed: {req_err}'
                    }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")  # 요청에서 Refresh Token 가져오기
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 추가

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
