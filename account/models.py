from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password) 
        user.save(using=self._db) 
        user.send_activation_code() 
        return user

    def create_user(self, email, password, **kwargs):
        return self._create(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create(email, password, **kwargs)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    username = None
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=8, allowed_chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
        self.activation_code = code
        self.save()

    def send_activation_code(self):
        from django.core.mail import send_mail
        self.create_activation_code()
        activation_link = f'http://127.0.0.1:8000/account/activate/{self.activation_code}'
        message = f'Activate your account using a link:\n {activation_link}'
        send_mail('Activate account', message, 'admin@admin.com',recipient_list=[self.email])
