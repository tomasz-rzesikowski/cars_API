from django.urls import path, include
from rest_framework import routers

from cars import views

app_name = "cars"

urlpatterns = [
    path('cars/', views.CarListCreateView.as_view(), name="cars"),
    path('popular/', views.PopularListView.as_view(), name="list_popular"),
]

