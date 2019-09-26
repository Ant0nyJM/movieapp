from django.forms import ModelForm,DateInput
from .models import MotionPicture

class MotionPictureForm(ModelForm):
    class Meta():
        model = MotionPicture
        fields = ['name','genre','release_date','description']
        widgets = {
             'release_date': DateInput(attrs={'type':'date'}),
         }