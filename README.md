# Amazon-MX-Bot
Amazon MX Price Tracker
# About
Este proyecto lo realice como parte del proyecto final de mi curso de programación, realmente me gusto realizarlo y aprendi bastante 
sobre temas que siempre quise desarrollar, como lo es la interfaz gráfica.


Si alguien requiere del uso de este programa o lo quiere modificar a su gusto me parece perfecto, obviamente si lo copian para su propio
 beneficio por lo menos denme creditos de lo que mi poco nivel logró XD. Cualquiere cosa que puedan detectar que pueda mejorar,
me lo pueden hacer llegar y estare infinitamente agradecido con ustedes.


# Important

***Rango de tiempo alto para evitar bloqueos por parte de Amazon (Recomiendo mantenerlo en media hora)

***Siempre pongan como raiz al ejecutar en terminal la carpeta en donde esten todos los archivos, al parecer 
la utilizacion de un tema en Tkinter complica bastante las cosas.

***Recuerda que si quieres hacer uso de la notificacion email tienes que entrar al archivo "servicio_email.py" 
e introducir tus datos en los campos de email y password, estos datos los usara el protocolo SMTP para logear sesion 
y poder enviar el correo desde esa cuenta. Hay que tener habilitado el acceso a este tipo de acciones desde la 
configuracion de tu correo.

***Existe un problema de procesamiento al momento de correr el bot, en futuras actualizaciones se corregira para 
impremeltar el multi-threading y ese lag al obtener el precio desaparezca. Si sucede cuando el bot está trabajando, 
no te asustes, es normal, en cuanto se obtengan los datos, se te volvera a permitie el manejo del programa.

# Libraries

Instala esto para que el programa ejecute sin problemas---->  "requests_html" y "bs4"

Puedes usar el comando pip en terminal para que no tengas problemas

--pip install bs4
--pip install requests_html


Las demas librerias ya vienen incluidas en Python, como Tkinter y SMTP
