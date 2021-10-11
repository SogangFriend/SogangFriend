from django.urls import path, include

from .views import *
from Member import views

app_name ='Main'

urlpatterns = [
    path('', HomeView.as_view(), name="homepage"),
    path('members/', MemberListView.as_view()),
]
