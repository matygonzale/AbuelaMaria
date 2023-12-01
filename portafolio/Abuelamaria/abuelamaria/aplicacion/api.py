from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *

#ES LA API DEL PROYECTO
#ESTAS FUNCIONES RECIBIRAN Y ENTREGARÁN LOS DATOS EN JSON 
#SE TRABAJA CON EL SERIALIZER Y LOS MODELOS

@api_view(['GET','POST'])
def clientes_api_view(request):
    
    if request.method == 'GET':
        clientes = Clientes.objects.all() #CONSULTA A BASE DE DATOS
        clientes_serializador = ClientesSerializer(clientes, many=True)
        return Response(clientes_serializador.data)
    
    elif request.method == 'POST':
        clientes_serializador = ClientesSerializer(data = request.data)#CAPTURAMOS LOS DATOS QUE LLEGAN
        if clientes_serializador.is_valid():                           #SE VALIDAN LOS CAMPOS NECESARIOS
            clientes_serializador.save()                               #SE GUARDAN
            return Response(clientes_serializador.data)
        return Response(clientes_serializador.errors)                  #SE RETORNA EL RESULTADO

@api_view(['GET','PUT','DELETE'])
def clientes_detail_view(request, pk = None):
    
    if request.method == 'GET':
        clientes = Clientes.objects.filter(idUser = pk).first()                  #SE HACE UNA CONSULTA CON UN IDENTIFICADOR
        clientes_serializador = ClientesSerializer(clientes)                     #SE LLENAN LOS DATOS AL SERIALIZADOR Y PASA A LA VARIABLE
        return Response(clientes_serializador.data)
    
    elif request.method == 'PUT':
        clientes = Clientes.objects.filter(idUser = pk).first()        #SE CAPTURA AL CLIENTE CON EL IDENTIFICADOR
        clientes_serializador = ClientesSerializer(clientes, data = request.data)#SE CAPTURA LOS DATOS DEL CLIENTE Y SE CARGAN AL SERIALIZER
        if clientes_serializador.is_valid():
            clientes_serializador.save()
            return Response(clientes_serializador.data)
        return Response(clientes_serializador.errors)                            #SE CAMBIAN LOS VALORES Y SE GUARDA
    
    elif request.method == 'DELETE':
        
        if request.method == 'DELETE':
            clientes = Clientes.objects.filter(idUser = pk).first().delete()     #SE CAPTURA AL CLIENTE Y SE BORRA
            return Response('Eliminado')
        else:
            return Response('Error')
        
        

@api_view(['GET','POST'])
def administrador_api_view(request):
    
    if request.method == 'GET':
        admin = Administrador.objects.all()
        admin_serializador = AdministradorSerializer(admin, many=True)
        return Response(admin_serializador.data)
    
    elif request.method == 'POST':
        admin_serializador = AdministradorSerializer(data = request.data)
        if admin_serializador.is_valid():
            admin_serializador.save()
            return Response(admin_serializador.data)
        return Response(admin_serializador.errors)
    
@api_view(['GET','PUT','DELETE'])
def administrador_detail_view(request, pk = None):
    
    if request.method == 'GET':
        admin = Administrador.objects.filter(idUser = pk).first()
        admin_serializador = AdministradorSerializer(admin)
        return Response(admin_serializador.data)
    
    elif request.method == 'PUT':
        admin = Administrador.objects.filter(idUser = pk).first()
        admin_serializador = admin_serializador(admin, data = request.data)
        if admin_serializador.is_valid():
            admin_serializador.save()
            return Response(admin_serializador.data)
        return Response(admin_serializador.errors) 
    
    elif request.method == 'DELETE':
        
        if request.method == 'DELETE':
            admin = Administrador.objects.filter(idUser = pk).first().delete()
            return Response('Eliminado')
        else:
            return Response('Error')
        
        

