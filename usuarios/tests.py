import smtplib
from django.test import TestCase
from django.core.mail import send_mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from comisionManager import settings
from django.template.loader import render_to_string
from usuarios.models import User


email_destino = "germanv09@gmail.com"

html = render_to_string('registro/email_pass.html',
                        {'user': User.objects.get(pk=1)})


def send_email():
    try:
        # Establecemos conexion con el servidor smtp de gmail
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mailServer.starttls()
        mailServer.login(settings.EMAIL_HOST_USER,
                         settings.EMAIL_HOST_PASSWORD)

        # Construimos el mensaje simple
        mensaje = MIMEMultipart('alternative')
        part = MIMEText(html, 'html')
        mensaje.attach(part)
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_destino
        mensaje['Subject'] = "Restablecer contraseña"

        # Envio del mensaje
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            email_destino, mensaje.as_string())

        print("Correo enviado")

    except Exception as e:
        print(e)


send_email()
