import firebase_admin
from firebase_admin import credentials
from django.conf import settings

# Firebase가 아직 초기화되지 않았다면 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIAL_PATH)
    firebase_admin.initialize_app(cred)