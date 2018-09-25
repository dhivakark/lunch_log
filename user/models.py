from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save



class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

