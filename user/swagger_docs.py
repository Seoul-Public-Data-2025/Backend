from drf_yasg import openapi
from .serializer import KakaoTokenSerializer

kakao_login_doc = {
    "operation_summary": "카카오 로그인",
    "operation_description": "카카오 accessToken을 이용해 JWT 토큰을 발급받습니다.\n\n"
                             "- 이미 가입된 이메일이면 로그인 처리\n"
                             "- 없으면 새로 유저를 생성하고 JWT 토큰 발급",
    "request_body": KakaoTokenSerializer,
    "responses": {
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
                    "message": "Invalid data",
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
    "tags": ["Auth"]
}