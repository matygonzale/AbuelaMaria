from django.contrib import admin
from .models import *

admin.site.register(Producto)
admin.site.register(TipoProducto)
admin.site.register(Ventas)
admin.site.register(Administrador)
admin.site.register(Clientes)

# Register your models here.
