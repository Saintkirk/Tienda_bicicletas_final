from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuración del enrutador de DRF
router = DefaultRouter()
router.register(r'bicicletas', views.BicicletaViewSet, basename='api_bicicletas')
router.register(r'categorias', views.CategoriaViewSet, basename='api_categorias')
router.register(r'marcas', views.MarcaViewSet, basename='api_marcas')
router.register(r'modelos', views.ModeloViewSet, basename='api_modelos')

urlpatterns = [
    # Rutas tradicionales existentes
    path("", views.InicioView.as_view(), name="inicio"),
    path("bicicletas/", views.ListaBicicletasView.as_view(), name="lista_bicicletas"),
    path(
        "bicicletas/<int:pk>/",
        views.DetalleBicicletaView.as_view(),
        name="detalle_bicicleta",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="bicicletas/login.html"
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "bicicletas/crear/",
        views.CrearBicicletaView.as_view(),
        name="crear_bicicleta",
    ),
    path(
        "bicicletas/<int:pk>/editar/",
        views.EditarBicicletaView.as_view(),
        name="editar_bicicleta",
    ),
    path(
        "bicicletas/<int:pk>/eliminar/",
        views.EliminarBicicletaView.as_view(),
        name="bicicleta_eliminar",
    ),

    # Rutas de la API REST (Prefijo /api/)
    path("api/", include(router.urls)),
]