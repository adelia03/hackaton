from django.contrib import admin

from .models import Film
from review.models import *

class RatingInLIne(admin.TabularInline):
    model = Rating

class CommentInLine(admin.TabularInline):
    model = Comment

class FilmAdmin(admin.ModelAdmin):
    list_display= ['title', 'genre',]
    list_filter = ['genre','favourites',]
    search_fields = ['title',]
    inlines = [CommentInLine]

admin.site.register(Film, FilmAdmin)