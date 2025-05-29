from django.contrib.gis.db import models
from django.utils import timezone
import pytz
import datetime
from django.conf import settings
from apps.map.models import DISTRICT_CHOICES, RESOURCE_TYPE_CHOICES
from core.services.spam_detection import predict_spam_score
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



PROBLEM_STATUS = [
    ('unresolved', 'Не решена'),
    ('resolved', 'Решена'),
]

class Report(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Пользователь'
    )
    district = models.CharField(
        max_length=100,
        choices=DISTRICT_CHOICES,
        verbose_name='Район'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
        default='Не указан',
        help_text='Укажите точный адрес проблемы'
    )
    resource = models.CharField(
        max_length=100,
        choices=RESOURCE_TYPE_CHOICES,
        verbose_name='Тип ресурса'
    )
    description = models.TextField(
        verbose_name='Описание проблемы'
    )
    area = models.PolygonField(
        srid=4326,
        verbose_name='Площадь',
        help_text='Полигон, описывающий область проблемы'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время создания'
    )

    # эти поля заполняются через сериализатор
    spam_score = models.FloatField(
        default=0.0,
        verbose_name='Оценка спама (0–1)'
    )
    requires_moderation = models.BooleanField(
        default=False,
        verbose_name='Требует модерации'
    )
    problem_status = models.CharField(
        max_length=20,
        choices=PROBLEM_STATUS,
        default='unresolved',
        verbose_name='Статус решения'
    )
    status_updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления статуса'
    )

    @property
    def is_spam(self):
        # Например, считать спамом если оценка выше 0.8
        return self.spam_score > 0.8

    def __str__(self):
        return f"Report by {self.user.username} in {self.district}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ["-created_at"]


class ReportLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'report')

    def __str__(self):
        return f"{self.user.username} likes {self.report.id}"