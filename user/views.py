import requests
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import KakaoCodeSerializer
import os

class KakaoLoginAPIView(GenericAPIView):
    serializer_class = KakaoCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        """
        code = serializer.validated_data['code']

        # 카카오로 토큰 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        redirect_uri = f'kakao{os.getenv("KAKAO_API_KEY")}://oauth'
        data = {
            "grant_type": "authorization_code",
            "client_id": os.getenv("KAKAO_API_KEY"),
            "redirect_uri": redirect_uri,
            "code": code
        }
        for key,value in data.items():
            print(key,value)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }

        try:
            kakao_response = requests.post(token_url, data=data, headers=headers)
            kakao_response.raise_for_status()
        except requests.RequestException as e:
            print("카카오 요청 실패 응답:", kakao_response.text)
            return Response({
                "success":False
            }, status=status.HTTP_400_BAD_REQUEST)

        token_data = kakao_response.json()

        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        """
        access_token = serializer.validated_data["accessToken"]
        refresh_token = serializer.validated_data["refreshToken"]
        
        if not access_token:
            return Response({
                "success":False
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "email":serializer.validated_data['email'],
            "success":True
        }, status=status.HTTP_200_OK)
