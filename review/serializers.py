from rest_framework.serializers import ModelSerializer

from .models import Comment, Rating, Favourite, LikeFilm , LikeComment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance: Comment):
        rep = super().to_representation(instance)
        rep['author'] = instance.author.email
        rep['likes'] = instance.likes.count()
        del rep['film']
        return rep


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('author',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')  # получаем запрос из view
        attrs['author'] = request.user
        return attrs

    
class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        exclude =('author',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['film'] = instance.film.title
        return rep



class LikeSerialzier(ModelSerializer):
    class Meta:
        model = LikeFilm
        fields = '__all__'


class LikeCommentSerializer(ModelSerializer):
    class Meta:
        model = LikeComment
        exclude = ('comment',)
