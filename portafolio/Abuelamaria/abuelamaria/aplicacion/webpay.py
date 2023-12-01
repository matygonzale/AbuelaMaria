import requests
import json
import random
from django.conf import settings
from .models import *

def crearTransaccion(user_id):
	#se crea la orden de compra
	
	instancia = User.objects.filter(id = user_id).get()
	
	datos=Carrito.objects.filter(users_metadata=instancia).order_by('-id').all()
	suma=0
 
	for dato in datos:
		valor=dato.cantidad*dato.producto.precio
		suma=suma+valor
	
	
	try:
		orden=Orden_de_compra.objects.filter(users_metadata= instancia).get()
	except Orden_de_compra.DoesNotExist:
		orden=Orden_de_compra.objects.create(users_metadata= instancia, monto=suma)

	buy_order = f"orden{orden.id}"
	session_id = str(random.randrange(1000000, 99999999))
	amount = suma
	ruta=f"{settings.BASE_URL}carro/webpay-respuesta"
	endpoint=settings.WEBPAY_URL
	payload={
		 "buy_order": buy_order,
		 "session_id": session_id,
		 "amount": amount,
		 "return_url": ruta
		}
	cabeceros = {'content-type': 'application/json', 'Tbk-Api-Key-Id': settings.WEBPAY_ID, 'Tbk-Api-Key-Secret': settings.WEBPAY_SECRET}
	response= requests.post(endpoint, json=payload, headers=cabeceros)
	#response.status_code
	respuesta=json.loads(response.text)
	#guardo el token recibido
	Orden_de_compra.objects.filter(id=orden.id).update(token_ws=respuesta['token'])
	#retorno token y URL
	ruta=f"{respuesta['url']}{respuesta['token']}"
	return respuesta


def verificarTransaccion(token):
	endpoint=f"{settings.WEBPAY_URL}/{token}"
	cabeceros = {'content-type': 'application/json', 'Tbk-Api-Key-Id': settings.WEBPAY_ID, 'Tbk-Api-Key-Secret': settings.WEBPAY_SECRET}
	response= requests.put(endpoint, headers=cabeceros)
	#response.status_code
	respuesta=json.loads(response.text)
	if response.status_code ==200:
		return [respuesta['status'], respuesta['card_detail']['card_number'], respuesta['transaction_date']]
	else:
		return ['vacio']