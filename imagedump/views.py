import mimetypes
import os

from django.conf import settings
from django.views.generic import View, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.utils import timezone
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404

from papillon_user.models import get_papillon_user
from .forms import ImageForm
from .models import Image


class UploadImageView(ContextMixin, TemplateResponseMixin, View):
    ''' Image upload page view '''
    template_name = 'imagedump/upload_image.html'

    def post(self, request):
        ''' Answer to POST requests '''
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = get_papillon_user(request.user)
            image.upload_date = timezone.now()
            image.full_clean()
            # ^ Will fail with 500 upon error -- this is what we want here
            image.save()

            # TODO redirect to image view
            return self.render_to_response(self.get_context_data())

        # ...upon error, show the form again (with errors)
        return self.render_to_response(
            self.get_context_data(partial_form=form))

    def get(self, request):
        del request
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            partial_form = kwargs['partial_form']
        except KeyError:
            partial_form = None

        if partial_form:
            context['upload_form'] = partial_form
        else:
            context['upload_form'] = ImageForm()
        return context


class ShowImageView(TemplateView):
    ''' Show an image and its metadata '''
    template_name = 'imagedump/show_image.html'

    def get_context_data(self, uuid, ext, **kwargs):
        context = super().get_context_data(**kwargs)
        image = get_object_or_404(Image, uuid=uuid)

        context['image'] = image
        context['raw_url'] = image.raw_url(ext)

        return context


class ServeImageView(View):
    ''' Serve a stored image

    This is served by Django, even though this is Bad for performance reasons,
    yet the decryption has to happen in Django '''

    def get(self, request, uuid, ext):
        image = get_object_or_404(Image, uuid=uuid)

        mimetype = mimetypes.guess_type('placeholder.{}'.format(ext))[0]
        if mimetype is None:
            mimetype = 'application/octet-stream'
        else:
            if not mimetype.startswith('image/'):
                raise Http404

        disk_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
        try:
            resp = FileResponse(open(disk_path, 'rb'))
            resp['Content-Type'] = mimetype
            return resp
        except FileNotFoundError:
            raise Http404
        except PermissionError:
            raise Http404
