from django.urls import path
from . import views

urlpatterns = [
    path("", views.explore_universities, name="explore_universities"),
]