@api_view(['GET','POST'])
def producto_api_view(request):
    
    if request.method == 'GET':
        producto = Producto.objects.all()
        producto_serializador = ProductoSerializer(producto, many=True)
        print(producto_serializador)
        return Response(producto_serializador.data)
    
    elif request.method == 'POST':
        producto_serializador = ProductoSerializer(data = request.data)
        if producto_serializador.is_valid():
            producto_serializador.save()
            return Response(producto_serializador.data)
        return Response(producto_serializador.errors)

@api_view(['GET','PUT','DELETE'])
def producto_detail_view(request, pk = None):
    
    if request.method == 'GET':
        producto = Producto.objects.filter(id = pk).first()
        producto_serializador = ProductoSerializer(producto)
        return Response(producto_serializador.data)
    
    elif request.method == 'PUT':
        producto = Producto.objects.filter(id = pk).first()
        producto_serializador = producto_serializador(producto, data = request.data)
        if producto_serializador.is_valid():
            producto_serializador.save()
            return Response(producto_serializador.data)
        return Response(producto_serializador.errors) 
    
    elif request.method == 'DELETE':
        
        if request.method == 'DELETE':
            admin = Administrador.objects.filter(id = pk).first().delete()
            return Response('Eliminado')
        else:
            return Response('Error')
        
        
    
@api_view(['GET','POST'])
def tipoproducto_api_view(request):
    
    if request.method == 'GET':
        producto = TipoProducto.objects.all()
        producto_serializador = TipoProductoSerializer(producto, many=True)
        return Response(producto_serializador.data)
    
    elif request.method == 'POST':
        producto_serializador = TipoProductoSerializer(data = request.data)
        if producto_serializador.is_valid():
            producto_serializador.save()
            return Response(producto_serializador.data)
        return Response(producto_serializador.errors)
    
@api_view(['GET','PUT','DELETE'])
def tipoproducto_detail_view(request, pk = None):
    
    if request.method == 'GET':
        producto = Producto.objects.filter(id = pk).first()
        producto_serializador = ProductoSerializer(producto)
        return Response(producto_serializador.data)
    
    elif request.method == 'PUT':
        producto = Producto.objects.filter(id = pk).first()
        producto_serializador = producto_serializador(producto, data = request.data)
        if producto_serializador.is_valid():
            producto_serializador.save()
            return Response(producto_serializador.data)
        return Response(producto_serializador.errors) 
    
    elif request.method == 'DELETE':
        
        if request.method == 'DELETE':
            admin = Administrador.objects.filter(id = pk).first().delete()
            return Response('Eliminado')
        else:
            return Response('Error')
        
        

@api_view(['GET','POST'])
def ventas_api_view(request):
    
    if request.method == 'GET':
        ventas = Ventas.objects.all()
        ventas_serializador = VentasSerializer(ventas, many=True)
        return Response(ventas_serializador.data)
    
    elif request.method == 'POST':
        ventas_serializador = VentasSerializer(data = request.data)
        if ventas_serializador.is_valid():
            ventas_serializador.save()
            return Response(ventas_serializador.data)
        return Response(ventas_serializador.errors)

@api_view(['GET','PUT','DELETE'])
def ventas_detail_view(request, pk = None):
    
    if request.method == 'GET':
        ventas = Ventas.objects.filter(id = pk).first()
        ventas_serializador = VentasSerializer(ventas)
        return Response(ventas_serializador.data)
    
    elif request.method == 'PUT':
        ventas = Ventas.objects.filter(id = pk).first()
        ventas_serializador = ventas_serializador(ventas, data = request.data)
        if ventas_serializador.is_valid():
            ventas_serializador.save()
            return Response(ventas_serializador.data)
        return Response(ventas_serializador.errors) 
    
    elif request.method == 'DELETE':
        
        if request.method == 'DELETE':
            ventas = Ventas.objects.filter(id = pk).first().delete()
            return Response('Eliminado')
        else:
            return Response('Error')