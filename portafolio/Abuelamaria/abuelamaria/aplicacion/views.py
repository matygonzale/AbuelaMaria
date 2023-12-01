from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
import json
import requests
from .templatetags import utilidades
from .webpay import *
from .forms import *
from django.contrib.auth.hashers import make_password

from django.http import JsonResponse

#FUNCION QUE TRAERÁ LA VISTA INDEX 
def home (request):
    
    return render(request, 'tienda/home.html')

def carro (request):
    productos = Producto.objects.all()
    return render(request, 'tienda/carro.html', {'productos': productos})


def detalleprod(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    productos_relacionados = Producto.objects.exclude(id=producto_id)[:4]
    print(productos_relacionados)

    return render(request, 'tienda/detalleprod.html', {'producto': producto, 'productos_relacionados': productos_relacionados})

def checkout(request):
    return render(request, 'tienda/checkout.html')


def editarUsuario(request):
    return render(request, 'crudUsuario/editarusuario.html')


def Base (request):
    return render(request, 'tienda/Base.html')

def contacto(request):
    return render(request, 'aplicacion/contacto.html')

def nosotros(request):
    return render(request, 'tienda/nosotros.html')

def prueba(request):
    productos=Producto.objects.all()
    return render(request, 'tienda/prueba.html', {"productos":productos})

def catalogo(request):
    productos=Producto.objects.all()
    return render(request, 'tienda/catalogo.html', {"productos":productos})
 
#DEFINITIVAS 
#FUNCIONES DE USUARIO 
#INICIO DE SESIÓN DEL CLIENTE
def iniciar_sesion(request):
    
    if request.method == 'GET':
        return render(request, 'crudUsuario/login.html')
    
    if request.method == 'POST':
        
        usuario = request.POST.get('username')
        contrasenia = request.POST.get('password')

        user = authenticate(request, username=usuario, password=contrasenia)
        
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            
            print('funcionó: ', user)
        else:
            
            print('NO funcionó')
            return HttpResponseRedirect('Home')
        
    return render(request, 'tienda/home.html')

#SALIR DE SESION
def deslogear(request):
    logout(request)
    
    print("sesion terminada")
    return redirect('Home')

# FUNCION QUE LISTARÁ LOS USUARIOS
def listar_usuario(request):
    personas = Clientes.objects.all()
    contexto = {
        'form' : personas
    }
    return render(request, 'crearusuario.html', contexto)

#FUNCION QUE CREARÁ UN USER Y UN CLIENTE A LA VEZ
def crear_usuario(request):
    
    if request.method == 'GET':
        
        usuario = ClientesForm()
    
        contexto = {'form': usuario}
        
    if request.method == 'POST':
        
        usuario = request.POST.get('username')
        usuario_existente = User.objects.filter(username=usuario).exists()
        
        contrasenia = request.POST.get('password')
        
        if usuario_existente:
            mensaje = f"El usuario {usuario} ya existe."
            return JsonResponse({'message': mensaje, 'exists': True})
        else:
            mensaje = f"El usuario {usuario} no existe."
            hashed_password = make_password(contrasenia)
            user = User.objects.create(username=usuario, password=hashed_password)
            
            x = User.objects.get(username=usuario)
            a = Clientes(request.POST)
            a.idUser = x
            a.nombre = request.POST.get('nombre')
            a.apellido = request.POST.get('apellido')
            a.email = request.POST.get('email')
            a.telefono = request.POST.get('telefono')
            cliente = a
            cliente.save()

            contexto = {'form': cliente, 'exists': False}
            
    return render(request, 'crudUsuario/crearusuario.html', contexto)

#FUNCION QUE EDITARÁ AL CLIENTE
def editar_usuario(request, pk):
    cliente = Clientes.objects.get(idUser_id = pk)
    
    if request.method == 'GET':
        
        usuario = ClientesForm(instance = cliente)
        contexto = {
            'form' : usuario
        }
    elif request.method == 'POST':
        
        usuario = ClientesForm(request.POST, instance = cliente)
        
        contexto = {
        'form' : usuario
        }
        if usuario.is_valid():
            usuario.save()
    return render(request, 'crudUsuario/editarusuario.html', contexto)

#FUNCION QUE ELIMINARÁ UN CLIENTE
def eliminar_usuario(request, pk):
    
    if request.method == 'GET':
        return render(request, 'crudUsuario/editarusuario.html')
    
    if request.method == 'POST':
        
        persona = Clientes.objects.get(idUser_id = pk)
        
        x = persona.idUser
        print(x)
        usuario = User.objects.get(id = x)
        
        print(usuario)
        
        persona.delete()
        usuario.delete()
        
        
    return render(request,'aplicacion/crearusuario.html')


#FUNCIONES DE CRUD PRODUCTO
#FUNCION QUE TRAE LA VISTA PRODUCTOS Y LOS LISTARÁ
#@login_required(login_url = 'Iniciosesion')
def listar_productos(request):
    productos=Producto.objects.all()
    return render(request, 'crud/productosAdmin.html', {'producto': productos})

# CREARA UN NUEVO PRODUCTO 
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Productos')  # ASIGNA LA VISTA LISTAR 
    else:
        form = ProductoForm()
    
    return render(request, 'crud/crear.html', {'form': form})

#FUNCION EDITAR PRODUCTO    
def editar_producto(request, id):
    productos = Producto.objects.get(id = id)
    
    if request.method == 'GET':
        
        producto = ProductoForm(instance = productos)
        contexto = {
            'form' : producto
        }
    elif request.method == 'POST':
        
        producto = ProductoForm(request.POST, instance = productos)
        
        contexto = {
        'form' : producto
        }
        if producto.is_valid():
            producto.save()
        return redirect('Productos')
    return render(request, 'crud/editar.html', contexto)

# FUNCION ELIMINAR PRODUCTO
def eliminar_producto(request, id):
    if request.method == 'GET':
        producto = Producto.objects.get(id = id)
        producto.delete()
        
    return redirect('Productos')

def buscarproducto(request):
    consulta = request.GET.get('q')  # Obtener el término de búsqueda de la URL
    
    if consulta:
        # Realizar la búsqueda de productos por nombre
        productos = Producto.objects.filter(nombre__contains=consulta)
    else:
        productos = Producto.objects.all()  # Mostrar todos los productos si no se especifica una búsqueda
    
    return render(request, 'crud/buscarproducto.html', {'productos': productos, 'Busqueda': consulta})



#FUNCIONES DE TIENDA
#FUNCION QUE PERMITIRA VER LOS PORDUCTOS DE LA TIENDA
def tienda(request):
    productos=Producto.objects.all()
    return render(request, "tienda/tienda.html", {"productos":productos})



# FUNCION QUE LISTARÁ LAS CATEGORIAS
def listar_categoria(request):
    categorias = TipoProducto.objects.all()
    contexto = {
        'form' : categorias
    }
    return render(request, 'crearusuario.html', contexto)

#FUNCION QUE CREARÁ UNA CATEGORIA
def crear_categoria(request):
    
    if request.method == 'GET':
        categorias = TipoProducto.objects.all()
        contexto = {
            'form' : categorias
        }
    
    if request.method == 'POST':
        
        categoria = TipoProductoForm(request.POST)
        
        contexto =   {
            'form' : categoria
        }
        if categoria.is_valid():
            categoria.save()
    
    return render(request, 'aplicacion/pruebas.html', contexto)

#FUNCION QUE EDITARÁ UNA CATEROGIA
def editar_categoria(request, pk):
    consulta = TipoProducto.objects.get(id = pk)
    
    if request.method == 'GET':
        
        categoria = TipoProductoForm(instance = consulta)
        contexto = {
            'form' : categoria
        }
    elif request.method == 'POST':
        
        categoria = TipoProductoForm(request.POST, instance = consulta)
        
        contexto = {
        'form' : categoria
        }
        if categoria.is_valid():
            categoria.save()
    return render(request, 'aplicacion/pruebas.html', contexto)

#FUNCION QUE ELIMINARÁ UNA CATEGORIA
def eliminar_categoria(request, pk):
    
    if request.method == 'GET':
        categoria = TipoProducto.objects.get(id = pk)
        contexto = {
            'form': categoria
        }
        
    elif request.method == 'POST':
        categoria = TipoProducto.objects.get(id = pk)
        
        contexto = {
            'form': categoria
        }
        categoria.delete()
        
    return render(request, 'aplicacion/pruebas.html', contexto)


# FUNCION QUE LISTARÁ LOS USUARIOS
def listar_admin(request):
    personas = Administrador.objects.all()
    contexto = {
        'form' : personas
    }
    return render(request, 'crearusuario.html', contexto)

#FUNCION QUE CREARÁ UNA ADMINISTRADOR
def crear_admin(request):
    
    if request.method == 'GET':
        categorias = Administrador.objects.all()
        contexto = {
            'form' : categorias
        }
    
    if request.method == 'POST':
        
        usuario = request.POST.get('username')
        contrasenia = request.POST.get('password')
        user = User()
        user.username = usuario
        user.password = contrasenia
        
        
        if user is not None:
            user.save()
            x = User.objects.get(username = usuario)
            a = Administrador(request.POST)
            a.idUser = x
            a.nombre = request.POST.get('nombre')
            a.apellido = request.POST.get('apellido')
            cliente = a
            cliente.save()
            
            contexto = {
                'form' : cliente
            }
    
    return render(request, 'aplicacion/pruebas.html', contexto)

#FUNCION QUE EDITARÁ AL CLIENTE
def editar_admin(request, pk):
    cliente = Administrador.objects.get(idUser_id = pk)
    
    if request.method == 'GET':
        
        usuario = AdministradorForm(instance = cliente)
        contexto = {
            'form' : usuario
        }
    elif request.method == 'POST':
        
        usuario = AdministradorForm(request.POST, instance = cliente)
        
        contexto = {
        'form' : usuario
        }
        if usuario.is_valid():
            usuario.save()
    return render(request, 'aplicacion/pruebas.html', contexto)

#FUNCION QUE ELIMINARÁ UN CLIENTE
def eliminar_admin(request, pk):
    
    if request.method == 'GET':
        return render(request, 'aplicacion/pruebas.html')
    
    if request.method == 'POST':
        
        persona = User.objects.get(id = pk)
        persona.delete()

    return render(request,'aplicacion/pruebas.html')


# FUNCION QUE LISTARÁ LAS VENTAS
def listar_venta(request):
    ventas = Ventas.objects.all()
    contexto = {
        'form' : ventas
    }
    return render(request, 'crearusuario.html', contexto)

#FUNCION QUE CREARÁ UNA VENTA
def crear_venta(request):
    
    if request.method == 'GET':
        ventas = Ventas.objects.filter()
        productos = Producto.objects.all()
        clientes = User.objects.all()
        
        contexto = {
            'form' : ventas,
            'form2': productos,
            'form3': clientes
        }
    
    if request.method == 'POST':
        
        ventas = VentasForm(request.POST)
        
        contexto =   {
            'form' : ventas
        }
        if ventas.is_valid():
            ventas.save()
    
    return render(request, 'aplicacion/pruebas.html', contexto)

#FUNCION QUE EDITARÁ UNA VENTA
def editar_venta(request, pk):
    consulta = Ventas.objects.get(id = pk)
    
    if request.method == 'GET':
        
        ventas = VentasForm(instance = consulta)
        contexto = {
            'form' : ventas
        }
    elif request.method == 'POST':
        
        ventas = VentasForm(request.POST, instance = consulta)
        
        print(ventas)
        contexto = {
        'form' : ventas
        }
        if ventas.is_valid():
            ventas.save()
    return render(request, 'aplicacion/pruebas.html', contexto)

#FUNCION QUE ELIMINARÁ UNA VENTA
def eliminar_venta(request, pk):
    
    if request.method == 'GET':
        return render(request, 'aplicacion/pruebas.html')
    
    if request.method == 'POST':
        
        persona = Ventas.objects.get(id = pk)
        persona.delete()

    return render(request,'aplicacion/pruebas.html')

#FUNCION BUSCAR VENTA POR EMAIL
def buscar_venta(request):
    consulta = request.GET.get('q')  # Obtener el término de búsqueda de la URL
    
    if consulta:
        # Realizar la búsqueda de productos por nombre
        ventas = Ventas.objects.filter(idCliente__email=consulta)
        
    else:
        ventas = Ventas.objects.all()  # Mostrar todos los productos si no se especifica una búsqueda
    
    return render(request, 'crud/buscarproducto.html', {'productos': ventas, 'Busqueda': consulta})

def boleta(request):
    user_metadata = User.objects.get(id=request.user.id)
    consulta = Orden_de_compra.objects.filter(users_metadata=user_metadata).get()
    carrito = Orden_de_compra_detalle.objects.filter(id_orden_compra=consulta)
    print(carrito)
    return render(request, 'tienda/boleta.html', {'carritoss': carrito})

def salioMal(request):
    return render(request, 'tienda/algoSalioMal.html')

def Acumulacion_puntos(request):
    
    if request.method == 'GET':
        
        user_metadata = User.objects.get(id=request.user.id)
        user_id = user_metadata.id
        
        datos = Carrito.objects.filter(users_metadata = user_id).order_by('id').all()
        
        suma = 0
    
        for dato in datos:
            valor = dato.cantidad * dato.producto.precio
            suma = suma + valor
            
        puntos = round(suma * 0.03)

        return render(request, 'aplicacion/checkout.html', {'puntos': puntos})
    
    
    

def productos_detalle(request, pk):
    try:
        datos = Producto.objects.filter(id = pk).filter(activo = 1).get()
        productos_relacionados = Producto.objects.exclude(id=pk)[:4]
    except Producto.DoesNotExist:
        raise Http404
    return render(request, 'tienda/detalleprod.html', {'datos': datos, 'productos_relacionados': productos_relacionados})

def checkout(request):
    
    user_metadata = User.objects.get(id=request.user.id)
    user_id = user_metadata.id
    
    datos = Carrito.objects.filter(users_metadata = user_id)
    rango = [1,2,3,4,5,6,7,8,9,10]
    
    datos = Carrito.objects.filter(users_metadata = user_id).order_by('id').all()
        
    suma = 0
    
    for dato in datos:
        valor = dato.cantidad * dato.producto.precio
        suma = suma + valor
            
    puntos = round(suma * 0.03) 
    
    return render(request, 'tienda/checkout.html', {'datos' : datos, 'rango' : rango, 'puntos': puntos})

@login_required()
def carro_inicio(request):
    
    cuantos = Carrito.objects.filter(users_metadata = request.session['users_metadata_id']).count()
    datos = Carrito.objects.filter(users_metadata = request.session['users_metadata_id']).order_by('id').all()
    suma = 0
    
    for dato in datos:
        valor = dato.cantidad * dato.producto.precio
        suma = suma + valor
        
    return render(request, '/carro/', {'datos': datos, 'suma': suma, 'cuantos': cuantos})    

@login_required() 
def carro_crear(request):
    
    if request.method == 'POST':
        try:
            datos = Producto.objects.filter(id = request.POST['id']).get()
        except Producto.DoesNotExist:
            raise Http404
        
        user_metadata = User.objects.get(id=request.user.id)
        user_id = user_metadata.id
        
        Carrito.objects.create(cantidad = request.POST['cantidad'],
                               producto = Producto.objects.get(id = request.POST['id']),
                               users_metadata = User.objects.get(id = user_id))
        return HttpResponseRedirect("/carro/")
    else:
        raise Http404
    

@login_required()    
def carro_vaciar(request):
    
    Carrito.objects.filter(users_metadata=request.user.id).delete()
    Orden_de_compra.objects.filter(users_metadata = request.user.id).delete()
    
    return HttpResponseRedirect("/checkout/")


@login_required()
def ejemplo(request, pk):
    print("LLEGUE AKI")
    
    if request.method == 'GET':
        print("LLEGUE AL GET")
        user_metadatas = User.objects.get(id=request.user.id)
        user_id = user_metadatas.id
        print(pk)
        x = Carrito.objects.filter(producto = pk).get()
        print(x)
    
    return HttpResponseRedirect('/checkout/')
        

@login_required()
def carro_quitar(request, pk):
    user_metadata = User.objects.get(id=request.user.id)
    user_id = user_metadata.id
    
    if request.method == 'GET':
        try:   
            datos = Producto.objects.filter(id = pk).get()
            print("CARRO QUITAR")
        except Producto.DoesNotExist:
            raise Http404
        print("CARRO QUITAR")
        Carrito.objects.filter(users_metadata = user_id).filter(producto = pk).delete()
    
    return HttpResponseRedirect("/checkout/")

@login_required()
def carro_modificar_cantidad(request, pk , cantidad):
    try:
        datos = Carrito.objects.filter(id = pk).get()
    except Carrito.DoesNotExist:
        raise Http404
    Carrito.objects.filter(id = pk).update(cantidad = cantidad)
    return HttpResponseRedirect('/checkout/')

@login_required()
def carro_pagar(request):
    
    user_metadata = User.objects.get(id=request.user.id)
    user_id = user_metadata.id
    
    cuantos=Carrito.objects.filter(users_metadata=user_id).count()
    if cuantos==0:
        return HttpResponseRedirect('/carro')
    datos=Carrito.objects.filter(users_metadata=user_id).order_by('-id').all()
    
    suma=0
    for dato in datos:
        valor=dato.cantidad*dato.producto.precio
        suma=suma+valor
    usuario = User.objects.filter(id=user_id).get()
    
    cliente = Clientes.objects.filter(idUser=usuario.id).get()
    
    return render(request, 'tienda/pagar.html', {'datos': datos, 'suma': suma, 'usuario': usuario, 'cuantos': cuantos, 'cliente': cliente})


#-------------------------------------WEBPAY----------------------------------------------

@login_required()
def carro_webpay(request):
    
    user_metadata = User.objects.get(id=request.user.id)
    user_id = user_metadata.id
    
    if request.method =='POST':
        cuantos=Carrito.objects.filter(users_metadata_id=user_id).count()
        if cuantos==0:
            return HttpResponseRedirect('/carro')
        result=crearTransaccion(user_id)
        return render(request, 'tienda/webpay.html', {'url': result['url'], 'token': result['token']})


@login_required()
def carro_webpay_respuesta(request):
    
    user_metadata = User.objects.get(id=request.user.id)
    user_id = user_metadata.id
    
    if not request.GET.get('token_ws'):
        print("ERROR EN EL TOKEN")
        return HttpResponseRedirect('/salioMal/')
    token=request.GET.get('token_ws')
    result=verificarTransaccion(token)
    #return render(request, 'carro/webpay_respuesta.html', {'result': result[0]})
    #return HttpResponse(result[0])
    if result[0]=='vacio':
        print("ERROR VACIO")
        return HttpResponseRedirect('/salioMal/')
    if result[0]=='AUTHORIZED':
        try:
            orden =Orden_de_compra.objects.filter(users_metadata_id = user_id, estado_transbank = 0).get()
            print(type(orden))
            print(orden)
        except Orden_de_compra.DoesNotExist:
            print("ERROR en el orden")
            return HttpResponseRedirect('/salioMal/')
        Orden_de_compra.objects.filter(users_metadata=user_id, estado_transbank=0).update(token_ws= token, estado_transbank=result[0], fecha_transbank=result[2], tarjeta=result[1])
        suma=0
        datos=Carrito.objects.filter(users_metadata=user_id).all()
        
        detalle=""
        for dato in datos:
            valor = dato.cantidad * dato.producto.precio
            suma = suma + valor
            detalle=f"""{detalle}
            <tr>
                <td style="border: 1px solid black;">
                    </td>
                    <td style="border: 1px solid black;">{dato.producto.nombre}s</td>
                    <td style="border: 1px solid black;">{dato.cantidad}</td>
                    <td style="border: 1px solid black;">${utilidades.numberFormat(dato.producto.precio)}</td>
            </tr>
             """
            user_metadata2 = User.objects.get(id=request.user.id)
            producto = Producto.objects.get(id=dato.producto.id)
            Orden_de_compra_detalle.objects.create(id_orden_compra = orden, id_producto=dato.producto, cantidad=dato.cantidad)
            Boleta.objects.create(producto = producto, user = user_metadata2, cantidad = dato.cantidad, precio_total = suma)
        
        Carrito.objects.filter(users_metadata=user_id).delete()
        usuario=Clientes.objects.filter(idUser=user_id).get()
        html=f"""
        <!DOCTYPE html>
                    <html>
                        <head>
                            <meta charset="utf-8" />
                            <title>el título de la página</title>
                            
                           
                    </head>
                        <div class="container">
                            <div class="row">
                                <h1>Hola {usuario}, tu pedido ha sido ingresado al sistema con el N°{orden.id}</h1>
                                <table style="border-collapse: collapse;">
                                    <thead>
                                        <tr>
                                            <th>*</th>
                                            <th>Producto</th>
                                            <th>Cantidad</th>
                                            <th>Precio</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {detalle}
                                        <tr>
                                            <td colspan="5" style="border: 1px solid black;">
                                                Total de tu compra
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="5" style="border: 1px solid black;">
                                                ${utilidades.numberFormat(suma)}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </html>
                """
        utilidades.sendMail(html, 'Tienda', usuario.email)
        utilidades.sendMail(html, 'Tienda', 'matiasgveloso@gmail.com')
       
        return HttpResponseRedirect('/boleta/')
    if result[0]=='FAILED':
        Orden_de_compra.objects.filter( users_metadata=user_id).filter(estado_transbank=0).update(token_ws= token, fecha_transbank=result[2], tarjeta=result[1])
        
        return HttpResponseRedirect('/salioMal/')    
    









    

    

        
