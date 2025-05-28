# your_app/management/commands/refresh_ivent_status.py
from django.core.management.base import BaseCommand
from apps.map.models import Ivent

class Command(BaseCommand):
    help = "Обновляет поле status у событий Ivent по расписанию"

    def handle(self, *args, **options):
        # выбираем все, кроме уже восстановленных (restored)
        qs = Ivent.objects.exclude(status='restored')
        updated = qs.refresh_status().count()
        self.stdout.write(self.style.SUCCESS(
            f"Обновлено событий: {updated}"
        ))
