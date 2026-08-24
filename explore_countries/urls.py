from django.urls import path
from . import views

urlpatterns = [
    path("", views.explore_countries, name="explore_countries"),

    path(
        "country/<str:country_name>/",
        views.country_detail,
        name="country_detail"
    ),
]