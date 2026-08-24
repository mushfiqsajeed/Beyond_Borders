from django.urls import path
from . import views

urlpatterns = [
    path("", views.saved_home, name="saved_home"),
    path("universities/", views.saved_universities, name="saved_universities"),
    path("universities/toggle/", views.toggle_saved_university, name="toggle_saved_university"),
    path("scholarships/", views.saved_scholarships, name="saved_scholarships"),
    path("scholarships/toggle/", views.toggle_saved_scholarship, name="toggle_saved_scholarship"),
]