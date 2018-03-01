from django.db import models
from papillon_user.models import PapillonUser


class Image(models.Model):
    path = models.CharField(max_length=1024,
                            unique=True)
    uploader = models.ForeignKey(PapillonUser,
                                 on_delete=models.SET_NULL,
                                 null=True)
    upload_date = models.DateTimeField()
