from django.urls import path
from .views import *

urlpatterns = [
    path("",admin_dashboard, name='admin_dashboard'),
    path("manage_users",manage_users,name="manage_users"),
    path("delete_alumni_api",delete_alumni_api,name="delete_alumni_api"),
    path("post_info",post_info,name='post_info'),
    path("post_info_api",post_info_api,name='post_info_api'),
    path("post_event_api",post_event_api,name="post_event_api"),
    path("post_event",post_event,name="post_event"),
    path("register_alumni_api",register_alumni_api,name="register_alumni_api"),
    path("register_alumni",register_alumni,name="register_alumni"),
]
