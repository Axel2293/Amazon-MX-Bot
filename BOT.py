from tkinter import *
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from tkinter import ttk
#---------LIB personal para la modificaion del archivo de precio--------------------#
from LIB_Read_Write import *
#---------LIB personal con el servicio SMTP para enviar correos---------------------#
from servicio_email import *


#---------------------HEADER PARA EL WEB SCRAPING-----------------------------------#
HEADER={
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'
    }

#---------------------SESION DE HTML------------------------------------------------#
s=HTMLSession()

#---------------------DECLARACION DE VARIABLES Y BOLEANOS---------------------------#
t_f=False
linkproducto=""
bol_link=False
first_run=False
validacion_correo=False


#*******************************FUNCIONES DEL BOT***************************************#
#--------------------VERIFICACION DEL LINK Y RETORNO DEL MISMO--------------------------#

def get_link():
    global linkproducto, bol_link
    linkproducto=linkentrada.get()
    if  "https://www.amazon.com.mx/" in linkproducto: 
        link_muestra.config(text='LINK VALIDO',bg='#0080FF',fg='#FFFFFF')
        linkentrada.config(foreground='#0080FF')
        bol_link=True
        link_detectado.config(text='Link detectado (Amazon)\nUsa Recargar para cargar los datos o inicia el BOT')
        return linkproducto
        #si el link es valido
    else:
        link_muestra.config(text='Link incorrecto', bg='#FF0000',fg='#FFFFFF')
        nombre_producto_var.set('LINK INVALIDO')  
        linkentrada.config(foreground='#990000')
        bol_link=False
        #en caso de que sea invalido

#--------------------OBTENCION DE PRECIO Y NOMBRE DEL PRODUCTO--------------------------#
def get_price(url):
    global precio_actual
    r=s.get(url,headers=HEADER)
    r.html.render(timeout=20)
    soup=BeautifulSoup(r.html.html, 'html.parser')
    #obtenemos los datos de la pagina amazon parseados en html y ls guardamos en soup
    try:
        price = soup.find(class_="a-offscreen").get_text()
        p_t= soup.find(class_="a-size-large product-title-word-break").get_text()
        price=price.replace('$','')
        price=price.replace(',','')
        price=price.strip()
        p_t=p_t.strip()
        #limpieza del precio y nombre
        print("Precio en get_price ", price)
        precio_actual.set(price)
        nombre_producto_var.set(p_t)
        return(price)
    except:
        precio_actual.set("Al parecer hubo un error :(, puedes esperar unos minutos antes de volver a iniciar")
    # Catch error en caso de que amazon regrese un HTML sin el precio o un cierre de conexion
#--------------------FUNCIONALIDAD PRINCIPAL BOT----------------------------------------#
def main(linkprducto):
    
    estado_lab.config(text='-BOT CORRIENDO-')
    get_link()
    if bol_link is True:
        try:
            newprice=get_price(get_link())
            error_msj_var.set('')
            print("Precio en main ", newprice)
            try:
                open('Price.txt')

            except FileNotFoundError:
                mensaje_var.set("Archivo no encontrado, creando uno nuevo")
                print('Creando archivo')
                writefile(newprice)
            #Catch error en caso de que no exista el archivo .txt
            oldprice= readfile()
            print('OLD: ',oldprice)
            print("NEW: ",newprice)
            if oldprice=="":
                writefile(newprice)
                oldprice=readfile()
            if float(newprice)<float(oldprice):
                message="Su producto ha sido rebajado a " + str(newprice) + " con una diferencia de " + str(float(oldprice)-float(newprice))
                #creamos mensaje con los datos para avisar de la reduccion de precio
                if validacion_correo is True:
                    sendemail(message, email_actual_var.get())
                    mensaje_var.set('El precio ha disminuido\n CORREO ENVIADO')
                    print("El precio ha disminuido\n CORREO ENVIADO")
                    #Enviamos correo si el usuario introdujo y verifico en la interfaz
                else:
                    mensaje_var.set('El precio ha disminuido\n CORREO NO CONFIGURADO')
                    print('El precio ha disminuido\n CORREO NO CONFIGURADO')
                    #si no se lo hacemos saber
                writefile(newprice)
            elif float(newprice)>float(oldprice):
                mensaje_var.set("El precio ha aumentado")
                writefile(newprice)
                # Si el precio aumenta
            else:
                mensaje_var.set("El precio sigue igual")
                #si sigue igual
        except:
            error_msj_var.set("--ERROR--\n Amazon probablemente detecto la actividad del BOT\n Espera unos minutos, te recomendamos que aumentes el tiempo de revision :)")
            print('error')
    elif bol_link is False:
        estado_lab.config(text='-Estado: Error(Link incorrecto)-')
    estado_lab.config(text='Durmiendo un rato -.-')

