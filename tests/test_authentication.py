import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registration_success(self, client):
        url = reverse('authentication:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'tokens' in response.data
        assert 'user' in response.data
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_user_registration_password_mismatch(self, client):
        url = reverse('authentication:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'password': 'newpass123',
            'password_confirm': 'differentpass'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_user_registration_duplicate_email(self, client, user):
        url = reverse('authentication:register')
        data = {
            'username': 'anotheruser',
            'email': user.email,
            'first_name': 'Another',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    def test_user_login_success(self, client, user):
        url = reverse('authentication:login')
        data = {
            'email': user.email,
            'password': 'testpass123'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data
        assert 'user' in response.data

    def test_user_login_invalid_credentials(self, client):
        url = reverse('authentication:login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpass'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_login_inactive_user(self, client, user):
        user.is_active = False
        user.save()
        
        url = reverse('authentication:login')
        data = {
            'email': user.email,
            'password': 'testpass123'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfile:
    def test_get_user_profile(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('authentication:profile')
        
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    def test_update_user_profile(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('authentication:profile')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.first_name == 'Updated'

    def test_change_password(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('authentication:change-password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password('newpass123')

    def test_change_password_wrong_old_password(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('authentication:change-password')
        data = {
            'old_password': 'wrongpass',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
