from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CommentFilm)
admin.site.register(LikeFilm)
admin.site.register(LikeComment)
admin.site.register(RatingFilm)
admin.site.register(FavoriteFilm)