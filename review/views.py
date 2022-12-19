from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import CommentFilm, LikeFilm,FavoriteFilm, LikeComment, RatingFilm
from .serializers import CommentSerializer, RatingSerializer, FavoriteSerializer, LikeSerialzier


# Create your views here.

User= get_user_model()

class CommentViewSet(ModelViewSet):
    queryset = CommentFilm.objects.all()
    serializer_class = CommentSerializer

    @action(['POST'], detail=False)
    def like(self,request):
        author_id = request.data.get('author')
        comment_id = request.data.get('comment')
        author = get_object_or_404(User, id = author_id)
        comment = get_object_or_404(CommentFilm, id = comment_id)

        if LikeComment.objects.filter(author=author, comment=comment).exists():
            LikeComment.objects.filter(author=author, comment=comment).delete()
        else:
            LikeComment.objects.create(author=author, comment=comment)
        return Response(status=201)



class LikeFilmViewSet(ModelViewSet):
    queryset = LikeFilm.objects.all()
    serializer_class = LikeSerialzier

    @action(['Post'], detail=False)
    def like(self,request):
        author_id = request.data.get('author')
        comment_id = request.data.get('comment')
        author = get_object_or_404(User, id = author_id)
        comment = get_object_or_404(LikeFilm, id = comment_id)

        if LikeFilm.objects.filter(author=author, comment=comment).exists():
            LikeFilm.objects.filter(author=author, comment=comment).delete()
        else:
            LikeFilm.objects.create(author=author, comment=comment)
        return Response(status=201)



class FavoriteViewSet(ModelViewSet):
    queryset = FavoriteFilm.objects.all()
    serializer_class = FavoriteSerializer

    @action(['POST'],detail=False)
    def favourite(request):
        author_id = request.data.get('author')
        film_id =request.data.get('film')
        author = get_object_or_404(User, id = author_id)
        film = get_object_or_404(FavoriteFilm , id = film_id)

        if FavoriteFilm.objects.filter(film=film, author=author).exists():
            FavoriteFilm.objects.filter(film=film,author=author).delete()
        else:
            FavoriteFilm.objects.create(film=film,author=author)
        return Response(status=201)

    

class CreateRatingAPIView(APIView):
    @swagger_auto_schema(request_body=RatingSerializer())
    def post(self, request):
        user = request.user
        ser = RatingSerializer(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        film_id = request.data.get('film')
        if RatingFilm.objects.filter(author=user,film_id=film_id).exists():
            rating = RatingFilm.objects.get(author=user, film_id=film_id)
            rating.value = request.data.egt('value')
            rating.save()
        else:
            ser.save()
        return Response(status=201)   
