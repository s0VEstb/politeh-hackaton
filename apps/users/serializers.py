from djoser.serializers import UserCreateSerializer as BaseCreate, UserSerializer as BaseUser
from .models import User


class UserCreateSerializer(BaseCreate):
    class Meta(BaseCreate.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')

class UserSerializer(BaseUser):
    class Meta(BaseUser.Meta):
        model = User
        fields = ('id', 'email', 'username', 'is_verified')
