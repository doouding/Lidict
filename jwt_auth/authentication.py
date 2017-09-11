from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from jwt_auth.model import TokenBlackList
import jwt

class JwtAuthentication(authentication.BaseAuthentication):
    """
    custom jwt authentication implement
    """

    def authenticate(self, request):
        token = request.META.get('auth-token')

        try:
            TokenBlackList.objects.get(token=token)
            raise exceptions.AuthenticationFailed
        except ObjectDoesNotExist:
            pass

        try:
            user_info = jwt.decode(token)
            user = User.objects.get(id=user_info.id)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed
        
        return (user, None)
