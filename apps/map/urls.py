from apps.map.views.ivent import (
    WaterIventListAPIView,
    ElectricityIventListAPIView,
    GazIventListAPIView,
)
from django.urls import path


urlpatterns = [
    path('water/', WaterIventListAPIView.as_view(), name='water_ivent_list'),
    path('electricity/', ElectricityIventListAPIView.as_view(), name='electricity_ivent_list'),
    path('gas/', GazIventListAPIView.as_view(), name='gaz_ivent_list'),
]