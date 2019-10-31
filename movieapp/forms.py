from django.forms import ModelForm,DateInput,HiddenInput,ChoiceField
from django import forms
from .models import MotionPicture,Review,Artist,List,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MotionPictureForm(ModelForm):
    movie_choices = [('Action','Action'),('Adventure','Adventure'),('History','History'),('Drama','Drama'),('Romance','Romance'),('Documentary','Documentary')]
    genre = ChoiceField(choices=movie_choices)


    class Meta():
        model = MotionPicture
        fields = ['name','genre','release_date','description','image']
        widgets = {
             'release_date': DateInput(attrs={'type':'date'}),
         }

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    class Meta():
        model = User
        fields = ['username','email','first_name','last_name']


class MovieReviewForm(ModelForm):
    class Meta():
        model = Review
        fields = ['review']

class ArtistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ArtistForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['image'].required = False

    artist_choices = [('Actor','Actor'),('Director','Director')]
    artist_type = ChoiceField(choices=artist_choices)
    class Meta():
        model = Artist
        fields = ['name','birthday','artist_type','description','image']
        widgets = {
             'birthday': DateInput(attrs={'type':'date'}),
             
         }

class ArtistEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ArtistEditForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['image'].required = False
        self.fields['artist_type'].required = False

    artist_choices = [('Actor','Actor'),('Director','Director')]
    artist_type = ChoiceField(choices=artist_choices)
    class Meta():
        model = Artist
        fields = ['name','birthday','artist_type','description','image']
        widgets = {
             'birthday': DateInput(attrs={'type':'date'}),
             
         }


class ListForm(ModelForm):
    class Meta():
        model = List
        fields = ['name']

