import html
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    MAX_PRECIO_CLP,
    Bicicleta,
    Categoria,
    Marca,
    Modelo,
)


class ModeloSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value and hasattr(value, "instance"):
            option["attrs"]["data-marca"] = str(value.instance.marca_id)
            if value.instance.categoria_id:
                option["attrs"]["data-categoria"] = str(value.instance.categoria_id)
        return option


class BicicletaForm(forms.ModelForm):
    """Formulario para gestión de bicicletas"""

    marca = forms.ModelChoiceField(
        queryset=Marca.objects.order_by("nombre"),
        empty_label="Seleccione una marca",
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    aro = forms.TypedChoiceField(
        choices=[(aro, f"Aro {aro}") for aro in (12, 16, 20, 24, 26, 27, 28, 29)],
        coerce=int,
        empty_value=None,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # Lista estricta de exactamente 4 colores permitidos
    COLOR_CHOICES = [
        ("", "Seleccione un color"),
        ("Negro", "Negro"),
        ("Rojo", "Rojo"),
        ("Azul", "Azul"),
        ("Blanco", "Blanco"),
    ]

    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Color"
    )

    class Meta:
        model = Bicicleta
        fields = [
            "modelo_rel", 
            "categoria_rel", 
            "aro", 
            "precio", 
            "precio_oferta", 
            "stock", 
            "stock_minimo", 
            "color", 
            "descripcion", 
            "especificaciones", 
            "estado", 
            "es_destacada", 
            "es_oferta",
        ]
        widgets = {
            "modelo_rel": ModeloSelect(attrs={"class": "form-select"}),
            "categoria_rel": forms.Select(attrs={"class": "form-select"}),
            "precio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": MAX_PRECIO_CLP,
                    "maxlength": 8,
                    "inputmode": "numeric",
                    "oninput": "this.value = this.value.replace(/\\D/g, '').slice(0, 8)",
                }
            ),
            "precio_oferta": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": MAX_PRECIO_CLP,
                    "maxlength": 8,
                    "inputmode": "numeric",
                    "oninput": "this.value = this.value.replace(/\\D/g, '').slice(0, 8)",
                }
            ),
            # Restricciones estrictas para Stock (máximo 10 unidades, mínimo 0)
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 10,
                    "maxlength": 2,
                    "inputmode": "numeric",
                    "oninput": "this.value = this.value.replace(/\\D/g, '').slice(0, 2)",
                }
            ),
            # Restricciones estrictas para Stock Mínimo (máximo 10 unidades, mínimo 1)
            "stock_minimo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 10,
                    "maxlength": 2,
                    "inputmode": "numeric",
                    "oninput": "this.value = this.value.replace(/\\D/g, '').slice(0, 2)",
                }
            ),
            "color": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3, "maxlength": 500}),
            "especificaciones": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "es_destacada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "es_oferta": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["modelo_rel"].label = "Modelo"
        self.fields["categoria_rel"].label = "Categoría"
        self.order_fields(
            [
                "marca",
                "modelo_rel",
                "categoria_rel",
                "aro",
                "precio",
                "precio_oferta",
                "stock",
                "stock_minimo",
                "color",
                "descripcion",
                "especificaciones",
                "estado",
                "es_destacada",
                "es_oferta",
            ]
        )
        self.fields["precio"].max_value = MAX_PRECIO_CLP
        self.fields["precio"].help_text = "Ingresa un valor entre $1 y $99.999.999 CLP."
        self.fields["precio_oferta"].max_value = MAX_PRECIO_CLP
        self.fields["precio_oferta"].help_text = (
            "Máximo $99.999.999 CLP y menor que el precio normal."
        )
        
        # Textos de ayuda y límites estrictos actualizados a máximo 10 unidades
        self.fields["stock"].min_value = 0
        self.fields["stock"].max_value = 10
        self.fields["stock"].help_text = "Ingrese un valor entre 0 y 10 unidades."

        self.fields["stock_minimo"].min_value = 1
        self.fields["stock_minimo"].max_value = 10
        self.fields["stock_minimo"].help_text = "Ingrese un valor entre 1 y 10 unidades."

        self.fields["modelo_rel"].required = True
        self.fields["categoria_rel"].required = True
        self.fields["categoria_rel"].queryset = Categoria.objects.filter(
            activa=True
        ).order_by("nombre")
        self.fields["categoria_rel"].help_text = (
            "La categoría define automáticamente las características de la bicicleta."
        )

        marca_id = self.data.get("marca") if self.is_bound else None
        if not marca_id and self.instance.modelo_rel_id:
            marca_id = self.instance.modelo_rel.marca_id

        self.fields["modelo_rel"].queryset = Modelo.objects.order_by(
            "marca__nombre", "nombre"
        )

        if self.instance.modelo_rel_id:
            self.initial["marca"] = self.instance.modelo_rel.marca_id

    def clean(self):
        cleaned_data = super().clean()
        marca = cleaned_data.get("marca")
        modelo = cleaned_data.get("modelo_rel")
        if marca and modelo and modelo.marca_id != marca.id:
            self.add_error(
                "modelo_rel", "El modelo seleccionado no pertenece a la marca indicada."
            )
        categoria = cleaned_data.get("categoria_rel")
        if modelo and categoria and modelo.categoria_id != categoria.id:
            self.add_error(
                "categoria_rel",
                "La categoría seleccionada no corresponde al modelo indicado.",
            )
        aro = cleaned_data.get("aro")
        if modelo and aro:
            aro_modelo = modelo.nombre.rsplit("(Aro ", 1)[-1].rstrip(")")
            if aro_modelo.isdigit() and int(aro_modelo) != aro:
                self.add_error(
                    "aro", "El aro seleccionado no corresponde al modelo indicado."
                )
        return cleaned_data

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio

    def clean_precio_oferta(self):
        precio_oferta = self.cleaned_data.get("precio_oferta")
        precio = self.cleaned_data.get("precio")

        if precio_oferta and precio:
            if precio_oferta >= precio:
                raise forms.ValidationError("El precio de oferta debe ser menor al precio normal.")
        return precio_oferta

    def clean_stock(self):
        """Valida estrictamente que el stock esté entre 0 y 10 unidades en el backend."""
        stock = self.cleaned_data.get("stock")
        if stock is not None:
            if stock < 0:
                raise ValidationError("El stock no puede ser negativo.")
            if stock > 10:
                raise ValidationError("El stock máximo permitido es de 10 unidades.")
        return stock

    def clean_stock_minimo(self):
        """Valida estrictamente que el stock mínimo esté entre 1 y 10 unidades en el backend."""
        stock_minimo = self.cleaned_data.get("stock_minimo")
        if stock_minimo is not None:
            if stock_minimo < 1:
                raise ValidationError("El stock mínimo debe ser al menos 1.")
            if stock_minimo > 10:
                raise ValidationError("El stock mínimo no puede superar las 10 unidades.")
        return stock_minimo

    def clean_color(self):
        """Valida que el color seleccionado pertenezca estrictamente a las opciones permitidas."""
        color = self.cleaned_data.get("color")
        colores_validos = [c[0] for c in self.COLOR_CHOICES if c[0] != ""]
        if color not in colores_validos:
            raise ValidationError("Seleccione un color válido de la lista.")
        return color

    def clean_descripcion(self):
        """Valida el límite de caracteres y sanitiza la descripción en el backend."""
        descripcion = self.cleaned_data.get("descripcion", "")

        if not descripcion:
            return descripcion

        if len(descripcion) > 500:
            raise ValidationError("La descripción no puede superar los 500 caracteres.")

        descripcion_limpia = html.escape(descripcion)

        return descripcion_limpia