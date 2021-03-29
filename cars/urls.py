from django.urls import path

from cars import views

app_name = "cars"

urlpatterns = [
    path('cars/', views.CarListCreateView.as_view(), name="cars"),
    path('cars/<int:pk>/', views.CarDeleteView.as_view(), name="car_del"),
    path('popular/', views.PopularListView.as_view(), name="list_popular"),
    path('rate/', views.RateCreateView.as_view(), name="rate"),
]
