from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#Request -> response

def hello (request):
    return render (request, 'homepage.html') 