from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet



from .models import Film
from .serializers import FilmSerializer

class FilmViewSet(ModelViewSet):
    serializer_class = FilmSerializer
    queryset = Film.objects.all()
