from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static
from .api import *
from .views import * 

#ORGANIZAMOS LAS URL DE LA APLICACION 
urlpatterns = [
    #URLS DE LAS API EN API.PY
    path('cliente/', clientes_api_view, name='cliente_api'),
    path('cliente/<int:pk>/', clientes_detail_view, name='cliente_detail_api'),
    path('administrador/', administrador_api_view, name='administrador_api'),
    path('administrador/<int:pk>/', administrador_detail_view, name='administrador_detail_api'),
    path('producto/', producto_api_view, name='producto_api'),
    path('producto/<int:pk>/', producto_detail_view, name='producto_detail_api'),
    path('tipoproducto/', tipoproducto_api_view, name='tipoproducto_api'),
    path('tipoproducto/<int:pk>/', tipoproducto_detail_view, name='tipoproducto_detail_api'),
    path('ventas/', ventas_api_view, name='ventas_api'),
    path('ventas/<int:pk>/', ventas_detail_view, name='ventas_detail_api'),

    
    #URLS DE LAS FUNCIONES EN VIEWS.PY
    path('', home  , name='Home'),
    path('nosotros/', nosotros  , name='Nosotros'),
    path('carro/', carro  , name='carro'),
    path('checkout/', checkout  , name='checkout'),
    path('catalogo/', catalogo  , name='Catalogo'),
    path('contacto/', contacto  , name='contacto'),
    path('Base/', Base  , name='Base'),
    path('detalleprod/<int:producto_id>/', detalleprod, name='detalleprod'),
    path('editarusuario/', editarUsuario  , name='EditarUsuario'),


    #URLS DE LAS FUNCIONES EN PRODUCTOS
    path('crearproducto/', crear_producto, name='crearproducto'),
    path('productos/', listar_productos  , name='Productos'),
    path('editarproducto/<int:id>/', editar_producto  , name='editarproducto'),
    path('eliminarproducto/<int:id>/', eliminar_producto, name='eliminarproducto'),
    path('buscarproducto/', buscarproducto, name='buscarproducto'),
  
    #URLS DE LAS FUNCIONES EN TIENDA
    path('tienda/', tienda, name='tienda'),

    #URLS DE LAS FUNCIONES DEL USUARIO
    path('iniciarsesion/', iniciar_sesion, name='Iniciosesion'),
    path('listarusuario/', listar_usuario, name='listarusuario'),
    path('deslogear/', deslogear, name='deslogear'),
    path('crearusuario/', crear_usuario, name='crearusuario'),
    path('editarusuario/<int:pk>/', editar_usuario, name='editarusuario'),
    path('eliminarusuario/<int:pk>/', eliminar_usuario, name='eliminarusuario'),
    
    #URLS DE LAS FUNCIONES DE CATEGORIAS(TIPOPRODUCTO)
    path('listarcategoria/', listar_categoria, name='listarcategoria'),
    path('crearcategoria/', crear_categoria, name='crearcategoria'),
    path('editarcategoria/<int:pk>/', editar_categoria, name='editarcategoria'),
    path('eliminarcategoria/<int:pk>/', eliminar_categoria, name='eliminarcategoria'),
    
    #URLS DE LAS FUNCIONES DEL ADMINISTRADOR
    path('listaradmin/', listar_admin, name='listaradmin'),
    path('crearadmin/', crear_admin, name='crearadmin'),
    path('editaradmin/<int:pk>/', editar_admin, name='editaradmin'),
    path('eliminaradmin/<int:pk>/', eliminar_admin, name='eliminaradmin'),
    
    #URLS DE LAS FUNCIONES DE VENTAS
    path('buscarventa/', buscar_venta, name='buscarventas'),
    path('listarventas/', listar_venta, name='listarventas'),
    path('crearventa/', crear_venta, name='crearventas'),
    path('editarventa/<int:pk>/', editar_venta, name='editarventas'),
    path('eliminarventa/<int:pk>/', eliminar_venta, name='eliminarventas'),
    
    #PRUEBA CARRITO DETALLE
    path('Acumulacion_puntos/', Acumulacion_puntos, name='acumulacion_puntos'),
    path('detalle/<int:pk>/', productos_detalle, name='productos_detalle'),
    path('crear/', carro_crear, name='carro_crear'),
    path('vaciar/', carro_vaciar, name='carro_vaciar'),
    path('modificar-cantidad/<int:pk>/<int:cantidad>/', carro_modificar_cantidad, name='carro_modificar_cantidad'),
    path('ejemplo/<int:pk>/', ejemplo, name='ejemplo'),
    path('carro_quitar/<int:pk>/', carro_quitar, name='carro_quitar'),
    path('pagar', carro_pagar, name="carro_pagar"),
    path('webpay', carro_webpay, name="carro_webpay"),
	path('carro/webpay-respuesta', carro_webpay_respuesta, name="carro_webpay_respuesta"),
    path('boleta/', boleta, name="boleta"),
    path('salioMal/', salioMal, name="salioMal"),
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


