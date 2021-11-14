from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MainApp.urls')),
    path('member/', include('Member.urls', namespace='Member')),
    path('Chat/', include('Chat.urls', namespace='Chat')),
]
