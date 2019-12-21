import os
import hashlib

from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, HttpRequest, JsonResponse
from chordsite.env import M_BIT
# from chordsite.server import head
from chordsite import server
from chordsite.node import Node
from chordsite.util import local_ip
from chordsite.env import NUM_SLOTS

global head

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def index(request):
    return render(request, os.path.abspath(BASE_DIR + '/web/index.html'))

def create_ring(request):
    global head
    head = server.create_ring()
    response = JsonResponse({'error': None})
    return response

def print_ring(request):
    # log
    server.print_ring()
    response = JsonResponse({'error': None})
    return response

def get_all_finger(request):
    global head
    rs= server.get_all_finger(head)
    response = JsonResponse({'error': None, 'shape': rs, 'm': M_BIT})
    return response

def list_dir(request):
    content = os.listdir('/home/c/ds_team_proj_chord')
    print('content: ', content)
    response = JsonResponse({'error': None, 'content': content})
    return response

def save_file(request):
    content = request.GET.get('content')
    filename = request.GET.get('filename')

    id = get_file_id(filename)

    f = open(filename, 'w+')
    print('content: ', content)
    f.write(content)
    f.close()

    node = head.find_successor(id)
    node.save_file(filename, content)
    return JsonResponse({'error': None})

def get_file(request):
    filename = request.GET.get('filename')

    f = open(filename, 'r')
    content = f.read()
    f.close()

    return JsonResponse({'error': None, 'content': content})

def get_file_id(filename):
    f = open(filename, 'rb')
    content = f.read()
    f.close()
    id = int(hashlib.md5(content).hexdigest(), 16) % NUM_SLOTS

    if not_in_file_mapping(filename):
        f.open('file_mapping', 'w+')
        entry = str(filename) + str(id)
        f.write(entry)
        f.close()

    return id

def add_node(request):
    ip = request.GET.get('ip')
    rs = server.add_node(ip)
    response = JsonResponse({'error': None, 'shape': rs})
    return response

def not_in_file_mapping(filename):
    f = open(filename, 'rb')
    content = f.read()
    if filename not in content:
        return True
    return False

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