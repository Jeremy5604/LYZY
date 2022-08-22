from datetime import datetime
import speech_recognition as sr #Clase para escuchar comandos de voz
import pyttsx3  #Clase para que Leasy responda con palabras verbales
import pywhatkit    #Clase para abrir y reproducir videos de youtube
import wikipedia    #Clase para buscar información en wikipedia

name = "alexa"
# Ese nombre es provisional, para pruebas , su verdadero nombre es Leasy
tiempo = datetime.now() #tiempo toma el valor de un objeto datetime(hora,min,segundo en tiempo real)
sample_rate = 48000 # variable que sirve para controlar la tasa de muestra de audio
chunk_size = 32 #No me acuerdo :v

listener = sr.Recognizer() #listener toma el valor del objeto reconocedor de voz---
#-- este objeto contiene métodos importantes para el procesamiento de ordenes

engine = pyttsx3.init() # la variable engine toma el valor de objeto pyttsx3, el cual---
#--- es un objeto que reproduce sonidos, se usará como respuesta cuando Leasy necesite datos más---
#--- especificos o cuando no pueda procesar una orden


voices: object = engine.getProperty('voices') #Son las voces que puede utilizar Leasy, creo que---
#---existen 4 voces.


#A continuación usaré el método(setProperty) "poner propiedades", primero se indica la propiedad---
#--- y luego el valor a asignarle según el que corresponda

engine.setProperty('rate', 150) #Propiedad Velocidad = 150
engine.setProperty('volume', 10.0)#Propiedad Volummen = 10.0
engine.setProperty('voice', voices[0].id) #Propiedad Voz = Elena creo que se llamaba la morra---
#---Para ver las voces coloque un print dentro de un for e impriman los valores del arreglo voices[].id---
#--- la palabra "id" significa que estas llamando al nombre de la voz




# 1. Que se active con la palabra "LIZY "(microfono encendido)
#NOTA: Aún no esta programada para escuchar, luego ejecutar y poner en modo espera hasta que se le vuelva---
#---a llamar por su nombre, sino que el código a continuación corre, escucha, ejecuta y se queda ---
#---ejecutanto en segundo plano pero sin escuchar. HAY QUE ARREGLAR ESO 

#Aqui está el método principal, el cual es el único obligatoriamente(revisa línea final)
def iniciar():
    while True:# El while es para que nunca deje de ejecutarse una ves se encienda
        with sr.Microphone(sample_rate=sample_rate,
                           chunk_size=chunk_size) as source:
            talk("Escuchando...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            engine.runAndWait()
            try:
                global comando
                comando = listener.recognize_google(voice, language='es-PE')
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service;{0}".format(e))
            comandofinal = comando.lower()
            print(comandofinal)
        if name in comandofinal:
            talk("Hola Jeremy")
            # 2.Se le indica la acción(lee)
            order = lecturaOrden()
            # 3.Busca la acción
            print(order)
            # 4. La ejecuta(Vuelve al estado inicial)
            buscarAccion(order)
    # 5.Pendiente de llamada(Paso 1)


def lecturaOrden():
    with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
        engine.runAndWait()
        try:
            global orden
            orden = listener.recognize_google(voice, language='es-PE')
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service;{0}".format(e))
        ordenfinal = orden.lower()
        return ordenfinal


def buscarAccion(orden):
    if 'reproduce' in orden:
        music = orden.replace('reproduce', ' ')
        talk('Reproduciendo' + music)
        pywhatkit.playonyt(music)
    elif 'fecha' in orden:
        talk("Hoy es  " + str(tiempo.day) + " del mes  " + str(tiempo.month) + " del " + str(tiempo.year))
    elif 'hora' in orden:
        talk(" La hora es " + str(tiempo.hour) + " horas  con " + str(tiempo.minute) + " minutos ")
    elif 'busca' in orden:
        dato = orden.replace('busca', ' ')
        talk('Buscando ' + dato)
        informacion = wikipedia.summary(dato, 1)
        talk(informacion)
    elif 'buen dia' in orden or 'buen día' in orden:
        buenDia()
    else:
        talk('No se reconoció el comando')


def buenDia():
    if tiempo.hour >= 6 and tiempo.hour < 13:
        talk("Buenos días Jeremy")
    elif tiempo.hour >= 13 and tiempo.hour < 18:
        talk("Buenas tardes Jeremy")
    else:
        talk("Buenas noches Jeremy")

    talk("Hoy es  " + str(tiempo.day) + " del mes  " + str(tiempo.month) + " del " + str(tiempo.year))
    talk(" La hora es " + str(tiempo.hour) + " horas  con " + str(tiempo.minute) + " minutos y " + str(
        tiempo.second) + " segundos")


def talk(texto):
    engine.say(texto)
    engine.runAndWait()
    pass


def escuchando():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            talk("Escuchando...")
            voice = listener.listen(source)
            engine.runAndWait()
            rec = listener.recognize_google(voice)
            rec = rec.lower()
            print(rec)
            if name in rec:
                # Con la sgte línea se va a quitar el nombre de la cadena mensaje
                rec = rec.replace(name, ' ')
                print(rec)
    except:
        talk('Lo lamento Jeremy, hubo un error que se debe corregir')
    return rec


def runmusic():
    mensaje = escuchando()
    if 'reproduce' in mensaje:
        music = mensaje.replace('reproduce', ' ')
        talk('Reproduciendo' + music)
        pywhatkit.playonyt(music)
    elif 'hoy' in mensaje:
        talk("Hoy es  " + str(tiempo.day) + " del mes  " + str(tiempo.month) + " del " + str(tiempo.year))
    elif 'hora' in mensaje:
        talk(" La hora es " + str(tiempo.hour) + " horas  con " + str(tiempo.minute) + " minutos ")
    elif 'busca' in mensaje:
        dato = mensaje.replace('busca', ' ')
        talk('Buscando ' + dato)
        informacion = wikipedia.summary(dato, 1)
        talk(informacion)

    else:
        talk('No se reconoció el comando')


iniciar()
