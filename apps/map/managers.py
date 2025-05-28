# your_app/managers.py
from django.db import models
from django.utils import timezone
import pytz

class IventQuerySet(models.QuerySet):
    def refresh_status(self):
        """
        Пробегает по всем событиям в этом QuerySet и
        обновляет поле status согласно текущему времени.
        """
        for iv in self:
            # 1) определяем tz
            try:
                tz = pytz.timezone(iv.timezone)
            except pytz.UnknownTimeZoneError:
                tz = pytz.UTC

            # 2) текущее время и даты события в этой tz
            now      = timezone.now().astimezone(tz)
            planned  = iv.planned_dt.astimezone(tz)
            restored = iv.restored_dt.astimezone(tz) if iv.restored_dt else None

            # 3) та же логика, что и в save()
            if now < planned:
                new_status = 'planned'
            elif restored and planned <= now < restored:
                new_status = 'cancelled'
            elif restored and now >= restored:
                new_status = 'restored'
            else:
                new_status = 'cancelled'

            # 4) сохраняем только если действительно поменялось
            if iv.status != new_status:
                iv.status = new_status
                iv.save(update_fields=['status'])
        return self
