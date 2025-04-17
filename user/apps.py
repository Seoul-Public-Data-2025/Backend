from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    # 앱 로딩 시 fcm 자동 초기화
    def ready(self):
        import config.firebase_admin
