from django.contrib import admin

from .models import Film
from review.models import *


class FilmAdmin(admin.ModelAdmin):
    list_display= ['title', 'genre',]
    list_filter = ['genre','favourites',]
    search_fields = ['title',]

admin.site.register(Film, FilmAdmin)