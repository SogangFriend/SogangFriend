from django.urls import path
from . import views


urlpatterns = [
   path('register/request/', views.MailView.as_view()),
   path('register/', views.register),
   path('login/', views.login),
   path('logout/', views.logout),
]
