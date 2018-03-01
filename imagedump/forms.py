import os
from django import forms
from .models import Image
from django.core.exceptions import ValidationError


class ImageForm(forms.ModelForm):
    ''' Default form for an Image model '''

    class Meta:
        model = Image
        fields = ['title', 'image']

    def clean_image(self):
        image = self.cleaned_data['image']
        ext = os.path.splitext(image.name)[1]
        if not ext:
            raise ValidationError("This file name lacks an image extension")
        return image
