from rest_framework import serializers
from django.utils import timezone
from .models import Vote, VotingResult
from lunch_service.apps.menus.serializers import TodayMenuSerializer


class VoteSerializer(serializers.ModelSerializer):

    user_name = serializers.ReadOnlyField(source='user.full_name')
    restaurant_name = serializers.ReadOnlyField(source='menu.restaurant.name')
    menu_title = serializers.ReadOnlyField(source='menu.title')

    class Meta:
        model = Vote
        fields = (
            'id', 'user', 'user_name', 'menu', 'restaurant_name',
            'menu_title', 'date', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'user_name', 'restaurant_name', 'menu_title')


class VoteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('menu', 'date')

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Cannot vote for past dates.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        date = attrs.get('date') or timezone.now().date()
        
        if Vote.objects.filter(user=user, date=date).exists():
            raise serializers.ValidationError("You have already voted for this date.")
        
        menu = attrs.get('menu')
        if menu and menu.date != date:
            raise serializers.ValidationError("Menu date does not match vote date.")
        
        if menu and not menu.is_active:
            raise serializers.ValidationError("Cannot vote for inactive menu.")
        
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        if not validated_data.get('date'):
            validated_data['date'] = timezone.now().date()
        return super().create(validated_data)


class VotingResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = VotingResult
        fields = ('date', 'results', 'total_votes', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class TodayVoteSerializer(serializers.ModelSerializer):

    menu = TodayMenuSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'menu', 'date', 'created_at')


class VoteStatsSerializer(serializers.Serializer):
    total_votes = serializers.IntegerField()
    user_voted = serializers.BooleanField()
    user_vote = serializers.DictField(required=False, allow_null=True)  
    results = serializers.DictField()
