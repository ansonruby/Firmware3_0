#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor: Anderson Amaya Pulido

Proceso para la actualizacion del Firmware.




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

PF_Mensajes = 1     # 0: NO print  1: Print

#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------
#                   funciones para el actualizador de firmware
#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------

def Hora_Actual():
	tiempo_segundos = time.time()
	#print(tiempo_segundos)
	#tiempo_cadena = time.ctime(tiempo_segundos) # 1488651001.7188754 seg
	tiempo_cadena = time.strftime("%I:%M %p")
	#print(tiempo_cadena)
	return tiempo_cadena
#---------------------------------------------------------
def Filtro_Caracteres(s): # eliminar los caracteres y estructura Jason
    s = s.replace('"',"")
    s = s.replace('[',"")
    s = s.replace('{',"")
    s = s.replace(']',"")
    s = s.replace('}',"")
    s = s.replace('data:',"")
    s = s.replace(',',"\r\n")
    return s
#---------------------------------------------------------
def Hora_Actualizacion_Firmware(Hora_Actualizacion):

	if Hora_Actualizacion == Hora_Actual():
		while 1:
		    time.sleep(1)
		    if Hora_Actual() != Hora_Actualizacion : break
		if PF_Mensajes:    print 'Actualizando el Firmware'
		Set_File(COM_ACTUALIZADOR, '1')   # Estado inicial del actualizador
#--------------------------------------------------------
def  Procedimiento_Actualizar_Firmware():
	if Get_File(COM_ACTUALIZADOR) == '1':
		Clear_File(COM_ACTUALIZADOR)
		if PF_Mensajes:
			print 'Proceso de revision del firmware'

		Vercion = Get_File(INF_VERCION)
		Vercion = Vercion.replace('\n','')
		Vercion = Vercion.strip()
		Vercion = "2022.03.11.0"  #----- comentariar    por que esta quemado

		T_A = str(int(time.time()*1000.0))

		Ruta            = Get_Rout_server()
		ID_Dispositivo  = Get_ID_Dispositivo()
		if PF_Mensajes:
			print 'Ruta:' + str(Ruta.strip()) + ', UUID:' + ID_Dispositivo

		Respuesta = Veri_Firmware(Ruta.strip(), T_A, ID_Dispositivo, Vercion)       #enviar peticion a servidor

		if Respuesta.find("Error") == -1:
			s = Filtro_Caracteres(Respuesta)
			s=s.partition('\n')
			s1 = s[0].replace('id:','')
			ID_F = s1.replace('\r','')
			s2 = s[2].partition('\r')
			s3 = s2[0].replace('version:','')
			Vercion_F =s3.replace('\r','')
			Git_F = s2[2].replace('\r','')
			Git_F = Git_F.replace('\n','')
			Git_F = Git_F.replace('github:','')
			#--------------------------------
			if PF_Mensajes:
				print 'ID: '+ ID_F + ' vercion: '+Vercion_F + ' git: '+Git_F


			if ID_F=='OK':
				if PF_Mensajes:
					print 'Estoy actualizado'
			else:
				if ID_F !=  ID_Dispositivo :
					if PF_Mensajes:
						print 'NO es para mi'
				else:
					if Vercion.find(Vercion_F) != -1 :
						if PF_Mensajes:
							print 'ya esta actualizado'
					else:
						if PF_Mensajes:
							print 'Devo actualizar la peticon es valida'#guarar la peticion
							Clear_File(RESP_PET_FIRMWARE)
							Add_File(RESP_PET_FIRMWARE,ID_F+'\n')
							Add_File(RESP_PET_FIRMWARE,Vercion_F+'\n')
							Add_File(RESP_PET_FIRMWARE,Git_F+'\n')
							Set_File(STATUS_ACTUALIZADOR, '1') # Estado en 1 para el comiendso del Actualizador

		else:
			if PF_Mensajes:
				print 'No contesto el Servidor'






#---------------------------------------------------------
while 1:
	#---------------------------------------------------------
	#  Proceso 0: Tiempo de espera para disminuir proceso
	#---------------------------------------------------------
	time.sleep(0.05)
	#---------------------------------------------------------
	#  Proceso 1: Actualizar en una hora determinada
	#---------------------------------------------------------
	Hora_Actualizacion_Firmware("12:34 PM") # 12:00 AM     03:59 PM # hora chile  10:00 PM 12:10 AM
	#---------------------------------------------------------
	#  Proceso 2: procedimiento inicial de Actualizacion
	#---------------------------------------------------------
	Procedimiento_Actualizar_Firmware()
