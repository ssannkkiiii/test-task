from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    is_available_today = serializers.ReadOnlyField()

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'description', 'address', 'phone_number',
            'email', 'website', 'is_active', 'is_available_today',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_available_today')


class RestaurantCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = (
            'name', 'description', 'address', 'phone_number',
            'email', 'website', 'is_active'
        )

    def validate_name(self, value):
        if Restaurant.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Restaurant with this name already exists.")
        return value


class RestaurantUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = (
            'name', 'description', 'address', 'phone_number',
            'email', 'website', 'is_active'
        )

    def validate_name(self, value):
        if Restaurant.objects.filter(name__iexact=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Restaurant with this name already exists.")
        return value
