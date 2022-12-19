from rest_framework.serializers import ModelSerializer

from .models import CommentFilm, RatingFilm, FavoriteFilm, LikeFilm , LikeComment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = CommentFilm
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = instance.author.username
        rep['likes'] = instance.likes.count()
        del rep['film']
        return rep


class RatingSerializer(ModelSerializer):
    class Meta:
        model = RatingFilm
        fields = '__all__'

    
class FavoriteSerializer(ModelSerializer):
    model = FavoriteFilm
    fields = '__all__'


class LikeSerialzier(ModelSerializer):
    model = LikeFilm
    fields = '__all__'


class LikeCommentSerializer(ModelSerializer):
    model = LikeComment
    fields = '__all__'
    