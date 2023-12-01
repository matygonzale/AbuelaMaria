from rest_framework import serializers
from .models import *

#ESTAS CLASES TRADUCIRAN LOS DATOS JSON SEGUN LA CLASE QUE INVOQUEMOS
#EL SERIALIZER SE ENCARGA DE RECIBIR LA INFORMACION TRADUCIRLA Y ENTREGARLA O VICEVERSA

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'
        
class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        
class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'
        
class VentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = '__all__'