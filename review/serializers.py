from rest_framework.serializers import ModelSerializer

from .models import Comment, Rating, Favourite, LikeFilm, LikeComment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('author',)

    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs

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
        request = self.context.get('request')  
        attrs['author'] = request.user
        return attrs

    
class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        exclude =('author',)

    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs
        

class LikeSerialzier(ModelSerializer):
    class Meta:
        model = LikeFilm
        exclude = ('author',)


class LikeCommentSerializer(ModelSerializer):
    class Meta:
        model = LikeComment
        exclude = ('author',)
