from rest_framework.serializers import ModelSerializer

from .models import Film
from review.serializers import *

class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
    
    def to_representation(self, instance:Film):
        rep = super().to_representation(instance)
    #     rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
    #     rep['comment_likes'] = LikeCommentSerializer(instance.likes).data
        rep['rating'] = instance.average_rating
    #     rep['favourite'] = instance.favourites.count()
    #     rep['film_likes'] = instance.likes.count()
    #     return rep