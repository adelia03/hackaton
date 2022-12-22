from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Film

from .models import Comment, LikeFilm, Favourite, LikeComment, Rating
from .serializers import CommentSerializer, RatingSerializer, FavoriteSerializer, LikeSerialzier
from account_one.models import User
from .permissions import IsAuthorOrReadOnly

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    @action(['POST'], detail=False)
    def like(self,request):
        author_id = request.data.get("author")
        comment_id = request.data.get("comment")
        author = get_object_or_404(User, id=author_id)
        comment = get_object_or_404(Comment, id=comment_id)

        if LikeComment.objects.filter(author=author, comment=comment).exists():
            LikeComment.objects.filter(author=author, comment=comment).delete()
        else:
            LikeComment.objects.create(author=author, comment=comment)
        return Response(status=201)


class CreateFavouriteAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    @swagger_auto_schema(request_body=FavoriteSerializer())
    def post(self, request):
        author_id = request.data.get('author')
        film_id =request.data.get('film')
        author = get_object_or_404(User, id=author_id)
        film = get_object_or_404(Film , id=film_id)

        if Favourite.objects.filter(film=film, author=author).exists():
            Favourite.objects.filter(film=film,author=author).delete()
        else:
            Favourite.objects.create(film=film,author=author)
        return Response(status=201)
    
    

class CreateRatingAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
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


class CreateLikeFilmAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    @swagger_auto_schema(request_body=LikeSerialzier())
    def post(self, request):
        film_id = request.data.get("film")
        author_id = request.data.get("author")
        film = get_object_or_404(Film, id=film_id)
        author = get_object_or_404(User, id=author_id)

        if LikeFilm.objects.filter(film=film,author=author).exists():
            # если лайк поставили 
            LikeFilm.objects.filter(film=film,author=author).delete()
            # удаляем
        else:
            # если лайка нет 
            LikeFilm.objects.create(film=film,author=author)
            # создаем
        return Response(status=201)