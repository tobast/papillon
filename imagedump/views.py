from django.shortcuts import render
from django.views.generic import TemplateView


class UploadImageView(TemplateView):
    ''' Image upload page view '''
    template_name = 'imagedump/upload_image.html'
