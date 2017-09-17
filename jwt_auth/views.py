import time
import math
from datetime import datetime
import jwt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, exceptions
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
            return Response({ 'detail': '不完整的验证信息' }, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({ 'detail': '验证信息错误' }, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({ 'detail': '验证信息错误' }, status=status.HTTP_400_BAD_REQUEST)

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
        except exceptions.AuthenticationFailed as e:
            return Response({ 'detail': e.detail }, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, token, format=None):
        """
        Delete a token by blacklist it, token in the black list is considered invalid.
        """
        try:
            expire_timestamp = jwt.decode(token, key=settings.SECRET_KEY)['exp']
            invalid_token = TokenBlackList(token=token, expire=(datetime.fromtimestamp(expire_timestamp).isoformat() + 'Z'))
            invalid_token.save()
        except jwt.exceptions.DecodeError:
            return Response({ 'detail': '无效的Token' }, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
