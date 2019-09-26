from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MotionPicture(models.Model):
    movie_id = models.AutoField(primary_key=True)
    mp_type = models.CharField(max_length=15,default='Movie')
    name = models.CharField(max_length=140)
    genre = models.CharField(max_length=15)
    release_date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None)
    approved = models.BooleanField(default=False)

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_type = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    movies = models.ManyToManyField(MotionPicture)                                                                                                                                                                                                                              