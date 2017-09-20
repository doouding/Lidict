from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=8, trim_whitespace=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'nickname', 'username', 'email', 'password')
