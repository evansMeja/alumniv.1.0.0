from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class story(models.Model):
    content = models.CharField(blank=True,null=True,max_length=100)
    story_file =models.FileField(upload_to='profile_pictures/',blank=True,null=True,default="default/anony.jpg")
    video_present = models.BooleanField(default=False)
    picture_present = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='like')
    hearts = models.ManyToManyField(User,related_name='heart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class comments(models.Model):
    content = models.TextField(blank=True,null=True,max_length=400)
    story = models.ForeignKey(story, on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class messages_table(models.Model):
    sender= models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender", default=1)
    receiver= models.ForeignKey(User, on_delete=models.CASCADE,related_name="receiver",default=1)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    content = models.CharField(blank=True,null=True, max_length=100)


class Notifications(models.Model):
    message = models.CharField(blank=True,null=True,max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class photo_gallery(models.Model):
    picture = models.ImageField(upload_to='profile_pictures/',blank=True,null=True,default="default/anony.jpg")
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)