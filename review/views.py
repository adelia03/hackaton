from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


from .models import Comment, LikeFilm, Favourite, LikeComment, Rating
from .serializers import CommentSerializer, RatingSerializer, FavoriteSerializer, LikeSerialzier
from account.models import User
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


class LikeFilmViewSet(ModelViewSet):
    queryset = LikeFilm.objects.all()
    serializer_class = LikeSerialzier
    permission_classes = [IsAuthenticated]

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



class FavouriteViewSet(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    @action(['POST'],detail=False)
    def favourite(request):
        author_id = request.data.get('author')
        film_id =request.data.get('film')
        author = get_object_or_404(User, id = author_id)
        film = get_object_or_404(Favourite , id = film_id)

        if Favourite.objects.filter(film=film, author=author).exists():
            Favourite.objects.filter(film=film,author=author).delete()
        else:
            Favourite.objects.create(film=film,author=author)
        return Response(status=201)

    

class CreateRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
