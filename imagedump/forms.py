from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    ''' Default form for an Image model '''

    class Meta:
        model = Image
        fields = ['title', 'image']
