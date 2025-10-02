from rest_framework import serializers
from django.utils import timezone
from .models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):

    dietary_info = serializers.ReadOnlyField()

    class Meta:
        model = MenuItem
        fields = (
            'id', 'name', 'description', 'category', 'price',
            'is_vegetarian', 'is_vegan', 'is_gluten_free',
            'allergens', 'calories', 'is_available', 'dietary_info',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'dietary_info')


class MenuItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = (
            'name', 'description', 'category', 'price',
            'is_vegetarian', 'is_vegan', 'is_gluten_free',
            'allergens', 'calories', 'is_available'
        )


class MenuSerializer(serializers.ModelSerializer):

    items = MenuItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Menu
        fields = (
            'id', 'restaurant', 'restaurant_name', 'date', 'title',
            'description', 'is_active', 'total_items', 'is_today',
            'items', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class MenuCreateSerializer(serializers.ModelSerializer):

    items = MenuItemCreateSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = (
            'restaurant', 'date', 'title', 'description',
            'is_active', 'items'
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        menu = Menu.objects.create(**validated_data)
        
        for item_data in items_data:
            MenuItem.objects.create(menu=menu, **item_data)
        
        return menu

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Cannot create menu for past dates.")
        return value


class MenuListSerializer(serializers.ModelSerializer):

    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')
    total_items = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()

    class Meta:
        model = Menu
        fields = (
            'id', 'restaurant', 'restaurant_name', 'date',
            'title', 'total_items', 'is_today', 'is_active'
        )


class TodayMenuSerializer(serializers.ModelSerializer):

    items = MenuItemSerializer(many=True, read_only=True)
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')
    restaurant_address = serializers.ReadOnlyField(source='restaurant.address')

    class Meta:
        model = Menu
        fields = (
            'id', 'restaurant', 'restaurant_name', 'restaurant_address',
            'date', 'title', 'description', 'items'
        )
