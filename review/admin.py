
from django.contrib import admin 
from django.contrib import admin

from .models import *

admin.site.register(Comment)
admin.site.register(LikeComment)
admin.site.register(LikeFilm)
admin.site.register(Rating)
admin.site.register(Favourite)

