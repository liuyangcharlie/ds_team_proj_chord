import os

from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, HttpRequest, JsonResponse
from chordsite.env import M_BIT
# from chordsite.server import head
from chordsite import server
from chordsite.node import Node
from chordsite.util import local_ip

global head

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def index(request):
    return render(request, os.path.abspath(BASE_DIR + '/web/index.html'))

# def create_ring(request):
#     global head
#     head = server.create_ring()
#     response = JsonResponse({'error': None})
#     return response

# def print_ring(request):
#     # log
#     server.print_ring()
#     response = JsonResponse({'error': None})
#     return response

def get_all_finger(request):
    global head
    rs= server.get_all_finger(head)
    response = JsonResponse({'error': None, 'shape': rs, 'm': M_BIT})
    return response

# def add_node(request):
#     ip = request.GET.get('ip')
#     rs = server.add_node(ip)
#     response = JsonResponse({'error': None, 'shape': rs})
#     return response

# def lookup(request):
#     key = request.GET.get('key')
#     id = request.GET.get('id')
#     target = server.lookup(key, id)
#     response = JsonResponse({'error': None, 'target': target})
#     return response

# def remove_node(request):
#     id = request.GET.get('id')
#     s = server.remove_node(id)
#     response = JsonResponse({'error': None, 'shape': s})
#     return response

def set_head(n):
    global head
    head = n

class Chord(APIView):
    # initialize
    def get(self, request, *args, **kwargs):
        # create_ring(request)
        # print_ring(request)
        return index(request)

    # def creat_chord(self, request):
    #     return creatring(request)