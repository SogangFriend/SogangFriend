
from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path

from .views import *
from django.contrib.auth import views as auth_views, views
from django.views.generic.base import TemplateView

from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name ='Member'

urlpatterns = [
    path('new/', RegisterView.as_view(), name='new'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', log_out),

    path('password/', PasswordResetView.as_view(), name='password'),

    path('activate/<str:uid64>/<str:token>/', activate, name='activate'),

    path('profile/', ProfileView.as_view(), name='profile'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


