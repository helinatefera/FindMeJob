from django.db import models
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User = get_user_model()
# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=True)
    id_user= models.IntegerField()
    name= models.CharField(max_length=200,blank=True)
    email = models.CharField(max_length=200,blank=True)
    main_location = models.CharField(max_length=200,blank=True)
    description = models.CharField(max_length=1000,blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png',blank=True)

    def __str__(self):
        return self.user.username

class Job(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_applay = models.IntegerField(default=0)

    def __str__(self):
        return self.user