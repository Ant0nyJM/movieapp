from django.forms import ModelForm,DateInput,HiddenInput
from django import forms
from .models import MotionPicture,Review,Artist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dal import autocomplete

class MotionPictureForm(ModelForm):
    class Meta():
        model = MotionPicture
        fields = ['name','genre','release_date','description','image']
        widgets = {
             'release_date': DateInput(attrs={'type':'date'}),
         }


class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','email']


class MovieReviewForm(ModelForm):
    class Meta():
        model = Review
        fields = ['review']

class ArtistSearchForm(ModelForm):
    class Meta():
        model = Artist
        fields = ['name']




