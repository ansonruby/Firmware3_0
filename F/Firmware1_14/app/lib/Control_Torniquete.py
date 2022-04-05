# -*- coding: utf-8 -*-
import Control_Archivos
import Control_Ethernet
import time
import RPi.GPIO as GPIO #Libreria Python GPIO

Leer_TT                 = int(Control_Archivos.Leer_Archivo(30))
Borrar                  = Control_Archivos.Borrar_Archivo
Escrivir_Estados        = Control_Archivos.Escrivir_Estados
ID_Dispo                = Control_Archivos.ID

Serial                  = Control_Ethernet.ID_Tarjeta


#print ID_Dispo()
GPIO.setmode (GPIO.BOARD)
		# Entrada, Salida
Rele =   [37,38] #16, 19 #[21,23]
Tiempo_Torniquete=Leer_TT#0.5#2 #segundos de respuesta

for k in range(2):
    GPIO.setup(Rele[k], GPIO.OUT)

def Entrar():
    global Tiempo_Torniquete
    global Rele
    if Serial.find("CCCB") != -1: #Para dispotitos CCCB
        Borrar(38)

        #print Tiempo_Torniquete
        #print "¿000000040001?"
        Dato_Rele = "¿00000004000" + str(Tiempo_Torniquete) + "?"
        Escrivir_Estados(Dato_Rele,38);
        #print Dato_Rele

        #Escrivir_Estados("¿000000040001?",38);
    GPIO.output(Rele[0], GPIO.LOW)
    time.sleep(Tiempo_Torniquete)
    GPIO.output(Rele[0], GPIO.HIGH)

def Salir():
    global Tiempo_Torniquete
    global Rele
    if Serial.find("CCCB") != -1: #Para dispotitos CCCB
        Borrar(38)

        #print Tiempo_Torniquete
        #print "¿000000040101?"
        Dato_Rele = "¿00000004010" + str(Tiempo_Torniquete) + "?"
        Escrivir_Estados(Dato_Rele,38);
        #print Dato_Rele

        #Escrivir_Estados("¿000000040101?",38);
    GPIO.output(Rele[1], GPIO.LOW)
    time.sleep(Tiempo_Torniquete)
    GPIO.output(Rele[1], GPIO.HIGH)
# mantener cerrado
def Cerrado():
    global Rele
    if Serial.find("CCCB") != -1: #Para dispotitos CCCB
        Borrar(38)
        Escrivir_Estados("¿000000040300?",38);
    GPIO.output(Rele[0], GPIO.HIGH)# Entrada
    GPIO.output(Rele[1], GPIO.HIGH)# Salida

Cerrado()
