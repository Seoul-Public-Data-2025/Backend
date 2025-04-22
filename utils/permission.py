from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException

class HashedPhoneRequired(APIException):
    status_code = 403
    default_detail = {
        "success": False,
        "message": "전화번호가 등록되어 있지 않습니다.",
    }
    
class HasHashedPhoneNumber(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if not user.hashedPhoneNumber:
            raise HashedPhoneRequired()  # 커스텀 예외 발생
        return True
