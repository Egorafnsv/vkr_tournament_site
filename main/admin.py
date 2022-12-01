from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Tournament)
admin.site.register(models.Clubs)
admin.site.register(models.Players)
admin.site.register(models.Tables)
admin.site.register(models.Matches)
admin.site.register(models.Playoff_scheme)
