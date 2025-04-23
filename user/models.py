from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 입력 항목입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    deleted_at=models.DateTimeField(null=True)
    notification = models.BooleanField(default=True)
    fcmToken = models.CharField(max_length=255, null=True, blank=True)
    hashedPhoneNumber = models.CharField(max_length=100, null = True , blank= True)
    image = models.CharField(max_length=255, null=True, blank= True)
    profileName=models.CharField(max_length=20, null=False, blank=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
