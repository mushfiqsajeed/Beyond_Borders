from django.urls import path
from . import views

urlpatterns = [
    path('cost-estimator/', views.cost_estimator, name='cost_estimator'),
]