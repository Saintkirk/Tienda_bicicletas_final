# bicicletas/serializers.py

from rest_framework import serializers
from .models import Bicicleta, Categoria, Marca, Modelo

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ModeloSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')
    
    class Meta:
        model = Modelo
        fields = '__all__'

class BicicletaSerializer(serializers.ModelSerializer):
    # Campos de lectura para mostrar la información legible en el JSON
    marca = serializers.ReadOnlyField()
    modelo = serializers.ReadOnlyField()
    categoria = serializers.ReadOnlyField()

    class Meta:
        model = Bicicleta
        fields = '__all__'