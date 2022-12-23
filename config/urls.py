from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


"=========---Swagger docs---==========="
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

swagger_view = get_schema_view(
    openapi.Info(
        title="Kinopoisk",
        default_version="v1",
        description="hackaton",
    ),
    public=True
)
"========================================"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),
    path('docs/', swagger_view.with_ui("swagger", cache_timeout=0)),
    path('accounts/', include('allauth.urls')),
    path('account/', include('account_one.urls')),
    path('chat/', include('chat.urls')),    
    path('', include('review.urls')),
    path('', include('main.urls')),
]


"======---Media and static---======"
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"================================"