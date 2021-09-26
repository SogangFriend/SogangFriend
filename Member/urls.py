
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
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout),

    path('password_reset_confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('password_reset/', UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    #path('<str:username>/', people, name="people"),
    path('activate/<str:uid64>/<str:token>/', activate, name='activate'),
    path(r'^profile/(?P<pk>[0-9]+)/$',ProfileView.as_view(), name='profile')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


