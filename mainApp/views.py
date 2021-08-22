from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import *
from .forms import *
# Create your views here.

# 컨트롤러 역할


class HomeView(FormView):
    form_class = TestForm
    template_name = 'home.html'