#--------------------DESACTIVAR ACTIVAR BOT---------------------------------------------#
def act_bot():
    global t_f, bol_link
    if bol_link is True:
        t_f=True
        boleano_bot.config(text='Boleano: TRUE')
        iniciarbot.config(state='disabled')
        apagarbot.config(state='active')
        refresh_precio.config(state='disabled')
        linkenviar.config(state='disabled')
        estado_lab.config(text='-BOT ENCENDIDO-')
        #configuracion de botones y estados en la interfaz
    else:
        mensaje_var.set('** Primero introduce un Link valido antes de iniciar **')
        #en caso de que el usuario todavia no haya verificado el link a hacer seguimiento
def des_bot():
    global t_f, first_run
    if t_f is True:
        t_f=False
        first_run=False
        boleano_bot.config(text='Boleano: FALSE')
        apagarbot.config(state='disabled')
        iniciarbot.config(state='active')
        refresh_precio.config(state='active')
        linkenviar.config(state='active')
        estado_lab.config(text='-BOT APAGADO-')
        nombre_producto_var.set('Introduce otro producto para obtener el nombre')
        precio_actual.set('Introduce otro producto para obtener el precio')

        open('Price.txt')
        writefile("0")

#--------------------FUNCION DE VERFIFICACION DE ENCENDIDO Y ACTIVACION DEL BOT---------#
def ver_onoff():
    global t_f
    if t_f is True:
        error_msj_var.set('')
        main(get_link())
    elif t_f is False:
        estado_lab.config(text='-BOT APAGADO-')
    raiz.after(select_time.get(), ver_onoff)
    print(select_time.get(), "ms")
    # este apartado detecta cuando el usuario haya activado el bot y comienza a activar el Bot
#--------------------PRIMER CHECK  CUANDO EL USUARIO PRESIONA INICIAR BOT---------------#
def first_check():
    global first_run, t_f, bol_link
    if first_run is False and t_f is True:
        get_link()
        if bol_link is True: 
            main(get_link)
            first_run=True
        elif bol_link is False:
            estado_lab.config(text='-Estado: Error(Link incorrecto)-')
    # esta funcion es para encargarse de la primera vez que funciona el bot debido a que si no hay este
    #apartado el bot iniciara hasta despues del tiempo especificado

#--------------------PRECIO y NOMBRE PARA MOSTRAR EN LA INTERFAZ------------------------#
def precio_pantalla():
    if bol_link is True:
        get_price(get_link())
    else:
        nombre_producto_var.set('Introduce un link valido primero :)')
    # para obtener datos sin tener que activar el bot
#--------------------VERIFICACION CORREO------------------------------------------------#
def verif_correo():
    global validacion_correo
    validacion_correo= False
    email=email_usuario_entrada.get()
    dicEmail={
        0:'@gmail.com',
        1:'@outlook.com',
        2:'@icloud.com',
        3:'@iteso.mx'
    }
    #diccionario con los correos admitidos
    for i in range(len(dicEmail.keys())):
        if dicEmail[i] == email[-len(dicEmail[i]):]:
            validacion_correo=True
            email_actual_var.set(email)
            break
    if validacion_correo is True:
        email_verificacion_estatus.config(text='CORREO VALIDO',bg='#0080FF',fg='#FFFFFF')
    elif validacion_correo is False:
        email_verificacion_estatus.config(text='CORREO INVALIDO',bg='#FF0000',fg='#FFFFFF')

    #Verificacion para cuatro dominios de correo mediante las posiciones de la cadena introducida

#--------------------VERIFICACION DEL TIEMPO SELECCIONADO POR EL USUARIO PARA ACTIVAR EL BOT------------------------------------------------#
def check_time():
    raiz.after(select_time.get(), ver_onoff)
#chequeo principal para mantener el funcionamiento del bot des pues de el tiempo seleccionado

#*****************************INICIO DE LA INTERFAZ***********************************************
raiz= Tk()
raiz.title('Amazon price tracker')
raiz.config(
    width=950, 
    height=700)

#--------------------TEMA (AZURE)---------------#
style = ttk.Style(raiz)
raiz.tk.call('source', 'azure.tcl')
style.theme_use('azure')

#--------------------VARIABLES------------------#
precio_actual=StringVar()
nombre_producto_var=StringVar()
mensaje_var=StringVar()
email_actual_var=StringVar()
error_msj_var=StringVar()
email_actual_var.set('-EMAIL ACTUAL-')

#---------------------LINK------------------------------------------------#
frame_link=ttk.LabelFrame(
    raiz, 
    text='Link', 
    width=400, 
    height=150)
frame_link.place(x=20, y=12)

link=ttk.Label(
    frame_link, 
    text='Link del producto:')
link.place(x=20, y=20)

linkentrada=ttk.Entry(
    frame_link)
linkentrada.place(x=130, y=15)

