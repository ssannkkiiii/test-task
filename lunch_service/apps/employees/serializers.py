from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EmployeeProfile

User = get_user_model()

class EmployeeProfileSerializer(serializers.ModelSerializer):

    full_name = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = EmployeeProfile
        fields = (
            'id', 'user_id', 'employee_id', 'department', 'position',
            'hire_date', 'is_active', 'full_name', 'email',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'user_id')


class EmployeeProfileCreateSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = EmployeeProfile
        fields = (
            'employee_id', 'department', 'position', 'hire_date',
            'username', 'email', 'first_name', 'last_name', 'password'
        )

    def validate_employee_id(self, value):
        if EmployeeProfile.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee with this ID already exists.")
        return value

    def create(self, validated_data):

        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
        }

        user = User.objects.create_user(**user_data)

        employee_profile = EmployeeProfile.objects.create(user=user, **validated_data)
        return employee_profile


class EmployeeListSerializer(serializers.ModelSerializer):

    full_name = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id', 'employee_id', 'full_name', 'email',
            'department', 'position', 'is_active'
        )
