from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from cook_app_drf.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('', include('recipes.urls')),
    path('', include('comment.urls')),
    path('api/', include('cook_app_drf.urls')),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

