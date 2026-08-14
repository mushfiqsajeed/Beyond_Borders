from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup')
]
