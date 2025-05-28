from rest_framework import serializers
from apps.map.models.ivent import Ivent, IventStreet


class IventStreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = IventStreet
        fields = ('id', 'name', 'ivent')


class IventSerializer(serializers.ModelSerializer):
    streets = IventStreetSerializer(many=True, read_only=True)
    class Meta:
        model = Ivent
        fields = ('id', 'city', 'district', 'resource', 'timezone', 'planned_dt',
                  'restored_dt', 'status', 'area', 'streets')

