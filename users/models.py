from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


STATUS_CHOICES = [
    ('a', 'Active'),
    ('b', 'Block')
]


class CustomUser(AbstractUser):
    objects = UserManager()
    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=200)
    description = models.TextField()
    email_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def short_description(self):
        return self.description[:20]


