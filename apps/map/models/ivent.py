from django.contrib.gis.db import models
from django.utils import timezone
import pytz
import datetime


DISTRICT_CHOICES = (
    ('pervomaysky', 'Первомайский'),
    ('leninsky', 'Ленинский'),
    ('sverdlovsky', 'Свердловский'),
    ('oktyabrsky', 'Октябрьский')
)
RESOURCE_TYPE_CHOICES = (
    ('water', 'Вода'),
    ('electricity', 'Электричество'),
    ('gas', 'Газ'),
)
STATUS_CHOICES = (
    ('planned',   'Плановое'),
    ('cancelled', 'Отключено'),
    ('restored',  'Восстановлено'),
)


class Ivent(models.Model):
    city          = models.CharField(max_length=100, verbose_name="Город")
    district      = models.CharField(
        max_length=20,
        choices=DISTRICT_CHOICES,
        default='pervomaysky',
        verbose_name="Район",
        help_text="Выберите район города (Первомайский, Ленинский, Свердловский, Октябрьский)",
    )
    resource = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        default='electricity',
        verbose_name="Тип ресурса",
        help_text="Выберите тип ресурса (вода, электричество, газ)",
    )
    timezone      = models.CharField(
        max_length=50,
        verbose_name="Часовой пояс",
        help_text="IANA (например, Europe/Moscow)",
        default='UTC',
    )
    planned_dt    = models.DateTimeField(verbose_name="Плановая дата и время")
    restored_dt   = models.DateTimeField(
        verbose_name="Время восстановления",
        null=True, blank=True,
    )
    status        = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name="Статус",
    )
    area          = models.PolygonField(srid=4326, verbose_name="Площадь")

    def save(self, *args, **kwargs):
        try:
            tz = pytz.timezone(self.timezone)
        except pytz.UnknownTimeZoneError:
            tz = pytz.UTC

        now = timezone.now().astimezone(tz)
        planned = self.planned_dt.astimezone(tz)
        restored = self.restored_dt.astimezone(tz) if self.restored_dt else None

        print(f"[DEBUG] now={now}, plan={planned}, rest={restored}")

        if now < planned:
            self.status = 'planned'
        elif restored and planned <= now < restored:
            self.status = 'cancelled'  # отключено
        elif restored and now >= restored:
            self.status = 'restored'
        else:
            self.status = 'cancelled'

        super().save(*args, **kwargs)



class IventStreet(models.Model):
    ivent = models.ForeignKey(
        Ivent,
        on_delete=models.CASCADE,
        related_name='streets'
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название улицы",
        help_text="Введите название улицы",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Улица события"
        verbose_name_plural = "Улицы событий"
