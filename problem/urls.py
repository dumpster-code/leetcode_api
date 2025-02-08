from django.urls import path
from .views import (
    problem_query,
    problem_detail,
    problem_random,
    problem_create,
    # problem_update,
    # problem_delete,
)

urlpatterns = [
    path('', problem_query, name='problem-query'),
    path('random', problem_random, name='problem-random'),
    path('<slug:slug>', problem_detail, name='problem-detail'),
    path('create', problem_create, name='problem-create'),
    path('daily', problem_create, name='problem-create'),
]
