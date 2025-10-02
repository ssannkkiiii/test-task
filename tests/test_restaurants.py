import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestRestaurantListCreate:
    def test_list_restaurants(self, client, restaurant, user):
        client.force_authenticate(user=user)
        url = reverse('restaurants:list-create')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_restaurant_as_admin(self, client, admin_user, restaurant_data):
        client.force_authenticate(user=admin_user)
        url = reverse('restaurants:list-create')
        
        response = client.post(url, restaurant_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == restaurant_data['name']

    def test_create_restaurant_as_regular_user(self, client, user, restaurant_data):
        client.force_authenticate(user=user)
        url = reverse('restaurants:list-create')
        
        response = client.post(url, restaurant_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_restaurant_duplicate_name(self, client, admin_user, restaurant):
        client.force_authenticate(user=admin_user)
        url = reverse('restaurants:list-create')
        data = {
            'name': restaurant.name,
            'address': 'Different address'
        }
        
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRestaurantDetail:
    def test_get_restaurant_detail(self, client, restaurant, user):
        client.force_authenticate(user=user)
        url = reverse('restaurants:detail', kwargs={'pk': restaurant.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == restaurant.name

    def test_update_restaurant_as_admin(self, client, admin_user, restaurant):
        client.force_authenticate(user=admin_user)
        url = reverse('restaurants:detail', kwargs={'pk': restaurant.pk})
        data = {'name': 'Updated Restaurant Name'}
        
        response = client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        restaurant.refresh_from_db()
        assert restaurant.name == 'Updated Restaurant Name'

    def test_update_restaurant_as_regular_user(self, client, user, restaurant):
        client.force_authenticate(user=user)
        url = reverse('restaurants:detail', kwargs={'pk': restaurant.pk})
        data = {'name': 'Updated Restaurant Name'}
        
        response = client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_restaurant_as_admin(self, client, admin_user, restaurant):
        client.force_authenticate(user=admin_user)
        url = reverse('restaurants:detail', kwargs={'pk': restaurant.pk})
        
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_restaurant_as_regular_user(self, client, user, restaurant):
        client.force_authenticate(user=user)
        url = reverse('restaurants:detail', kwargs={'pk': restaurant.pk})
        
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRestaurantSearch:
    def test_search_restaurants_by_name(self, client, restaurant, user):
        client.force_authenticate(user=user)
        url = reverse('restaurants:search')
        response = client.get(url, {'q': 'Test'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_search_restaurants_no_query(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('restaurants:search')
        response = client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_search_restaurants_no_results(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('restaurants:search')
        response = client.get(url, {'q': 'Nonexistent'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
