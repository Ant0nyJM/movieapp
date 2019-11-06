from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ChoiceField, DateInput, HiddenInput, ModelForm
from django.utils.translation import gettext as _
from .models import Artist, List, MotionPicture, Review


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



        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        

    class Meta():
        model = User
        fields = ['username','email','first_name','last_name']

    def clean_email(self):
        users = User.objects.all().only('email')
        emails = [x.email for x in users]
        entered_email = self.cleaned_data['email']
        if entered_email in emails:
            raise ValidationError(_('This email is already in use by a user.'),code='existing-email')
        return entered_email


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



    # def clean_name(self):
    #     data = self.cleaned_data['name']
    #     existing_names = Artist.objects.all().only('name')
    #     if data in existing_names:
    #         raise forms.ValidationError(_('A movie with this name already exists.'))
    #     return data

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
