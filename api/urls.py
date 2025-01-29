from django.urls import path
from .views import get_problem, create_problem

urlpatterns = [
    path('problem/', get_problem, name='get_problem'),
    path('problem/create', create_problem, name='create_problem'),
]
