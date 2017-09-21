from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=8, trim_whitespace=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'nickname', 'username', 'email', 'password')

    # default `create` method call `model.objects.create` method to create new instance
    # override to create user correctly
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # since the password cannot be changed directly
    # override to update user correctly
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance
