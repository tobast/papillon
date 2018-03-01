from django.views.generic import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.utils import timezone

from papillon_user.models import get_papillon_user
from .forms import ImageForm


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
        partial_form = kwargs['partial_form']

        context = super().get_context_data(**kwargs)
        if partial_form:
            context['upload_form'] = partial_form
        else:
            context['upload_form'] = ImageForm()
        return context
