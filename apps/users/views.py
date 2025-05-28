from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from djoser.serializers import ActivationSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        


User = get_user_model()

class ActivationGetView(APIView):
    authentication_classes = []
    permission_classes = []
    token_generator = default_token_generator

    def get(self, request, uid, token, *args, **kwargs):
        # 1) Раскодируем UID
        try:
            uid_decoded = urlsafe_base64_decode(uid).decode()
        except Exception:
            uid_decoded = uid

        # 2) Найдём пользователя
        try:
            user = User.objects.get(pk=uid_decoded)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid user id or user does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3) Проверим токен
        if not self.token_generator.check_token(user, token):
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4) Активируем и верифицируем
        updated = []
        if not user.is_active:
            user.is_active = True
            updated.append('is_active')
        # Если у вас есть поле is_verified – сразу тоже помечаем
        if hasattr(user, 'is_verified') and not user.is_verified:
            user.is_verified = True
            updated.append('is_verified')

        if updated:
            user.save(update_fields=updated)

        return Response(
            {'detail': 'User activated and verified successfully.'},
            status=status.HTTP_200_OK
        )