from django.urls import path, include

from .views import *
from Member import views

urlpatterns = [
    path('', HomeView.as_view()),
]
