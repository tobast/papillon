from django.db import models
from django.conf import settings


class PapillonUser(models.Model):
    ''' User model overlay, for future features '''
    django_user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       primary_key=True)
