from django.urls import path
from . import views

urlpatterns = [
    path('document-review/', views.document_review, name='document_review'),
]