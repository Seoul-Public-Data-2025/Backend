from firebase_admin import messaging

def send_fcm_notification(token, title, body, data=None):
    """
    단일 FCM 토큰으로 푸시 메시지를 보냅니다.

    :param token: 수신자의 FCM 토큰
    :param title: 푸시 알림 제목
    :param body: 푸시 알림 본문
    :param data: (선택) 딕셔너리 형태의 추가 데이터
    :return: 응답 메시지 ID 또는 예외
    """
    try:
        message = messaging.Message(
            token=token,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data or {},  # 딕셔너리 형태로 추가 데이터 전달 가능
        )

        response = messaging.send(message)
        return response  # 메시지 ID 반환
    except Exception as e:
        print(f"FCM fail : {e}")
        return None
