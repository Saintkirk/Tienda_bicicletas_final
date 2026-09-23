from django.urls import path
from . import views

urlpatterns = [
    # Vistas principales
    path("", views.InicioView.as_view(), name="inicio"),
    path("bicicletas/", views.ListaBicicletasView.as_view(), name="lista_bicicletas"),
    
    # Ruta de creación de bicicleta corregida con el nombre 'crear_bicicleta'
    path("bicicletas/crear/", views.CrearBicicletaView.as_view(), name="crear_bicicleta"),
    
    path("bicicletas/<int:pk>/", views.DetalleBicicletaView.as_view(), name="detalle_bicicleta"),
    path("bicicletas/<int:pk>/editar/", views.EditarBicicletaView.as_view(), name="editar_bicicleta"),
    path("bicicletas/<int:pk>/eliminar/", views.EliminarBicicletaView.as_view(), name="bicicleta_eliminar"),
   
]