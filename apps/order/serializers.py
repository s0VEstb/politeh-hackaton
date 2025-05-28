from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Report, ReportLike

User = get_user_model()

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') 
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id',
            'user',
            'district',
            'address',
            'resource',
            'description',
            'area',
            'created_at',
            'spam_score',
            'problem_status',
            'status_updated_at',
            'likes_count',
        ]
        read_only_fields = ['created_at', 'spam_score', 'problem_status', 'status_updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)  # удаляем user, если он есть
        return Report.objects.create(user=user, **validated_data)


    def update(self, instance, validated_data):
        # запрещаем менять всё, кроме перечисленных полей
        allowed_fields = ['district', 'address', 'resource', 'description', 'area']
        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance
    

class ReportLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # показываем кто лайкнул, менять нельзя

    class Meta:
        model = ReportLike
        fields = ['id', 'user', 'report', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        report = data.get('report')

        # Проверяем, что пользователь еще не лайкал этот отчёт
        if ReportLike.objects.filter(user=user, report=report).exists():
            raise serializers.ValidationError("Вы уже поставили лайк этому отчету.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return ReportLike.objects.create(user=user, **validated_data)

