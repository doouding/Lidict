import time
import datetime
import math
import jwt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from jwt_auth.serializers import UserSerializer
from .model import TokenBlackList

class AuthViews(APIView):
    """
    Provide jwt base authencation api
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
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
                return Response({ 'detail': '密码错误' }, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, token, format=None):
        """
        Delete a token by adding it to token black list.
        Token in the black list is invalid.
        """
        try:
            expire_timestamp = jwt.decode(token, key=settings.SECRET_KEY)['exp']
            invalid_token = TokenBlackList(token=token, expire=datetime.datetime.fromtimestamp(expire_timestamp).isoformat())
            invalid_token.save()
        except jwt.exceptions.DecodeError:
            return Response({ 'detail': 'Invalid token' })

        return Response(status=status.HTTP_200_OK)
