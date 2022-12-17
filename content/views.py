from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

def handler404(request):
    return HttpResponseNotFound('<h1>500 Internal server error</h1>')
    
# Create your views here.
