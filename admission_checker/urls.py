from django.urls import path
from . import views

urlpatterns = [
    path('admission-checker/', views.admission_checker, name='admission_checker'),
]