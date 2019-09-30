from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.


class MotionPicture(models.Model):
    def __str__(self):
        return self.name
    movie_id = models.AutoField(primary_key=True)
    mp_type = models.CharField(max_length=15,default='Movie')
    name = models.CharField(max_length=140)
    genre = models.CharField(max_length=15)
    release_date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None)
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')

class Artist(models.Model):
    def __str__(self):
        return self.name
    artist_id = models.AutoField(primary_key=True)
    artist_type = models.CharField(max_length=15,default="Actor")
    name = models.CharField(max_length=50,null=False)
    description = models.TextField(default="")
    image = models.ImageField()
    movies = models.ManyToManyField(MotionPicture)   

class Rate(models.Model):
    def __str__(self):
        return str(self.user.username+" for "+self.movie.name)
    rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    movie = models.OneToOneField(MotionPicture,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
