# -*- coding: utf-8 -*-
# Librerias creadas para multi procesos o hilos -------------

import Control_Archivos
import Seguridad
#import time

from datetime import datetime
from datetime import timedelta

# definiciones para el aplicativo principal -----------------

Leer_Archivo            = Control_Archivos.Leer_Archivo
Borrar                  = Control_Archivos.Borrar_Archivo
Escrivir_Archivo        = Control_Archivos.Escrivir_Archivo
MD5		        = Seguridad.MD5


def Generador_Pines(N_PINES):

    Usuarios = Leer_Archivo(0)
    Key = Leer_Archivo(25)

    now = datetime.now()
    Fecha = now.strftime('%Y%m%d')

    #Fecha ='20200225'
    print(Fecha)

    Borrar(26)
    for linea in Usuarios.split('\n'):
        if len (linea) >5 :
            Lista_Pines =''
            linea = linea.split('.')
            ID= linea[0].rstrip('\r')
            Rut_MD5 = linea[1].rstrip('\r')
            a =''
            for x in  range(N_PINES):

                if x == 0   : Resualtado = MD5(Key + Rut_MD5+ Fecha)
                else        : Resualtado = MD5(Resualtado)
                a += 'MD5         :' + Resualtado+'\n'
                #print 'MD5         :' + Resualtado
                Numeros =''
                contador =0
                for letra in Resualtado:
                    if letra.isalpha() == False:
                        Numeros += letra
                contador =0
                N_Salto =''
                #print 'Numeros     :' + Numeros
                a +=  'Numeros     :' + Numeros+'\n'
                inv_numeros = Numeros[::-1] # invertir lista de nuemros
                #print 'N_Invertidos:' +inv_numeros
                a += 'N_Invertidos:' +inv_numeros+'\n'
                for Numero in inv_numeros:
                    if contador%2 == 0 :
                        N_Salto += Numero
                    contador = contador + 1
                #print 'N_Saltos    :' + N_Salto
                a += 'N_Saltos    :' + N_Salto+'\n'
                Pin_Generado = N_Salto[0:4]
                #print 'Pin_Generado:' + Pin_Generado
                a +=  'Pin_Generado:' + Pin_Generado+'\n'
                Lista_Pines = Lista_Pines + '.'+ Pin_Generado

            cadena = ID + Lista_Pines  # +'\n'
            cadena2 = ID+'\n' + a  # +'\n'
            #print cadena
            Escrivir_Archivo(cadena,26)

    print 'Pines Generados'



#Generador_Pines(4)
