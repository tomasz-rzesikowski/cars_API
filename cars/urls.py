from django.urls import path, include
from rest_framework import routers

from cars import views

router = routers.SimpleRouter()
router.register(r"cars", views.CarListCreateView)

app_name = "cars"

urlpatterns = [
    path('cars/', views.CarListCreateView.as_view(), name="cars"),
    # path("", include(router.urls)),
    path('popular/', views.PopularListView.as_view(), name="list_popular"),
]

