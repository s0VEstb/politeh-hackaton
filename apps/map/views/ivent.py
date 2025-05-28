from django.shortcuts import render
from apps.map.models.ivent import Ivent, IventStreet
from rest_framework import generics
from apps.map.serializers.ivent import IventSerializer, IventStreetSerializer
from apps.map.models import Ivent, RESOURCE_TYPE_CHOICES
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class GazIventListAPIView(generics.ListAPIView):
    queryset = Ivent.objects.filter(resource='gas')
    serializer_class = IventSerializer
    pagination_class = None 


class ElectricityIventListAPIView(generics.ListAPIView):
    queryset = Ivent.objects.filter(resource='electricity')
    serializer_class = IventSerializer
    pagination_class = None


class WaterIventListAPIView(generics.ListAPIView):
    queryset = Ivent.objects.filter(resource='water')
    serializer_class = IventSerializer
    pagination_class = None


class ResourceOutageStatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Динамически получаем названия и цвета
        resource_labels = {key: label for key, label in RESOURCE_TYPE_CHOICES}
        resource_colors = {
            key: ['#3498db', '#f1c40f', '#e74c3c'][i % 3]
            for i, (key, _) in enumerate(RESOURCE_TYPE_CHOICES)
        }

        # Подсчет отключений
        stats = defaultdict(int)
        for ivent in Ivent.objects.filter(status='cancelled'):
            stats[ivent.resource] += 1

        # Формируем ответ
        data = []
        for key, label in resource_labels.items():
            data.append({
                'type': label,
                'count': stats.get(key, 0),
                'color': resource_colors.get(key, '#000000')
            })

        return Response(data)