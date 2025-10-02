from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.EmployeeListCreateView.as_view(), name='list-create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='detail'),
    path('search/', views.search_employees_view, name='search'),
    path('my-profile/', views.my_profile_view, name='my-profile'),
]
