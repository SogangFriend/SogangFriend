from django.urls import path
from .views import *

app_name='Member'

urlpatterns = [
   path('register/', RegisterView.as_view()),
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', logout),
   path('activate/<str:uid64>/<str:token>/', activate, name='activate'),
]
