from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class TokenBlackList(models.Model):
    """
    Token in the black list is considered invalid.
    This is an implement of deleting a token.
    """
    token = models.CharField(max_length=200)
    expire = models.DateTimeField()

class CustomUserManager(UserManager):    
    # the default `create_user` allow password field left empty
    # override to make password required
    def create_user(self, username, email, password, **extra_fields):
        if password is None:
            raise ValueError('Password must be given')
        return super()._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=150,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name='nick name',
        max_length=10,
    )

    objects = CustomUserManager()
