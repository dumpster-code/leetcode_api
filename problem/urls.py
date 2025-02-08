from django.urls import path
from .views import (
    problem_detail,
    problem_create,
    # problem_update,
    # problem_delete,
)

urlpatterns = [
    path('<slug:slug>', problem_detail, name='problem-detail'),
    path('create', problem_create, name='problem-create')
]
