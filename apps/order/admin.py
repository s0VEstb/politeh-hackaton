from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Report, ReportLike


class ReportLikeInline(admin.TabularInline):
    model = ReportLike
    extra = 0
    readonly_fields = ('user', 'created_at')
    can_delete = True
    show_change_link = True


@admin.register(Report)
class ReportAdmin(LeafletGeoAdmin):
    list_display = (
        'id',
        'user',
        'district',
        'address',
        'resource',
        'problem_status',
        'spam_score',
        'requires_moderation',
        'is_spam_display',
        'likes_count',
        'created_at',
    )
    list_filter = ('requires_moderation', 'problem_status', 'district', 'resource')
    search_fields = ('user__username', 'description', 'address')
    list_editable = ('problem_status',)
    readonly_fields = ('created_at', 'spam_score', 'requires_moderation', 'is_spam_display', 'likes_count')
    fieldsets = (
        (None, {
            'fields': ('user', 'district', 'address', 'resource', 'description', 'area')
        }),
        ('Статус и модерация', {
            'fields': ('problem_status', 'status_updated_at', 'spam_score', 'requires_moderation', 'is_spam_display')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'likes_count')
        }),
    )
    inlines = [ReportLikeInline]
    actions = ['mark_as_not_spam', 'mark_as_spam']

    def is_spam_display(self, obj):
        return obj.is_spam
    
    is_spam_display.boolean = True
    is_spam_display.short_description = 'Спам?'

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Лайков'

    @admin.action(description="Пометить как не спам")
    def mark_as_not_spam(self, request, queryset):
        queryset.update(requires_moderation=False)

    @admin.action(description="Удалить как спам")
    def mark_as_spam(self, request, queryset):
        for report in queryset:
            report.delete()

    def save_model(self, request, obj, form, change):
        # При изменении статуса отмечаем время обновления
        if change and 'problem_status' in form.changed_data:
            from django.utils import timezone
            obj.status_updated_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(ReportLike)
class ReportLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'report', 'created_at')
    search_fields = ('user__username', 'report__description')
    readonly_fields = ('created_at',)
