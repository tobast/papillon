import uuid
import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from papillon_user.models import PapillonUser
from crypto.crypto import AESCipher


def image_save_location(instance, filename):
    ''' Get the image save path on disk of an image '''
    del filename  # Unused, we use the uuid instead
    return os.path.join(settings.UPLOAD_DIR, str(instance.uuid))


class Image(models.Model):
    ''' An uploaded image, with its metadata '''

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


class InaccessibleFile(Exception):
    ''' Raised when trying to read an inaccessible file

    Can be raised upon file not found, permission error, etc. '''

    def __init__(self, what):
        super().__init__()
        self.what = what

    def __str__(self):
        return self.what


class EncryptedFile(models.Model):
    ''' An encrypted file on the filesystem '''

    # The file's path on disk, relative to UPLOAD_DIR
    path = models.CharField(max_length=512)

    @property
    def disk_path(self):
        ''' On-disk path of the file '''
        return os.path.join(settings.UPLOAD_DIR, self.path)

    @property
    def raw_data(self):
        ''' Raw data for the file (encrypted) '''
        # TODO: caching?
        try:
            with open(self.disk_path, 'rb') as handle:
                data = handle.read()
        except FileNotFoundError:
            raise InaccessibleFile("File not found: {}".format(self.path))
        except PermissionError:
            raise InaccessibleFile("Permission error: {}".format(self.path))
        return data

    def data(self, key):
        ''' Decrypted data (server-side decryption) '''
        raw = self.raw_data
        cipher = AESCipher(key)
        return cipher.decrypt(raw)

    def raw_write(self, data):
        ''' Write raw, pre-encrypted data to the file (truncating it) '''
        try:
            with open(self.disk_path, 'wb') as handle:
                handle.write(data)
        except PermissionError:
            raise InaccessibleFile("Permission error: {}".format(self.path))

    def write(self, data, key):
        ''' Write data to the file (truncating it), encrypting it with the
        provided key '''
        cipher = AESCipher(key)
        raw = cipher.encrypt(data)
        self.raw_write(raw)
