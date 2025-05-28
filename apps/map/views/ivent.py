from django.shortcuts import render
from apps.map.models.ivent import Ivent, IventStreet
from rest_framework import generics
from apps.map.serializers.ivent import IventSerializer, IventStreetSerializer


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
