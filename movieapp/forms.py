from django.forms import ModelForm,DateInput,HiddenInput,ChoiceField,EmailField
from django import forms
from .models import MotionPicture,Review,Artist,List
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User


class MotionPictureForm(ModelForm):
    choices = (('Horror','Horror'),('Comedy','Comedy'),('Action','Action'),('Drama','Drama'),('Adventure','Adventure'),('Documentary','Documentary'))
    genre = ChoiceField(choices=choices)
    class Meta():
        model = MotionPicture
        fields = ['name','genre','release_date','description','image']
        widgets = {
             'release_date': DateInput(attrs={'type':'date'}),
         }

class CustomUserCreationForm(UserCreationForm):
    email = EmailField(required=True)
    class Meta():
        model = User
        fields = ['username','email']


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

    choices = (('Actor','Actor'),('Director','Director'))
    artist_type = ChoiceField(choices=choices)
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


class NewUserChangeForm(UserChangeForm):
    class Meta():
        model = User
        fields = ['first_name','last_name','email']

