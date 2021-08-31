from django.urls import path
from .views import *
from . import views

app_name = "mainApp"

urlpatterns = [
    path('', HomeView.as_view()),
]