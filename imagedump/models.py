import uuid
import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from papillon_user.models import PapillonUser


def image_save_location(instance, filename):
    del filename  # Unused, we use the uuid instead
    return os.path.join(settings.UPLOAD_DIR, str(instance.uuid))


class Image(models.Model):
    # Unique identifier of the image, used in URLs
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)

    # On-disk path of the image
    image = models.ImageField(upload_to=image_save_location)

    # Displayed title
    title = models.CharField(max_length=512)

    # Image's uploader (or null)
    uploader = models.ForeignKey(PapillonUser,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    # Upload date of the image
    upload_date = models.DateTimeField()

    def raw_url(self, ext):
        ''' Get the image's raw display url '''
        return reverse('raw_image', kwargs={
            'uuid': str(self.uuid),
            'ext': ext,
        })

    def show_url(self, ext):
        ''' Get the image's decorated display url '''
        return reverse('show_image', kwargs={
            'uuid': str(self.uuid),
            'ext': ext,
        })
