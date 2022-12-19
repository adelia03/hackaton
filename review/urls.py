from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FavoriteViewSet, LikeFilmViewSet, CreateRatingAPIView

router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('favorites', FavoriteViewSet)
router.register('likefilms', LikeFilmViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('rating/', CreateRatingAPIView.as_view()),
]