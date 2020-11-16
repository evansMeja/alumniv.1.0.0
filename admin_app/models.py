from django.db import models
class posts(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    content = models.CharField(max_length=100,blank=True,null=True)
    picture =models.ImageField(upload_to='profile_pictures/',blank=True,null=True,default="default/anony.jpg")

class events(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    venue = models.CharField(max_length=100,blank=True,null=True)
    date =models.DateTimeField(auto_now_add=True)
