from django.urls import path

from cars import views

app_name = "cars"
urlpatterns = [
    path('cars/', views.CarListView.as_view(), name="list_cars"),
    path('popular/', views.PopularListView.as_view(), name="list_popular"),
]
