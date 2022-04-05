# -*- coding: utf-8 -*-

import serial
import os, time
import commands

import lib.Control_Archivos  as Ca

from serial import SerialException

import RPi.GPIO as GPIO #Libreria Python GPIO


GPIO.setmode (GPIO.BOARD)
        #chicharra
CC_Pin =   31
GPIO.setup(CC_Pin, GPIO.OUT)

GPIO.output(CC_Pin, GPIO.HIGH)


Leer		         = Ca.Leer_Led
Borrar		         = Ca.Borrar_Archivo
Escrivir_Estados         = Ca.Escrivir_Estados
Escrivir                 = Ca.Escrivir_Archivo
Leer_Estado              = Ca.Leer_Estado


# Enable Serial Communication
#res = commands.getoutput('ls /dev/ttyACM*')


Puerto_Serial = '/dev/ttyS0'
print Puerto_Serial

port = serial.Serial(Puerto_Serial, baudrate=9600, timeout=1)
#port = serial.Serial(Puerto_Serial, baudrate=57600, timeout=1)

"""
port =0

while True:

    #res = commands.getoutput('ls /dev/ttyACM*')
    res = commands.getoutput('/dev/ttyS0')
    print res#.find("/dev/ttyACM*")

    if res.find("/dev/ttyACM*") == -1:
        print 'abrir puerto'
        #port.close()
        port = serial.Serial(res, baudrate=9600, timeout=1)
        break


"""

#port = serial.Serial(res, baudrate=9600, timeout=1)
#port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
#port.write('Inofrmacion serial'+'\n\r')


Eliminar_antes=0
N_Cade=0
C_armar=''



QR =''
QR_antes =''
Tinicio =0
Tfin =0
Tdiferencia =0
TRepeticion = 2
#---------------------

def Log_QR():

    Contador = str(int(Leer_Estado(12))+1)
    print 'Log QR: '+ Contador
    Borrar(12)              # Borrar QR
    Escrivir(Contador,12)   # Guardar QR


