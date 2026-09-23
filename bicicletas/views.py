from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import BicicletaForm
from .models import Bicicleta, Categoria, Marca, Modelo





class ListaBicicletasView(ListView):
    """Lista todas las bicicletas con filtros y búsqueda"""

    model = Bicicleta
    template_name = "bicicletas/lista.html"
    context_object_name = "bicicletas"
    paginate_by = 12

    def get_queryset(self):
        queryset = Bicicleta.objects.select_related(
            "categoria_rel", "modelo_rel__marca"
        ).all()

        # Filtro por búsqueda
        busqueda = self.request.GET.get("q")
        if busqueda:
            queryset = queryset.filter(
                Q(modelo_rel__nombre__icontains=busqueda)
                | Q(modelo_rel__marca__nombre__icontains=busqueda)
                | Q(descripcion__icontains=busqueda)
            )

        # Filtro por tipo
        tipo = self.request.GET.get("tipo")
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        # Filtro por categoría
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

        # Filtro por estado
        estado = self.request.GET.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)

        # Filtro por rango de precio
        precio_min = self.request.GET.get("precio_min")
        precio_max = self.request.GET.get("precio_max")
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)

        # Filtro solo disponibles
        solo_disponibles = self.request.GET.get("disponibles")
        if solo_disponibles:
            queryset = queryset.filter(stock__gt=0)

        # Ordenamiento
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
        context["aros"] = [20, 24, 26, 27, 28, 29]
        context["tipos"] = Bicicleta.TIPO_CHOICES
        context["estados"] = Bicicleta.ESTADO_CHOICES
        return context


class DetalleBicicletaView(DetailView):
    """Detalle de una bicicleta específica"""

    model = Bicicleta
    template_name = "bicicletas/detalle.html"
    context_object_name = "bicicleta"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bicicleta = self.object
        filtros = Q(tipo=bicicleta.tipo)
        if bicicleta.modelo_rel_id:
            filtros |= Q(modelo_rel__marca_id=bicicleta.modelo_rel.marca_id)
        context["relacionados"] = Bicicleta.objects.filter(
            filtros, stock__gt=0
        ).exclude(pk=bicicleta.pk)[:4]
        return context


class CrearBicicletaView(CreateView):
    """Crear nueva bicicleta"""

    model = Bicicleta
    form_class = BicicletaForm
    template_name = "bicicletas/crear.html"
    success_url = reverse_lazy("lista_bicicletas")

    def form_valid(self, form):
        messages.success(self.request, "La bicicleta fue creada correctamente.")
        return super().form_valid(form)


class EditarBicicletaView(UpdateView):
    """Editar bicicleta existente"""

    model = Bicicleta
    form_class = BicicletaForm
    template_name = "bicicletas/editar.html"
    success_url = reverse_lazy("lista_bicicletas")

    def form_valid(self, form):
        messages.success(
            self.request, "La bicicleta fue modificada correctamente."
        )
        return super().form_valid(form)


class EliminarBicicletaView(DeleteView):
    """Eliminar bicicleta"""

    model = Bicicleta
    template_name = "bicicletas/eliminar.html"
    success_url = reverse_lazy("lista_bicicletas")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "La bicicleta fue eliminada correctamente.")
        return super().delete(request, *args, **kwargs)
