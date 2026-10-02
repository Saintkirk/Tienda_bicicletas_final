from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Incluimos las URLs de la app bicicletas en la raíz para que maneje '/' y '/bicicletas/' correctamente
    path("", include("bicicletas.urls")),
]