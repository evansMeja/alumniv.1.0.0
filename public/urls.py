from django.urls import path
from .views import *

urlpatterns = [
    path("",index, name='index'),
    path("register",register, name='register'),
    path("login",Login, name='login'),
    path("register_api",register_api,name="register_api"),
    path("login_api",login_api,name='login_api'),
    path('logout',Logout,name="logout")
]
