from django.urls import path, include

from .views import *
from Member.views import LoginView, log_out

urlpatterns = [
    path('', HomeView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', log_out),
]
