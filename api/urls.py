from django.urls import path
from .views import problem

urlpatterns = [
    path('problem/<slug:title_slug>/', problem, name='problem'),
]
