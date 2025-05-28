from django.contrib import admin
from ..models import Ivent, IventStreet
from leaflet.admin import LeafletGeoAdmin
from django.utils.timezone import make_aware
import pytz


class IventStreetInline(admin.TabularInline):
    model = IventStreet
    extra = 1  # Кол-во пустых строк по умолчанию
    verbose_name = "Улица"
    verbose_name_plural = "Улицы"
    fields = ('name',)


@admin.register(Ivent)
class IventAdmin(LeafletGeoAdmin):
    list_display = (
        'city',
        'district',
        'resource',
        'status',
        'planned_dt',
        'restored_dt',
        'timezone',
    )
    list_filter = ('status', 'city', 'district', 'timezone')
    search_fields = ('city', 'district')
    readonly_fields = ('status',)
    inlines = [IventStreetInline]

    fieldsets = (
        (None, {
            'fields': (
                'city',
                'district',
                'resource',
                'timezone',
                'planned_dt',
                'restored_dt',
                'status',
                'area',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        # Получаем timezone из модели
        tz = pytz.timezone(obj.timezone or 'Asia/Bishkek')

        # Если время введено без tzinfo (т.е. наивное), превращаем в aware
        if obj.planned_dt and obj.planned_dt.tzinfo is None:
            obj.planned_dt = make_aware(obj.planned_dt, timezone=tz)

        if obj.restored_dt and obj.restored_dt.tzinfo is None:
            obj.restored_dt = make_aware(obj.restored_dt, timezone=tz)

        super().save_model(request, obj, form, change)
