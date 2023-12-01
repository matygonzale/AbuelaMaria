from django import template
from aplicacion.models import Carrito
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


register = template.Library()


@register.filter(name='getCuantosItemsHayEnCarro')  
def getCuantosItemsHayEnCarro(pk):
    cuantos = Carrito.objects.filter(users_metadata = pk).count()
    
    if cuantos == 0:
        return ""
    elif cuantos == 1:
        return f""" <span class='badge bg-dark text-white ms-1 rounded-pill' id='lblCartCount'>{cuantos}</span>
            <div>ítem</div>"""
    else:
        return f""" <span class='badge bg-dark text-white ms-1 rounded-pill' id='lblCartCount'>{cuantos}</span>
            <div>ítem</div>"""
            

def numberFormat(numero):
    if numero == None:
        return 0
    else:
        return "{:,}".format(numero).replace(",",".")
    
    
def sendMail(html, asunto, para):
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = settings.MAIL_SALIDA
    msg['To'] = para

    msg.attach(MIMEText(html, 'html'))
    try:
        server = smtplib.SMTP(settings.SERVER_STMP, settings.PUERTO_SMTP)
        server.login(settings.MAIL_SALIDA, settings.PASSWORD_MAIL_SALIDA)
        server.sendmail(settings.MAIL_SALIDA, para, msg.as_string())
        server.quit()
    except smtplib.SMTPResponseException as e:
        pass
    

@register.filter(name='multiplicarValores')
def multiplicarValores(valor1, valor2):
    return valor1*valor2


@register.filter(name='numberFormat')
def numberFormat(numero):
    if numero == None:
        return 0
    else:
        return "{:,}".format(numero).replace(",",".")