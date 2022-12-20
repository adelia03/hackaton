from rest_framework.serializers import ModelSerializer
from .models import Film
from review.serializers import *

class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
    
    def to_representation(self, instance: Film):
        rep = super().to_representation(instance)
        # rep['category'] = CategorySerializer(instance.category).data
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['rating'] = instance.average_rating
        rep['favourites'] = FavoriteSerializer(instance.favourites.all(), many=True).data
        
        return rep