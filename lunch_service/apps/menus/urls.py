from django.urls import path
from . import views

app_name = 'menus'

urlpatterns = [
    path('', views.MenuListCreateView.as_view(), name='list-create'),
    path('<int:pk>/', views.MenuDetailView.as_view(), name='detail'),
    path('today/', views.today_menu_view, name='today'),
    path('restaurant/<int:restaurant_id>/today/', views.restaurant_today_menu_view, name='restaurant-today'),
    path('<int:menu_id>/items/', views.MenuItemListCreateView.as_view(), name='items-list-create'),
    path('<int:menu_id>/items/<int:pk>/', views.MenuItemDetailView.as_view(), name='item-detail'),
]
