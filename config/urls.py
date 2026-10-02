from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Incluimos las URLs de la app bicicletas en la raíz para que maneje '/' y '/bicicletas/' correctamente
    path("", include("bicicletas.urls")),
]

# ESTO OBLIGA A DJANGO A ENCONTRAR Y SERVIR TU VIDEO E IMÁGENES EN DESARROLLO
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
