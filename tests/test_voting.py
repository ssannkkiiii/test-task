import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from lunch_service.apps.voting.models import Vote


@pytest.mark.django_db
class TestVoting:
    def test_vote_for_restaurant(self, client, user, menu):
        client.force_authenticate(user=user)
        url = reverse('voting:vote-restaurant', kwargs={'menu_id': menu.pk})
        
        response = client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert Vote.objects.filter(user=user, menu=menu).exists()

    def test_vote_twice_same_day(self, client, user, menu):
        client.force_authenticate(user=user)
        url = reverse('voting:vote-restaurant', kwargs={'menu_id': menu.pk})
        
        response = client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        
        response = client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_vote_for_inactive_menu(self, client, user, menu):
        menu.is_active = False
        menu.save()
        
        client.force_authenticate(user=user)
        url = reverse('voting:vote-restaurant', kwargs={'menu_id': menu.pk})
        
        response = client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_vote_for_nonexistent_menu(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('voting:vote-restaurant', kwargs={'menu_id': 999})
        
        response = client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_today_vote(self, client, user, menu):
        Vote.objects.create(user=user, menu=menu, date=timezone.now().date())
        
        client.force_authenticate(user=user)
        url = reverse('voting:today-vote')
        
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['menu']['id'] == menu.pk

    def test_get_today_vote_no_vote(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('voting:today-vote')
        
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_today_results(self, client, user, menu):
        Vote.objects.create(user=user, menu=menu, date=timezone.now().date())
        
        client.force_authenticate(user=user)
        url = reverse('voting:today-results')
        
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_votes'] == 1
        assert response.data['user_voted'] is True

    def test_cancel_today_vote(self, client, user, menu):
        Vote.objects.create(user=user, menu=menu, date=timezone.now().date())
        
        client.force_authenticate(user=user)
        url = reverse('voting:cancel-today')
        
        response = client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert not Vote.objects.filter(user=user, date=timezone.now().date()).exists()

    def test_cancel_today_vote_no_vote(self, client, user):
        client.force_authenticate(user=user)
        url = reverse('voting:cancel-today')
        
        response = client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_voting_history(self, client, user, menu):
        Vote.objects.create(user=user, menu=menu, date=timezone.now().date())
        
        client.force_authenticate(user=user)
        url = reverse('voting:my-history')
        
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