linkenviar=ttk.Button(
    frame_link, 
    text='Verificar', 
    command=get_link)
linkenviar.place(x=280, y=15)

link_estado=ttk.Label(
    frame_link, 
    text='Verificación:')
link_estado.place(x=20, y=50)

link_muestra=Label(
    frame_link, 
    text='')
link_muestra.place(x=130, y=50)

link_detectado=ttk.Label(
    frame_link, 
    text='')
link_detectado.place(x=20, y=80)

#------------------------DATOS DEL PRODUCTO------------------------------------#
frame_producto=ttk.LabelFrame(
    raiz, 
    text='Producto seleccionado', 
    width=400, 
    height=200)
frame_producto.place(x=450, y=12)

nombre_producto=ttk.Label(
    frame_producto, 
    textvariable=nombre_producto_var)
nombre_producto.place(x=20, y=20)

precio_producto=ttk.Label(
    frame_producto, 
    textvariable=precio_actual)
precio_producto.place(x=20, y=100)

refresh_precio=ttk.Button(
    frame_producto, 
    text='Recargar', 
    command=precio_pantalla)
refresh_precio.place(x=20, y=130)

#----------------------------------BOT-----------------------------------------#
frame_bot=ttk.LabelFrame(
    raiz, 
    text='BOT', 
    width=145, 
    height=120)
frame_bot.place(x=20, y=170)

iniciarbot=ttk.Button(
    frame_bot, 
    text='Iniciar bot',
    command=lambda:[act_bot(), first_check()])
iniciarbot.place(x=20, y=15)

apagarbot=ttk.Button(
    frame_bot, 
    text='Apagar bot', 
    command=des_bot)
apagarbot.place(x=20, y=50)

#---------------------------------ESTADO BOT------------------------------------#
frame_estadobot=ttk.LabelFrame(
    raiz, 
    text='Estado-BOT', 
    width=240, 
    height=120)
frame_estadobot.place(x=180, y=170)

estado_lab=ttk.Label(
    frame_estadobot, 
    text='*ESTADO BOT*')
estado_lab.place(x=20, y=20)

boleano_bot=ttk.Label(
    frame_estadobot, 
    text='-BOLEANO BOT-')
boleano_bot.place(x=20, y=60)

#----------------------------------MENSAJES--------------------------------------#
frame_mensajes=ttk.LabelFrame(
    raiz,
    text='Mensajes del BOT',
    width=400,
    height=120)
frame_mensajes.place(x=20,y=300)

mensaje_bot=ttk.Label(
    frame_mensajes, 
    textvariable=mensaje_var)
mensaje_bot.place(x=20, y=20)

error_msj=ttk.Label(
    frame_mensajes, 
    textvariable=error_msj_var)
error_msj.place(x=20, y=40)

#----------------------------DATOS USUARIO-----------------------------------------#
frame_usuario=ttk.LabelFrame(
    raiz, 
    text='Tus datos',
    width=400, 
    height=200)
frame_usuario.place(x=450, y=220)

email_usuario=ttk.Label(
    frame_usuario, 
    text='Tu email')
email_usuario.place(x=20, y=20)

email_usuario_entrada=ttk.Entry(
    frame_usuario,
    width=35)
email_usuario_entrada.place(x=20, y=50)

email_verificar=ttk.Button(
    frame_usuario, 
    text='Verificar',
    command=verif_correo)
email_verificar.place(x=300, y=50)

email_verificacion_estatus=Label(
    frame_usuario, 
    text='-ESTATUS DE EMAIL-')
email_verificacion_estatus.place(x=20, y=100)

email_actual=Label(
    frame_usuario, 
    textvariable=email_actual_var)
email_actual.place(x=20, y=120)

#----------------------------Frame de config--------------#
frame_config=ttk.LabelFrame(
    raiz,
    width=180, 
    height=100, text='Configuracion')
frame_config.place(x=20, y=450)

ms_gui=ttk.Label(
    frame_config, 
    text='Tiempo de revision del BOT \n(ms, default : 1000 ms)')
ms_gui.place(x=20, y=10)

tiempos=[1000,60000,900000,1800000,3600000]
select_time=ttk.Combobox(frame_config, values=tiempos,width=9)
select_time.current(0)
select_time.place(x=20, y=50)

#---------------------------DEV-------------------------
dev=ttk.LabelFrame(
    raiz,
    width=150, 
    height=100, text='DEV TEST')
dev.place(x=250, y=450)
email_prueba=""
email_template='Esto es un Email de prueba'

email_test=ttk.Button(
    dev, 
    text='Enviar EMAIL', command=lambda:[sendemail(email_template, email_prueba)])
email_test.place(x=20, y=20)

print(select_time.get())


#-----------Verificar si el usuario inicio el bot---------#
raiz.after(1000, check_time)

#--------------------CICLO DE LA INTERFAZ-----------------#
raiz.mainloop()







