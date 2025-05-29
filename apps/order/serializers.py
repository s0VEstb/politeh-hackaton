from rest_framework import serializers
from core.services.spam_detection import predict_spam_score
from .models import Report, ReportLike

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'user', 'district', 'address', 'resource',
            'description', 'area', 'created_at',
            'spam_score', 'requires_moderation', 'problem_status',
            'status_updated_at', 'likes_count',
        ]
        read_only_fields = [
            'created_at', 'spam_score', 'requires_moderation',
            'problem_status', 'status_updated_at', 'likes_count'
        ]

    def validate(self, data):
        # перед сохранением считаем спам-скор
        score = predict_spam_score(data.get('description', ''))
        if score > 0.95:
            raise serializers.ValidationError({
                'description': 'Сообщение распознано как спам и не сохраняется.'
            })
        # добавляем поля в validated_data
        data['spam_score'] = score
        data['requires_moderation'] = score > 0.8
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)  # удаляем, если есть
        return Report.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        # разрешаем менять только эти поля
        for field in ('district','address','resource','description','area'):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class ReportLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ReportLike
        fields = ['id', 'user', 'report', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        report = data.get('report')
        if ReportLike.objects.filter(user=user, report=report).exists():
            raise serializers.ValidationError(
                'Вы уже поставили лайк этому отчету.'
            )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)  # удаляем, если есть
        return Report.objects.create(user=user, **validated_data)