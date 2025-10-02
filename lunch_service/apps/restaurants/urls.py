from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.RestaurantListCreateView.as_view(), name='list-create'),
    path('<int:pk>/', views.RestaurantDetailView.as_view(), name='detail'),
    path('search/', views.search_restaurants_view, name='search'),
    path('available/', views.available_restaurants_view, name='available'),
]
