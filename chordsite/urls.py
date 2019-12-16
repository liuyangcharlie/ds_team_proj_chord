"""chordsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from chordsite.views import Chord
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Chord.as_view()),
    path('admin/', admin.site.urls),
    path('create_ring/', views.create_ring),
    path('get_all_finger/', views.get_all_finger),
    path('add_node/', views.add_node),
    path('lookup/', views.lookup),
    path('remove_node/', views.remove_node),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
