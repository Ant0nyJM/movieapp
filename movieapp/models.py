from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
from django.utils import timezone

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
    image = models.ImageField(upload_to='images/',blank=True)
    rating = models.DecimalField(max_digits=3,decimal_places=1,default=0.00)

class Artist(models.Model):
    def __str__(self):
        return self.name
    artist_id = models.AutoField(primary_key=True)
    artist_type = models.CharField(max_length=15,default="Actor")
    name = models.CharField(max_length=50,null=False)
    birthday = models.DateField(null=False,default=timezone.now().date())
    description = models.TextField(default="")
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None)
    image = models.ImageField(upload_to='images/')
    movies = models.ManyToManyField(MotionPicture)
    approved = models.BooleanField(default=False)   

class Rate(models.Model):
    def __str__(self):
        return str(self.user.username+" for "+self.movie.name)
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    movie = models.ForeignKey(MotionPicture,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Review(models.Model):
    def __str__(self):
        return str("Review by "+self.user.username+" for "+self.movie.name)
    review = models.TextField()
    movie = models.ForeignKey(MotionPicture,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)



class List(models.Model):
    def __str__(self):
        return str(self.name)
    name = models.CharField(max_length=40)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movies = models.ManyToManyField(MotionPicture)
