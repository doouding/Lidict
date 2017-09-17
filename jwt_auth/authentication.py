from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from jwt_auth.model import TokenBlackList
import re
import jwt

def validate_token(token):
    """
    Validate token
    """

    # check whether the token has been blacklisted
    try:
        TokenBlackList.objects.get(token=token)
        raise exceptions.AuthenticationFailed('invalid token')
    except ObjectDoesNotExist:
        pass

    try:
        user_info = jwt.decode(token, settings.SECRET_KEY)
        user = User.objects.get(id=user_info['uid'])
    except jwt.InvalidTokenError as e:
        if isinstance(e, jwt.ExpiredSignatureError):
            raise exceptions.AuthenticationFailed('expired token')
        else:
            raise exceptions.AuthenticationFailed('invalid token')

    return (user, token)

class JwtAuthentication(authentication.BaseAuthentication):
    """
    custom jwt authentication implement
    """

    def authenticate(self, request):
        for path in settings.SKIP_AUTHENTICATION_PATH:
            match = re.search(path, request.path)
            if match:
                return (None, None)

        token = request.META.get('Authorization')
        return authenticate(token)
