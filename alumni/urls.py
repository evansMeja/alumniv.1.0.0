from django.urls import path
from .views import *

urlpatterns = [
    path("",alumni_dashboard, name='alumni_dashboard'),
    path("post_story",post_story, name='post_story'),
    path("alumni/<slug:slug>",alumni_detail,name="alumni_detail"),
    path('send_message',send_message,name="send_message"),
    path("follow",follow,name='follow'),
    path("following",following,name='following'),
    path('follow_api',follow_api,name='follow_api'),
    path("unfollow_api",unfollow_api,name='unfollow_api'),
    path("followers",followers,name="followers"),
    path("profile",profile,name="profile"),
    path("fetch_fields_api",fetch_fields_api,name="fetch_fields_api"),
    path("update_profile_api",update_profile_api,name="update_profile_api"),
    path("alumni_public/<slug:slug>",alumni_public,name="alumni_public"),
    path("save_mood",save_mood,name="save_mood"),
    path("all_feeds",all_feeds,name="all_feeds"),
    path("user_profile/<slug:slug>",user_profile,name="user_profile"),
    path("following_friends/<slug:slug>",following_friends,name="following_friends"),
    path("connect_friends/<slug:slug>",connect_friends,name="connect_friends"),
    path("folowers_friends/<slug:slug>",folowers_friends,name="folowers_friends"),
    path("gallery",gallery,name="gallery"),
    path("add_photo_to_gallery",add_photo_to_gallery,name="add_photo_to_gallery"),
    path("my_photos/<slug:slug>",my_photos,name="my_photos"),
    path("about/<slug:slug>",about,name="about"),
    path("like_post",like_post,name="like_post"),
    path("heart_post",heart_post,name="heart_post"),
    path("fetch_comments_endpoint",fetch_comments_endpoint,name="fetch_comments_endpoint"),
    path('new_comment',new_comment,name='new_comment'),
    path('notification_endpoint',notification_endpoint,name='notification_endpoint')
]
