from django import forms
from .models import *
from django.contrib.auth.models import User

#ESTAS CLASES HEREDAN LOS FORMULARIOS PREDETERMINADOS DE DJANGO
#NOS SIRVE PARA ORDENAR LOS ATRIBUTOS SEGUN CORRESPONDAN 

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'apellido', 'email', 'telefono']
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'mi-input-estilo'}),
            'descripcion': forms.Textarea(attrs={'class': 'mi-input-estilo'}),
            'precio': forms.NumberInput(attrs={'class': 'mi-input-estilo'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'mi-input-estilo'}),
            'stock': forms.NumberInput(attrs={'class': 'mi-input-estilo'}),
            'activo': forms.CheckboxInput(attrs={'class': 'mi-input-estilo'}),
            'idTipo': forms.Select(attrs={'class': 'mi-input-estilo'}),
        }

class TipoProductoForm(forms.ModelForm):
    class Meta:
        model: TipoProducto
        fields = '__all__'
          
class VentasForm(forms.ModelForm):
    class Meta:
        model : Ventas
        fields = '__all__'

class AdministradorForm(forms.ModelForm):
    class Meta:
        model : Administrador
        fields = '__all__'
        
