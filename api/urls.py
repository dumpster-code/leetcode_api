from django.urls import path
from . import views

urlpatterns = [
    path('problem/', views.get_query, name='get_query'),
    path('problem/daily/', views.get_daily_problem, name='get_daily_problem'),
    path('problem/<slug:title_slug>/', views.get_problem, name='get_problem'),
    path('problem/create/<slug:title_slug>/', views.create_problem, name='create_problem'),
    path('problem/delete/<slug:title_slug>/', views.delete_problem, name='delete_problem'),
]
