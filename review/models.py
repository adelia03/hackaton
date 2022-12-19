from django.db import models

from main.models import Film
from account.models import User

# Create your models here.

class CommentFilm(models.Model):
    film = models.ForeignKey(Film, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='film_comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.author} -> {self.film}'


class LikeComment(models.Model):
    author = models.ForeignKey(User,  related_name='comment_likes', on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentFilm, related_name='likes', on_delete=models.CASCADE)



class RatingFilm(models.Model):
    film = models.ForeignKey(Film, related_name='ratings', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])

    def __str__(self):
        return f'{self.author}->{self.film}'


class FavoriteFilm(models.Model):
    author = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    film = models.ForeignKey(Film, related_name='favorites', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}_>{self.film}'


class LikeFilm(models.Model):
    author = models.ForeignKey(User,related_name='film_likes', on_delete=models.CASCADE)
    film = models.ForeignKey(Film,related_name='likes',on_delete=models.CASCADE)
