from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid
User=get_user_model()
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField
    bio =models.TextField(blank=True)
    profileimg=models.ImageField(upload_to='profile_img',default="blank.jpeg")
    location=models.CharField(max_length=100,blank=True)
    def __str__(self) :
        return self.user.username
class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=50)
    image=models.ImageField(upload_to='post')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self) :
        return self.user   
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.username
class followercount(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    def __str__(self) :
        return self.follower