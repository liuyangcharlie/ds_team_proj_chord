from django.shortcuts import render
import os
from rest_framework.views import APIView
from django.http import HttpResponse, HttpRequest, JsonResponse
from . import server
from .env import M_BIT
from .server import ring

# Create your views here.
def index(request):
    return render(request, 'index.html')

def creat_ring(request):
    global ring
    ring = server.create_ring()
    response = JsonResponse({'error': None})
    return response
    # return render(request, 'index.html')

def print_ring(request):
    # log 
    server.print_ring()
    response = JsonResponse({'error': None})
    return response
    # return render(request, 'index.html')

def get_all_finger(request):
    global ring
    rs= server.get_all_finger()
    response = JsonResponse({'error': None, 'shape': rs, 'm': M_BIT})
    return response
    # return render(request, 'index.html')

def add_node(request):
    ip = request.GET.get('ip')
    rs = server.add_node(ip)
    response = JsonResponse({'error': None, 'shape': rs})
    return response
    # return render(request, 'index.html')

def lookup(request):
    key = request.GET.get('key')
    id = request.GET.get('id')
    target = server.lookup(key, id)
    response = JsonResponse({'error': None, 'target': target})
    return response

def remove_node(request):
    id = request.GET.get('id')
    s = server.remove_node(id)
    response = JsonResponse({'error': None, 'shape': s})
    return response

class Chord(APIView):
    # initialize
    def get(self, request, *args, **kwargs):
        creat_ring(request)
        print_ring(request)
        return index(request)
    
    # def creat_chord(self, request):
    #     return creatring(request)