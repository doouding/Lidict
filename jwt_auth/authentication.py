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
        raise exceptions.AuthenticationFailed('Invalid token')
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
        # check the request path is excluded or not
        paths = list(settings.AUTHENTICATION_EXCLUDE['ALL']) if 'ALL' in settings.AUTHENTICATION_EXCLUDE else []

        try:
            paths.extend(list(settings.AUTHENTICATION_EXCLUDE[request.method]))
        except KeyError:
            pass

        for path in paths:
            match = re.search(path, request.path)
            if match:
                return (None, None)
        
        # do authentication
        try:
            auth = request.META.get('Authorization').split(' ')
        except:
            raise exceptions.AuthenticationFailed('The resource require token to authenticate')

        auth_type = auth[0]
        token = auth[1]

        if auth_type.lower() == 'token':
            return validate_token(token)
        else:
            raise exceptions.AuthenticationFailed('Invalid authentication header')

    def authenticate_header(self, request):
        return 'Token'
