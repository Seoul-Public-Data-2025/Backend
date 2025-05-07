from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # 기본 DRF 예외 처리
    response = exception_handler(exc, context)

    # 예외가 발생하고 응답이 있을 때
    if response is not None:
        # response.data가 딕셔너리인지 리스트인지 확인하여 처리
        if isinstance(response.data, dict):
            # 'detail' 또는 'message' 필드를 찾아 메시지 설정
            message = response.data.get('detail') or response.data.get('message') or str(response.data)
        else:
            # 리스트인 경우 메시지 처리 방법 정의 (예: 첫 번째 항목 가져오기)
            message = str(response.data[0])  # 리스트라면, 그 자체를 문자열로 변환하여 메시지로 사용

        # 메시지를 'success'와 함께 응답 데이터로 설정
        response.data = {
            'success': False,
            'message': message
        }

    # 예외 처리 응답이 없을 경우 (서버 오류 처리)
    else:
        response = Response({
            'success': False,
            'message': str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
