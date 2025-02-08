from django.urls import path
from .views import (
    problem_detail,
    problem_query,
    problem_daily,
    problem_random,

    problem_create,
    # problem_update,
    # problem_delete,
)

urlpatterns = [
    path('daily', problem_daily, name='problem-daily'),
    path('random', problem_random, name='problem-random'),
    path('create', problem_create, name='problem-create'),

    path('', problem_query, name='problem-query'),
    path('<slug:slug>/', problem_detail, name='problem-detail'),
]
