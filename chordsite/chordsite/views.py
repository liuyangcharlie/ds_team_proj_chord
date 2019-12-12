from django.shortcuts import render
import os
from rest_framework.views import APIView
from django.http import HttpResponse, HttpRequest
from . import server

# Create your views here.
def index(request):
    return render(request, 'index.html')

def creat_ring(request):
    server.create_ring()
    # response = HttpResponse()
    # response['content_type'] = 'application/json; charset=utf-8'
    return HttpResponse(render(request, 'index.html'), content_type='application/json; charset=utf-8')

def print_ring(request):
    server.print_ring()
    response = HttpResponse()
    response['content_type'] = 'application/json; charset=utf-8'
    {'error': None}

class Chord(APIView):
    def get(self, request, *args, **kwargs):
        return index(request)
    
    # def creat_chord(self, request):
    #     return creatring(request)