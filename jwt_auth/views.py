import time
import math
from datetime import datetime
import jwt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed
from lightil.util.exception import ClientException
from .model import TokenBlackList
from .authentication import validate_token

class TokenCreateViews(APIView):
    """
    Create Token
    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        """
        Request a new authencation token.
        """
        try:
            username = request.data['username']
            pwd = request.data['pwd']
        except KeyError:
            raise ClientException('Incomplete authentication information')

        try:
            u = User.objects.get(username=username)

            if u.check_password(pwd):
                token = jwt.encode({
                    "uid": u.id,
                    "exp": math.floor(time.time()) + settings.AUTH_EXPIRE_TIME
                }, settings.SECRET_KEY)
                data = { 'token': token }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                raise ClientException('Incorrect authentication information')
        except ObjectDoesNotExist:
            raise ClientException('Incorrect authentication information')

class TokenVerifyDeleteViews(APIView):
    """
    Delete token or verify a token through GET method
    """
    parser_classes = (JSONParser,)

    def get(self, request, token, format=None):
        """
        Validating a token
        """
        try:
            validate_token(token)
        except AuthenticationFailed as exc:
            raise ClientException('Invalid token')
        
        data = {'token': token}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, token, format=None):
        """
        Delete a token by blacklist it, token in the black list is considered invalid.
        """
        try:
            expire_timestamp = jwt.decode(token, key=settings.SECRET_KEY)['exp']
            invalid_token = TokenBlackList(token=token, expire=(datetime.fromtimestamp(expire_timestamp).isoformat() + 'Z'))
            invalid_token.save()
        except jwt.exceptions.DecodeError:
            return ClientException('Invalid token')

        return Response(status=status.HTTP_204_NO_CONTENT)
