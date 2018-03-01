from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class PapillonUser(models.Model):
    ''' User model overlay, for future features '''
    django_user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       primary_key=True)

    def __str__(self):
        return str(self.django_user)


def get_papillon_user(user):
    if not user.is_authenticated:
        return None
    else:
        try:
            return user.papillonuser
        except ObjectDoesNotExist:
            return None  # No papillon user associated
