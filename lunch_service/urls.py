from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('lunch_service.apps.authentication.urls')),
    path('api/v1/restaurants/', include('lunch_service.apps.restaurants.urls')),
    path('api/v1/employees/', include('lunch_service.apps.employees.urls')),
    path('api/v1/menus/', include('lunch_service.apps.menus.urls')),
    path('api/v1/voting/', include('lunch_service.apps.voting.urls')),
    path('api/v2/auth/', include('lunch_service.apps.authentication.urls')),
    path('api/v2/restaurants/', include('lunch_service.apps.restaurants.urls')),
    path('api/v2/employees/', include('lunch_service.apps.employees.urls')),
    path('api/v2/menus/', include('lunch_service.apps.menus.urls')),
    path('api/v2/voting/', include('lunch_service.apps.voting.urls')),
    # JWT Token endpoints
]
