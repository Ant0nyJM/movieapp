from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class MovieappBaseModel(models.Model):

    created_date_time = models.DateTimeField(auto_now_add=True)
    modified_date_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MotionPicture(MovieappBaseModel):

    # movie_id = models.AutoField(primary_key=True, unique=True)
    mp_type = models.CharField(max_length=15, default='Movie')
    name = models.CharField(max_length=140, db_index=True)
    genre = models.CharField(max_length=15)
    release_date = models.DateField(default=timezone.now().date())
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.00)
    movie_id = models.SlugField(primary_key=True,unique=True)

    def __str__(self):
        return self.name
    def get_director(self):
        artist = self.artist_set.get(artist_type='Director')
        return artist.name
    get_director.short_description = 'Director'



class Artist(MovieappBaseModel):

    # artist_id = models.AutoField(primary_key=True, unique=True)
    artist_type = models.CharField(max_length=15, default="Actor")
    name = models.CharField(max_length=50, null=False, db_index=True)
    birthday = models.DateField(null=False, default=None)
    description = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    image = models.ImageField(upload_to='images/')
    movies = models.ManyToManyField(MotionPicture)
    approved = models.BooleanField(default=False)  
    artist_id = models.SlugField(primary_key=True,unique=True)

    def __str__(self):
        return self.name


     

class Rate(MovieappBaseModel):

    rating = models.DecimalField(max_digits=3, decimal_places=1)
    movie = models.ForeignKey(MotionPicture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.user.username+" for "+self.movie.name)
    

class Review(MovieappBaseModel):

    review = models.TextField()
    movie = models.ForeignKey(MotionPicture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str("Review by "+self.user.username+" for "+self.movie.name)
    



class List(MovieappBaseModel):

    name = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(MotionPicture)

    def __str__(self):
        return str(self.name)
    