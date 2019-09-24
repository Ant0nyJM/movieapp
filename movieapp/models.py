from django.db import models

# Create your models here.
class MotionPicture(models.Model):
    movie_id = models.AutoField(primary_key=True)
    mp_type = models.CharField(max_length=15)
    name = models.CharField(max_length=140)
    genre = models.CharField(max_length=15)
    release_date = models.DateField()
    description = models.TextField()

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_type = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    movies = models.ManyToManyField(MotionPicture)                                                                                                                                                                                                                              