def Leer_datos_SensorQR():

    global Eliminar_antes
    global N_Cade
    global C_armar
    global QR
    global QR_antes
    global B_sensor
    global Tinicio
    global Tfin
    global Tdiferencia
    global TRepeticion
    global port
    global res


    while True:

        try :
            #-------------------------------
            #Para dispotitos CCCB
            #-------------------------------
            rele = Leer_Estado(38)
            if len(rele)>= 1:
                print rele
                port.write(rele)
                Borrar(38)
            #-------------------------------


            rcv = port.read(250)

            #-----------------------------------------
            #       Analisis de Cadenas recojidas
            #-----------------------------------------
            T_rcv = len(rcv)
            #print T_rcv

            if T_rcv >= 1:

                QRT = rcv.split('\r')
                #print QRT

                for x in QRT:
                    #print 'x Procesando: '+x
                    N_Cade +=1

                    TaCadena = len (x)
                    Inicio = x[0:1]
                    Fin = x[TaCadena-1:TaCadena]

                    if (Inicio == '<' ) and (Fin == '>'):

                        N_Cade=0
                        C_armar=''

                        QR = x
                        if QR != QR_antes:
                            #print 'OK QR: '+QR
                            #-----------------------------------------
                            Tfin = time.time()
                            Tdiferencia = Tfin - Tinicio

                            if Tdiferencia >= TRepeticion:
                                print 'Procesar:'+QR + ' T_Diferencia:'+ str(Tdiferencia)
                                QR_antes = QR
                                QR = QR.replace ("<","")
                                QR = QR.replace (">","")

                                #Log_QR()

                                Borrar(7)               # Borrar QR
                                Escrivir(QR,7)          # Guardar QR
                                Escrivir_Estados('1',8) # Cambiar estado del QR
                                B_sensor = 2

                            Tinicio = time.time()
                            #-----------------------------------------



                        else:
                            #Log_QR()
                            # si la foma es la del tiiqued proceesar denuevo
                            puntos = QR.count(".")
                            print puntos

                            if puntos == 3:
                                Escrivir_Estados('1',8) # Cambiar estado del QR
                            else:
                                Escrivir_Estados('2',11) # Estado QR repetido
                                print 'QR YA: ' +QR



                    else:
                        C_armar=C_armar + x

                        if (C_armar[0:1] == '<' ) and (C_armar[len (C_armar)-1:len (C_armar)] == '>'):

                            QR = C_armar
                            if QR != QR_antes:
                                #print 'OK QR: '+QR
                                #-----------------------------------------
                                Tfin = time.time()
                                Tdiferencia = Tfin - Tinicio

                                if Tdiferencia >= TRepeticion:
                                    print 'Procesar:'+QR + ' T_Diferencia:'+ str(Tdiferencia)
                                    QR_antes = QR
                                    QR = QR.replace ("<","")
                                    QR = QR.replace (">","")

                                    #Log_QR()

                                    Borrar(7)               # Borrar QR
                                    Escrivir(QR,7)          # Guardar QR
                                    Escrivir_Estados('1',8) # Cambiar estado del QR
                                    B_sensor = 2

                                Tinicio = time.time()
                                #-----------------------------------------

                            else:
                                #Log_QR()
                                puntos = QR.count(".")
                                print puntos
                                if puntos == 3:
                                    Escrivir_Estados('1',8) # Cambiar estado del QR
                                else:
                                    Escrivir_Estados('2',11) # Estado QR repetido
                                    print 'QR YA: ' +QR

                            N_Cade=0
                            C_armar=''
                        else:
                            if len(x) >=2:
                                if (Inicio == '<' ) or (Fin == '>'):
                                    a=0
                                    #print 'pertenese a un qr valido'
                                else:
                                    print 'NO cumple parametros'
                                    print 'X: '+x
                                    QR = x
                                    if QR != QR_antes:
                                        #print 'X QR: '+QR
                                        QR_antes = QR
                                        print 'que pasa'

                                        if QR.find("Igual") != -1:
                                            aqr = Leer_Estado(7) #QR
                                            aqr= aqr.strip()
                                            puntos = aqr.count(".")
                                            print puntos
                                            if puntos == 3:
                                                Escrivir_Estados('1',8) # Cambiar estado del QR
                                            else:
                                                Escrivir_Estados('2',11) # Estado QR repetido
                                                print 'QR YA: ' +QR

                                            #Escrivir_Estados('2',11) # Estado QR repetido
                                            print "Repetido"
                                        else:

                                            #Log_QR()
                                            Borrar(7)               # Borrar QR
                                            Escrivir(QR,7)           # Guardar QR
                                            Escrivir_Estados('1',8) # Cambiar estado del QR
                                            B_sensor = 2
                                    else:

                                        if QR.find("Igual") != -1:
                                            aqr = Leer_Estado(7) #QR
                                            aqr= aqr.strip()
                                            puntos = aqr.count(".")
                                            print puntos
                                            if puntos == 3:
                                                Escrivir_Estados('1',8) # Cambiar estado del QR


                                        print 'mmm'




                #----------------------------------
                #           fin del for
                N_Cade = 0



            else:

                #       Descartar por tiempo espirado
                Eliminar_antes +=1
                if Eliminar_antes >=5:
                    #print 'Borado de cadenas y puesta en zero'
                    Eliminar_antes=0
                    N_Cade=0
                    C_armar=''
                    B_sensor = 0

                #print 'salida del while'
                break
        except SerialException:
            print 'algo paso'
            #port.close()
            while True:

                port = serial.Serial(Puerto_Serial, baudrate=9600, timeout=1)
                break

                """
                res = commands.getoutput('ls /dev/ttyACM*')
                print res#.find("/dev/ttyACM*")

                if res.find("/dev/ttyACM*") == -1:
                    print 'abrir puerto'
                    port.close()
                    port = serial.Serial(res, baudrate=9600, timeout=1)
                    break
                """




            #res=res.replace('"',"")
            #res=res.replace('\n',"")
            #redes =res.split("ESSID:")
    #---------------------------------------
    #       fin de analisis de cadena
    #---------------------------------------


#---------------------
C_Sensor_IR_en_UNO = 0

B_sensor=0

Estado_Antes=0

GPIO.output(CC_Pin, GPIO.LOW)


while 1:

    Leer_datos_SensorQR()
