from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('', views.VoteListCreateView.as_view(), name='list-create'),
    path('<int:pk>/', views.VoteDetailView.as_view(), name='detail'),
    path('vote/<int:menu_id>/', views.vote_for_restaurant_view, name='vote-restaurant'),
    path('today/', views.today_vote_view, name='today-vote'),
    path('results/today/', views.today_results_view, name='today-results'),
    path('results/<str:date>/', views.results_for_date_view, name='results-date'),
    path('my-history/', views.my_voting_history_view, name='my-history'),
    path('cancel-today/', views.cancel_today_vote_view, name='cancel-today'),
]
