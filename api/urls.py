from django.urls import path
from .views import get_problem, get_query, create_problem

urlpatterns = [
    path('problem/', get_query, name='get_query'),
    path('problem/<slug:title_slug>/', get_problem, name='get_problem'),
    path('problem/create/<slug:title_slug>/', create_problem, name='create_problem'),
]
