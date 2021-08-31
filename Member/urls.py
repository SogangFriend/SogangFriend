from django.urls import path

from . import views
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
   path('register/', RegisterView.as_view()),
   path('login/', LoginView.as_view(),name="login"),
   path('logout/', logout),
   path("password_reset", views.password_reset_request, name="password_reset"),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='member/password/password_reset_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', views.password_reset_request, name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='member/password/password_reset_complete.html'), name='password_reset_complete'),
   ]

