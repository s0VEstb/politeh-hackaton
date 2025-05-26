from django.dispatch import receiver
from djoser.signals import user_activated

@receiver(user_activated)
def set_is_verified(sender, user, request, **kwargs):
    if not user.is_verified:
        user.is_verified = True
        user.save()
