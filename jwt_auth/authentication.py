from rest_framework import authentication
from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from jwt_auth.models import TokenBlackList, User
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
            raise exceptions.AuthenticationFailed('Expired token')
        else:
            raise exceptions.AuthenticationFailed('Invalid token')

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

        auth = request.META.get('Authorization')

        return validate_token(auth.split(' ').pop())
    
    def authenticate_header(self, request):
        return 'Token'
