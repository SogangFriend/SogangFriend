# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('SogangFriend/', include('Member.urls')),  # new
    path('SogangFriend/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
