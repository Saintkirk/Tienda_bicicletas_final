from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

# Importaciones para Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .serializers import BicicletaSerializer, CategoriaSerializer, MarcaSerializer, ModeloSerializer

from .forms import BicicletaForm
from .models import Bicicleta, Categoria, Marca, Modelo


# --- PERMISO PERSONALIZADO PARA SUPERUSUARIO EN LA API ---
class EsSuperUsuarioOReadOnly(BasePermission):
    """
    Permite acceso de lectura (GET, HEAD, OPTIONS) a cualquier usuario.
    Permite operaciones de escritura (POST, PUT, PATCH, DELETE) exclusivamente a superusuarios.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_superuser


# --- VISTAS TRADICIONALES (HTML) ---

class InicioView(TemplateView):
    """
    Vista para la página de bienvenida cinematográfica con video de fondo.
    Mapea al archivo ubicado en 'templates/bicicletas/inicio.html'.
    """
    template_name = "bicicletas/inicio.html"

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario ya está autenticado, lo salta automáticamente al catálogo
        if request.user.is_authenticated:
            return redirect("lista_bicicletas")
        return super().dispatch(request, *args, **kwargs)


class ListaBicicletasView(LoginRequiredMixin, ListView):
    """
    Catálogo principal del inventario de bicicletas. Incluye paginación y 
    múltiples filtros avanzados acumulativos.
    """
    model = Bicicleta
    template_name = "bicicletas/lista.html"
    context_object_name = "bicicletas"
    paginate_by = 10
    login_url = "login"

    def get_queryset(self):
        queryset = Bicicleta.objects.select_related(
            "categoria_rel", "modelo_rel__marca"
        ).all()

        # Filtro de búsqueda global (por nombre de modelo, marca o descripción)
        busqueda = self.request.GET.get("q")
        if busqueda:
            queryset = queryset.filter(
                Q(modelo_rel__nombre__icontains=busqueda)
                | Q(modelo_rel__marca__nombre__icontains=busqueda)
                | Q(descripcion__icontains=busqueda)
            )

        # Filtros por atributos del modelo
        tipo = self.request.GET.get("tipo")
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        categoria = self.request.GET.get("categoria")
        if categoria:
            queryset = queryset.filter(categoria_rel_id=categoria)

        marca = self.request.GET.get("marca")
        if marca:
            queryset = queryset.filter(modelo_rel__marca_id=marca)

        modelo = self.request.GET.get("modelo")
        if modelo:
            queryset = queryset.filter(modelo_rel_id=modelo)

        aro = self.request.GET.get("aro")
        if aro:
            queryset = queryset.filter(aro=aro)

        estado = self.request.GET.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)

        # Filtros por rangos de precio
        precio_min = self.request.GET.get("precio_min")
        precio_max = self.request.GET.get("precio_max")
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)

        # Filtro de disponibilidad inmediata
        solo_disponibles = self.request.GET.get("disponibles")
        if solo_disponibles:
            queryset = queryset.filter(stock__gt=0)

        # Ordenamiento dinámico (por defecto muestra lo más reciente)
        orden = self.request.GET.get("orden", "-fecha_ingreso")
        queryset = queryset.order_by(orden)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.filter(activa=True)
        context["marcas"] = Marca.objects.order_by("nombre")
        context["modelos"] = Modelo.objects.select_related("marca").order_by(
            "marca__nombre", "nombre"
        )
        context["aros"] = [12, 16, 20, 24, 26, 27, 28, 29]
        context["tipos"] = Bicicleta.TIPO_CHOICES
        context["estados"] = Bicicleta.ESTADO_CHOICES
        return context


class DetalleBicicletaView(LoginRequiredMixin, DetailView):
    model = Bicicleta
    template_name = "bicicletas/detalle.html"
    context_object_name = "bicicleta"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bicicleta = self.object
        filtros = Q(tipo=bicicleta.tipo)
        if bicicleta.modelo_rel_id:
            filtros |= Q(modelo_rel__marca_id=bicicleta.modelo_rel.marca_id)
        
        # Sugiere hasta 4 productos relacionados basados en tipo o marca común
        context["relacionados"] = (
            Bicicleta.objects.filter(filtros, stock__gt=0)
            .exclude(pk=bicicleta.pk)
            .select_related("modelo_rel__marca")[:4]
        )
        return context


class CrearBicicletaView(LoginRequiredMixin, CreateView):
    model = Bicicleta
    form_class = BicicletaForm
    template_name = "bicicletas/crear.html"
    success_url = reverse_lazy("lista_bicicletas")
    login_url = "login"

    def form_valid(self, form):
        messages.success(self.request, "La bicicleta fue creada correctamente.")
        return super().form_valid(form)


class EditarBicicletaView(LoginRequiredMixin, UpdateView):
    model = Bicicleta
    form_class = BicicletaForm
    template_name = "bicicletas/editar.html"
    success_url = reverse_lazy("lista_bicicletas")
    login_url = "login"

    def form_valid(self, form):
        messages.success(
            self.request, "La bicicleta fue modificada correctamente."
        )
        return super().form_valid(form)


class EliminarBicicletaView(LoginRequiredMixin, DeleteView):
    model = Bicicleta
    template_name = "bicicletas/eliminar.html"
    success_url = reverse_lazy("lista_bicicletas")
    login_url = "login"

    def delete(self, request, *args, **kwargs):
        messages.success(
            request, "La bicicleta fue eliminada correctamente."
        )
        return super().delete(request, *args, **kwargs)


# --- VIEWSETS DE LA API REST (Django REST Framework) ---

class BicicletaViewSet(viewsets.ModelViewSet):
    queryset = Bicicleta.objects.select_related("categoria_rel", "modelo_rel__marca").all()
    serializer_class = BicicletaSerializer
    permission_classes = [EsSuperUsuarioOReadOnly]


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsSuperUsuarioOReadOnly]


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [EsSuperUsuarioOReadOnly]


class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.select_related("marca", "categoria").all()
    serializer_class = ModeloSerializer
    permission_classes = [EsSuperUsuarioOReadOnly]
