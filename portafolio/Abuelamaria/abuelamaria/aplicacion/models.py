from django.db import models
from django.contrib.auth.models import User


#MODELOS CON LOS QUE TRABAJAREMOS E IMPORTAREMOS A NUESTRA BD
class TipoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField(max_length=150)
    precio = models.PositiveIntegerField()
    stock = models.SmallIntegerField(default=0)
    imagen = models.ImageField(upload_to='imagenes/', blank=True)
    activo = models.BooleanField(default=1) 
    idTipo = models.ForeignKey(TipoProducto, models.DO_NOTHING, verbose_name="categoria")
    
    def __str__(self):
        return self.nombre
    
class Clientes(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=12)
    puntos = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    pais = models.CharField(max_length=50, null=True)
    idUser = models.OneToOneField(User, models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class Ventas(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.BigIntegerField()
    fecha = models.DateField(auto_now=True, null=True)
    hora = models.DateTimeField(auto_now=True, null=True)
    trimestre = models.PositiveSmallIntegerField()
    idProducto = models.ManyToManyField(Producto, db_table='detalle_venta_producto')
    idCliente = models.ManyToManyField(Clientes, db_table='compras_x_usuarios')
    
class Administrador(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    idUser = models.OneToOneField(User, models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.nombre
    
#------------------------- MODELOS NECESARIOS PARA INTEGRAR TRANSBANK-----------------------------------------------

class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField(default=0)
    fecha = models.DateField(auto_now=True, blank=True)
    producto = models.ForeignKey(Producto, models.CASCADE)
    users_metadata = models.ForeignKey(User, models.CASCADE)
    
class Orden_de_compra(models.Model):
    id = models.AutoField(primary_key=True)
    users_metadata = models.ForeignKey(User, models.DO_NOTHING)
    token_ws = models.CharField(max_length=255, default=0)
    tarjeta = models.CharField(max_length=10, default=0)
    fecha_transbank = models.CharField(max_length=100, default='0')
    estado_transbank = models.CharField(max_length=100, default='0')
    monto = models.PositiveIntegerField()
    
class Orden_de_compra_detalle(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    id_orden_compra = models.ForeignKey(Orden_de_compra, models.CASCADE)
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING)
    
class Boleta(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    cantidad = models.PositiveIntegerField()
    precio_total = models.BigIntegerField()
 
   
class Contacto(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    nombre = models.CharField(max_length=80)
    telefono = models.BigIntegerField()
    descripcion = models.TextField(max_length=300)
    
