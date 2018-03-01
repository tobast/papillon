from django.contrib import admin
from .models import PapillonUser


@admin.register(PapillonUser)
class PapillonUserAdmin(admin.ModelAdmin):
    pass
