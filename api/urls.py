from django.urls import path
from .views import get_problem, create_problem

urlpatterns = [
    path('problem/<slug:title_slug>/', get_problem, name='get_problem'),
    path('problem/create/<slug:title_slug>/', create_problem, name='create_problem'),
]
