from django.urls import path
from . import views

urlpatterns = [
    # Página principal (Home) obligatoria por la pauta
    path("", views.InicioView.as_view(), name="inicio"),
    
    # Catálogo de bicicletas y listado general
    path("bicicletas/", views.ListaBicicletasView.as_view(), name="lista_bicicletas"),
    
    # Rutas del CRUD de bicicletas
    path("bicicletas/crear/", views.CrearBicicletaView.as_view(), name="crear_bicicleta"),
    path("bicicletas/<int:pk>/", views.DetalleBicicletaView.as_view(), name="detalle_bicicleta"),
    path("bicicletas/<int:pk>/editar/", views.EditarBicicletaView.as_view(), name="editar_bicicleta"),
    path("bicicletas/<int:pk>/eliminar/", views.EliminarBicicletaView.as_view(), name="bicicleta_eliminar"),
]