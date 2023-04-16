import streamlit as st
import socket
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
from threading import Thread

#diseño de la página
st.set_page_config(page_title = 'SDR-ASR', page_icon=':radio:')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#contenedor para mostrar encabezado en la página
h_container = st.container()
h_container.style.justify_content = 'center'
with h_container:
    st.image('image.png', use_column_width='always')
    st.markdown("<h1 style = 'text-align: center;'>Captura de señales FM y Reconocimiento de Voz</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style = 'text-align: center;'> En Vivo ● </h3>", unsafe_allow_html=True)
#contenedor para mostrar el texto en la página
t_container = st.empty()

#socket GNU Radio + Python
IP_ = "127.0.0.1"
PORT_ = 50868
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #para UDP: socket.SOCK_DGRAM; para TCP: socket.SOCK_STREAM
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #for UDP
#client.connect((IP_, PORT_)) #for TCP
client.bind((IP_, PORT_)) #for UDP
client.settimeout(0.7)

#variable string global que se mostrará en la página web
text = ""

#conversión de audio a texto
def speech():
    global text
    comparador = ""
    while True:
        try: 
            #lectura del archivo wav
            with sr.AudioFile(archivo) as source:
                audio = r.record(source)

            text = r.recognize_google(audio, language='es-MX') #hacer que esto no se imprima en consola
            #imprimiendo texto sin repetir en consola
            if(text != comparador):
                print(text)
                comparador = text
        except:
            print("...")

#ejecución del método speech en simultáneo
thread = Thread(target=speech)
thread.daemon = True
thread.start()

#Array donde se concatena la data
msg = np.array([0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0])
#Array base para eliminar data vieja
msg0 = np.array([0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0])

#variable booleana para salir del ciclo while
llave = True

#ruta en la que se guardará el archivo wav de la data recibida de gnuradio
#cambia esta ruta según en dónde se encuentre la carpeta clonada del repositorio.
archivo = '/home/popuser/Desktop/SDR-ASR/app/outgnu.wav'
#samp_rate gnuradio
fs = 48000
#volume
volume = 30000
#objeto para utilizar la api de google
r = sr.Recognizer()

count = 0
#recepción de data de gnuradio
while llave:
    try:
        data = client.recv(4096) #tamaño del bus, 4096 para UDP, 1024 para TCP, se recomienda que sea una potencia de 2ʌn
        datas = np.frombuffer(data, dtype=np.complex64, count=-1) #decodificando data
        msg = np.concatenate((msg, datas)) #creación de un arreglo significante de datos

        if(msg.shape[0] > 200000): #200000  120000  15000
            max_value = np.max(np.abs(msg))
            data_to_write = msg*(volume/max_value) # ajustar escala audible
            write('outgnu.wav', fs, data_to_write.astype(np.int16)) #generando archivo wav

            #imprimiendo texto final en la página web
            with t_container.container():
                st.markdown("### "+ text)
            #eliminando data vieja
            msg = msg0
    except socket.timeout:
        #si se cierra gnuradio, finaliza el ciclo while
        llave = False