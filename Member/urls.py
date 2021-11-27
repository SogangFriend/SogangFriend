
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

    path('password/', PasswordResetView.as_view(), name='password'),

    path('activate/<str:uid64>/', activate, name='activate'),


    path('mypage/', MyPageView.as_view(), name='my_page'),
    path('mypage/password/', PasswordChangeView.as_view(), name='password_change'),

    path('mail/<str:email>/', RetryMailView.as_view(), name='retry'),

    # ajax 통신 url
    path('check/', name_overlap_check, name='check'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


