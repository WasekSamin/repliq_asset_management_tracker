from rest_framework import serializers
from .models import (
    Device, Category, DeviceDistribution
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        depth = 5


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        depth = 5


class DeviceDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDistribution
        fields = "__all__"
        depth = 5
