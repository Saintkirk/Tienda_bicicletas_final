from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.InicioView.as_view(), name="inicio"),
    path("bicicletas/", views.ListaBicicletasView.as_view(), name="lista_bicicletas"),
    path(
        "bicicletas/<int:pk>/",
        views.DetalleBicicletaView.as_view(),
        name="detalle_bicicleta",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="bicicletas/login.html"),
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
]