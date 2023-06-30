from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from.models import *

# Create your views here.
class HomeView(ListView):
    queryset = User.objects.all()
    template_name = 'index.html'
    context_object_name = 'users'
