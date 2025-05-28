from djoser.serializers import UserCreateSerializer as BaseCreate, UserSerializer as BaseUser
from rest_framework import serializers
from .models import User


class UserCreateSerializer(BaseCreate):
    # явно объявляем re_password
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            're_password',
            'first_name',
            'last_name',
            'addres',
        )
        extra_kwargs = {
            'username':   {'required': True},
            'email':      {'required': True},
            'password':   {'write_only': True, 'required': True},
            're_password':{'write_only': True, 'required': True},
            'first_name': {'required': True},
            'last_name':  {'required': True},
            'addres':     {'required': True},
        }

    def validate(self, data):
        if data['password'] != data.pop('re_password'):
            raise serializers.ValidationError({"re_password": "Пароли не совпадают."})
        return data


class UserSerializer(BaseUser):
    class Meta(BaseUser.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'addres',
            'is_verified',
        )
