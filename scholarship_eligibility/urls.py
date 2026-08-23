from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.scholarship_eligibility,
        name="scholarship_eligibility"
    ),
]