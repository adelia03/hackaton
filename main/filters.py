from django_filters.rest_framework import FilterSet
import django_filters

from .models import Film

class FilmFilter(FilterSet):
    film_title = django_filters.CharFilter(field_name='film_title')
    film_id = django_filters.NumberFilter(field_name='film')
    
    class Meta:
        model = Film
        fields = ['film_title','film_id']
