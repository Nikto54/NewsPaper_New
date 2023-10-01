from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import BaseRegisterView, upgrade_me

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name = '../templates/Login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = '../templates/Logout.html'),
         name='logout'),
    path('signup/',BaseRegisterView.as_view(template_name='../templates/Signup.html'),name='signup'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]