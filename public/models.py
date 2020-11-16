from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import unique_slug_generator

class courses(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    def __str(self):
        return str(self.name)

class field(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    course = models.ForeignKey(courses,on_delete=models.CASCADE,default=1)

    def __str(self):
        return str(self.name)


class alumnae_registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug  = models.SlugField(blank=True)
    followers = models.ManyToManyField(User,related_name='follower')
    phone = models.CharField(max_length=14,blank=True,null=True)
    field = models.ForeignKey(field,on_delete=models.CASCADE,default=1)
    picture =models.ImageField(upload_to='profile_pictures/',blank=True,null=True,default="default/anony.jpg")
    about = models.TextField(max_length=14,blank=True,null=True)

