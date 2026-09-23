"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Panel de administración de Django
    path("admin/", admin.site.urls),
    
    # URLs de la app bicicletas bajo el prefijo 'bicicletas/'
    path("bicicletas/", include("bicicletas.urls")),
    
    # Permite que la ruta raíz (http://127.0.0.1:8000/) cargue directamente las bicicletas
    path("", include("bicicletas.urls")),
]