from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

# from .views import ()

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='papillon_user/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='papillon_user/logout.html'),
         name='logout'),
]
