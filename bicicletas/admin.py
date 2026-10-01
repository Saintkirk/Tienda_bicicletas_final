from django.contrib import admin
from .models import Bicicleta, Categoria, Marca, Modelo


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "segmento")


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ("nombre", "marca")
    list_filter = ("marca",)


@admin.register(Bicicleta)
class BicicletaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modelo_rel",
        "tipo",
        "aro",
        "precio",
        "stock",
        "estado",
        "es_oferta",
    )
    list_filter = ("tipo", "estado", "es_oferta", "es_destacada")
    search_fields = (
        "modelo_rel__nombre",
        "modelo_rel__marca__nombre",
        "descripcion",
    )
    list_editable = ("precio", "stock", "estado", "es_oferta")