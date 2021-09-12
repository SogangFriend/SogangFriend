
from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path

from .views import *
from django.contrib.auth import views as auth_views, views
from django.views.generic.base import TemplateView
from django.urls import path
from . import views


urlpatterns = [
   path('register/', RegisterView.as_view()),
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', logout),
    path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
]