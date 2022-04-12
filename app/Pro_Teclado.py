#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor: Anderson Amaya Pulido

Libreria personal para procesar un qr.




# ideas a implementar





"""
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
# Librerias creadas para multi procesos o hilos -------------
import datetime
import time
import commands
import sys
import socket
import os


#---------------------------------
#           Librerias personales
#---------------------------------

from lib.Lib_File import *              # importar con los mismos nombres
from lib.Lib_Rout import *              # importar con los mismos nombres
from lib.Lib_Requests_Server import *   #
from lib.Lib_Networks import *          #
from lib.Fun_Dispositivo import *       #
from lib.Fun_Server import *            #
from lib.Fun_Tipo_QR import *           #

#-------------------------------------------------------
# inicio de variable	--------------------------------

PT_Mensajes = 1     # 0: NO print  1: Print

#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------
#                   Deisiones para autorizar por teclado
#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------
#----
#---------------------------------------------------------
def Decision_General():
    global PT_Mensajes


    T_A = str(int(time.time()*1000.0))  # Tiempo()

    if PT_Mensajes:
        print 'Nuevo------------------------------------'
        print 'Tiempo: ', "%s" % T_A

    # Prepararacion de informacion para tratamiento
    Set_File(COM_BUZZER,'1')       #sonido eliminar si no es necesario
    R_Teclas = Get_Teclas()

    if PT_Mensajes:
        print 'Digitado: '+ R_Teclas

    # -----------------------------------------------------------------------------
    # Decision dependiendo del estado del dispositivo y configuracion de prioridades
    # -----------------------------------------------------------------------------

    Prioridad = Get_File(CONF_AUTORIZACION_QR).strip()

    # ------- Prioridades de autorizacion ---------------------
    # 0 :   Servidor      -> Dispositivos -> sin counter    F1_17
    # 1 :   Counter       -> Dispositivos -> sin Servidor   offLine
    # 2 :   Servidor      -> counter      -> Dispositivos   Nuevo
    # 3 :   Counter       -> Servidor     -> Dispositivos   Nuevo
    # ---------------------------------------------------------
    if  Prioridad == '0':
        if PT_Mensajes: print 'Prioridad Serv -> Dispo'
        Status_Peticion_Server = Decision_Server(R_Teclas, T_A)
        if  Status_Peticion_Server == -1:# Error en el  Dispositivo
            Accion_Torniquete ('Error') # Qr no valido

    # ---------------------------------------------------------
    elif  Prioridad == '1':
        if PT_Mensajes: print 'Prioridad Counter -> Dispo'
        Accion_Torniquete ('Error') # no hay prioridad

    # ---------------------------------------------------------
    elif  Prioridad == '2':
        if PT_Mensajes: print 'Prioridad Serv -> counter -> Dispo'
        Accion_Torniquete ('Error') # no hay prioridad

    # ---------------------------------------------------------
    elif  Prioridad == '3':
        if PT_Mensajes: print 'Prioridad counter -> Serv -> Dispo'
        Accion_Torniquete ('Error') # no hay prioridad

    # ---------------------------------------------------------
    else: Accion_Torniquete ('Error') # no hay prioridad


    #print 'Desicion:' + str(Decision_Server(R_Q,T_A))
    #print 'Desicion:' + str(Decision_Dispositivo(R_Q,T_A))
    #print 'Desicion:' + str(Decision_Counter(R_Q,T_A))

#---------------------------------------------------------
#----       Ruta para que autorise el servidor
#---------------------------------------------------------
def Decision_Server(Teclado, Tiempo_Actual):
    global PT_Mensajes

    if PT_Mensajes: print 'Autorisa el servidor'

    Ruta            = Get_Rout_server()
    ID_Dispositivo  = Get_ID_Dispositivo()
    if PT_Mensajes: print 'Ruta:' + str(Ruta.strip()) + ', UUID:' + ID_Dispositivo
    #Enviar_Teclado(IP,T_actual,ID,Rut)
    Respuesta = Enviar_Teclado(Ruta.strip(), Tiempo_Actual, ID_Dispositivo, Teclado)

    if PT_Mensajes: print 'Respuesta: ' + str(Respuesta)

    if Respuesta.find("Error") == -1:                           # Entradas/Salidas Autorizadas
        Accion_Torniquete (Respuesta)
        # verificar si hay registros del usuario
        #Pos_linea = Buscar_Autorizados_ID_Tipo_1(QR)
        #Guardar_Autorizacion_Tipo_1(QR, Tiempo_Actual, Pos_linea, Respuesta, '1') # status internet en 1
        return 1                                                # funcionamiento con normalidad
    elif Respuesta.find("Error :Access denied") != -1:          # Autorizaciones denegadas
        Accion_Torniquete (Respuesta)
        return 1
    else :                                                      # Sin internet Momentanio o fallo del servidor
        if PT_Mensajes: print 'Sin internet o Fallo del servidor'
        return -1



    #NOTAS
    # return -2 #NO tiene tipo de qr valido
    # return -1 #sin internet o fallo del servidor
    # return 1  # respuesta del servidor valida
    return -2




#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------
#               Acciones en el Actuador (torniquete) y visualizadores
#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------
def Accion_Torniquete (Res):
    global PP_Mensajes

    Res=Res.rstrip('\n')            # eliminar caracteres extras
    Res=Res.rstrip('\r')            # eliminar caracteres extras

    if Res == 'Access granted-E':
        #if PP_Mensajes: print "Access granted-E"
        Set_File(COM_LED , 'Access granted-E')
        Set_File(COM_RELE, 'Access granted-E')

    elif Res == 'Access granted-S':
        #if PP_Mensajes: print "Access granted-S"
        Set_File(COM_LED , 'Access granted-S')
        Set_File(COM_RELE, 'Access granted-S')
    else :
        #if PP_Mensajes: print "Denegado"
        Set_File(COM_LED, 'Error')



def Get_Teclas():
    return Get_File(COM_TECLADO)
#---------------------------------------------------------------------------------------
def revicion_Teclado ():
    if Get_File(STATUS_TECLADO) == '1':
        Decision_General()
        Clear_File(STATUS_TECLADO)


#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------
print 'Ciclo principal lectura Teclado'
Set_File(COM_LED, '0')
#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------

while 1:
    #---------------------------------------------------------
    #  Proceso 0: Tiempo de espera para disminuir proceso
    #---------------------------------------------------------
    time.sleep(0.05)
    #---------------------------------------------------------
    # Proceso 4: Procesamiento del QR
    #---------------------------------------------------------
    revicion_Teclado ()
