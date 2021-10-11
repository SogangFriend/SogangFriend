from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainApp.urls', namespace='Main')),
    path('member/', include('Member.urls', namespace='Member')),
    path('chat/', include('chat.urls', namespace='Chat')),

]
