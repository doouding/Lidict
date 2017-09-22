"""
Jwt-auth app provide user and token related functionality
"""
import time
import math
from datetime import datetime
import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from lightil.util.exception import ClientException
from .models import TokenBlackList, User
from .serializers import UserSerializer

class TokenViews(viewsets.ViewSet):
    """
    Provide `create`, `delete` actions for token
    """

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
            user = User.objects.get(username=username)

            if user.check_password(pwd):
                token = jwt.encode({
                    "uid": user.id,
                    "exp": math.floor(time.time()) + settings.AUTH_EXPIRE_TIME
                }, settings.SECRET_KEY)
                data = {'token': token}
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                raise ClientException('Incorrect authentication information')
        except ObjectDoesNotExist:
            raise ClientException('Incorrect authentication information')

    def delete(self, request, token, format=None):
        """
        Delete a token by blacklist it, token in the black list is considered invalid.
        """
        if request.auth is token:
            raise PermissionDenied('You can only delete the token you currently use')

        try:
            expire_timestamp = jwt.decode(token, key=settings.SECRET_KEY)['exp']
            invalid_token = TokenBlackList(
                token=token,
                expire=(datetime.fromtimestamp(expire_timestamp).isoformat() + 'Z'),
            )
            invalid_token.save()
        except jwt.exceptions.DecodeError:
            return ClientException('Invalid token')

        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViews(viewsets.GenericViewSet,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin):
    """
    Provide `create`, `retrieve`, `update` for user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # identify an user by `username` field not primary key
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # username cannot be changed once user is created
        # email cannot be changed directly PUT /user/{username}/email to update email
        try:
            del kwargs['username']
            del kwargs['email']
        except KeyError:
            pass

        kwargs['partial'] = True

        return self.update(request, *args, **kwargs)
