import requests
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import KakaoCodeSerializer

class KakaoLoginAPIView(GenericAPIView):
    serializer_class = KakaoCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        # 카카오로 토큰 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": "56d45462db421a0576a8bc4710c16560",
            "redirect_uri": "kakao56d45462db421a0576a8bc4710c16560://oauth",
            "code": code
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }

        try:
            kakao_response = requests.post(token_url, data=data, headers=headers)
            kakao_response.raise_for_status()
        except requests.RequestException as e:
            return Response({
                "error": "카카오 토큰 요청 실패",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        token_data = kakao_response.json()

        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        if not access_token:
            return Response({
                "error": "토큰 발급 실패",
                "details": token_data
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": token_data.get("expires_in"),
            "refresh_token_expires_in": token_data.get("refresh_token_expires_in"),
            "token_type": token_data.get("token_type")
        }, status=status.HTTP_200_OK)
