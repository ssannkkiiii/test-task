import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from lunch_service.apps.restaurants.models import Restaurant
from lunch_service.apps.employees.models import EmployeeProfile
from lunch_service.apps.menus.models import Menu, MenuItem

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpass123'
    }


@pytest.fixture
def admin_user_data():
    return {
        'username': 'admin',
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'password': 'adminpass123',
        'is_staff': True,
        'is_superuser': True
    }


@pytest.fixture
def user(db, user_data):
    return User.objects.create_user(**user_data)


@pytest.fixture
def admin_user(db, admin_user_data):
    return User.objects.create_user(**admin_user_data)


@pytest.fixture
def restaurant_data():
    return {
        'name': 'Test Restaurant',
        'description': 'A test restaurant',
        'address': '123 Test Street',
        'phone_number': '+1234567890',
        'email': 'test@restaurant.com',
        'website': 'https://testrestaurant.com'
    }


@pytest.fixture
def restaurant(db, restaurant_data):
    return Restaurant.objects.create(**restaurant_data)


@pytest.fixture
def employee_profile_data():
    return {
        'employee_id': 'EMP001',
        'department': 'Engineering',
        'position': 'Developer',
        'hire_date': '2023-01-01'
    }


@pytest.fixture
def employee_profile(db, user, employee_profile_data):
    return EmployeeProfile.objects.create(user=user, **employee_profile_data)


@pytest.fixture
def menu_data():
    from django.utils import timezone
    return {
        'title': 'Test Menu',
        'description': 'A test menu',
        'date': timezone.now().date(),
        'is_active': True
    }


@pytest.fixture
def menu(db, restaurant, menu_data):
    return Menu.objects.create(restaurant=restaurant, **menu_data)


@pytest.fixture
def menu_item_data():
    return {
        'name': 'Test Dish',
        'description': 'A test dish',
        'category': 'main_course',
        'price': 12.99,
        'is_vegetarian': False,
        'is_vegan': False,
        'is_gluten_free': True
    }


@pytest.fixture
def menu_item(db, menu, menu_item_data):
    return MenuItem.objects.create(menu=menu, **menu_item_data)