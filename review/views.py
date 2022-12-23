from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Comment, LikeFilm, Favourite, LikeComment, Rating
from .serializers import CommentSerializer, RatingSerializer, FavoriteSerializer, LikeSerialzier, LikeCommentSerializer
from .permissions import IsAuthorOrReadOnly


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    @action(['POST'], detail=False)
    def like(self,request):
        user = request.user
        ser = LikeCommentSerializer(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        comment_id = request.data.get("comment")

        if LikeComment.objects.filter(author=user, comment_id=comment_id).exists():
            LikeComment.objects.filter(author=user, comment_id=comment_id).delete()
        else:
            LikeComment.objects.create(author=user, comment_id=comment_id)
        return Response(status=201)


class CreateFavouriteAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    @swagger_auto_schema(request_body=FavoriteSerializer())
    def post(self, request):
        user = request.user
        ser = FavoriteSerializer(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        film_id =request.data.get("film")

        if Favourite.objects.filter(film_id=film_id, author=user).exists():
            Favourite.objects.filter(film_id=film_id, author=user).delete()
        else:
            Favourite.objects.create(film_id=film_id, author=user)
        return Response(status=201)
    

class CreateLikeFilmAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    @swagger_auto_schema(request_body=LikeSerialzier())
    def post(self, request):
        user = request.user
        ser = LikeSerialzier(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        film_id = request.data.get("film")

        if LikeFilm.objects.filter(film_id=film_id,author=user).exists():
            LikeFilm.objects.filter(film_id=film_id,author=user).delete()
        else:
            LikeFilm.objects.create(film_id=film_id,author=user)
        return Response(status=201)


class CreateRatingAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    @swagger_auto_schema(request_body=RatingSerializer())
    def post(self, request):
        user = request.user
        ser = RatingSerializer(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        film_id = request.data.get('film')

        if Rating.objects.filter(author=user,film_id=film_id).exists():
            rating = Rating.objects.get(author=user, film_id=film_id)
            rating.value = request.data.get('value')
            rating.save()
        else:
            ser.save()
        return Response(status=201)   
