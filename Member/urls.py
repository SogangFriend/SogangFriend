
from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path

from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView



urlpatterns = [
   path('register/', RegisterView.as_view()),
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', logout),
   path("f",MyPasswordResetView.as_view(), name="password_reset"),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='member/password_reset_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', change_pw, name='change_pw'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='member/password_reset_complete.html'), name='password_reset_complete'),
]
