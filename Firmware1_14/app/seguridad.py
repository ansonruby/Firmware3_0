
import commands
import sys
import time
import RPi.GPIO as GPIO #Libreria Python GPIO


GPIO.setmode (GPIO.BOARD)
# configuracion de pines
        #chicharra
CC_Pin_UPS =  8 #8sin fuentee #3 para la sinta de seguridad 
GPIO.setup(CC_Pin_UPS, GPIO.IN)
CC_Pin_Seguridad =  3 #8sin fuentee #3 para la sinta de seguridad 
GPIO.setup(CC_Pin_Seguridad, GPIO.IN)
a = '0'
b = '0'



#------		Directorio
SE_Carpeta = "/home/pi/FirmwareBK2/"

SE_Directorio =[
        
        #-------        Data     ----------
        'db/Data/Tabla_Servidor.txt',
        'db/Data/Tabla_Pines.txt',
        'db/Data/Tabla_Lector.txt',
        'db/Data/Tabla_Enviar.txt',
        'db/Data/Tabla_Pines_Usados.txt',
        #-------        Status     ----------
        'db/Status/Estado_Led.txt',
        'db/Status/Led.txt',
        'db/Status/Estado_Teclado.txt',
        'db/Status/Teclas.txt',
        'db/Status/Estado_Chicharra.txt',
        'db/Status/QR.txt',
        'db/Status/Estado_QR.txt',
        'db/Status/Estado_Sensor.txt'
        'db/Status/Estado_QR_Repetido.txt',
        #-------        Log     ----------
        'db/Log/Numero_Lecturas_QR.txt',
        'db/Log/Numero_Reinicios.txt',
        #-------        Config     ----------
        'db/Config/Direccion_Torniquete.txt',
        #-------        Comunicacion Dispostivos     ----------
        'db/Dispositivos/IP.txt',
        'db/Dispositivos/Para_Dispostivos.txt',
        'db/Dispositivos/Tx_Dispo.txt',
        'db/Dispositivos/Rx_Dispo.txt',
        #-------        Actualizador     ----------
        'auto/Procesos.txt',
        'db/Config/Vercion_Firmware.txt',
        'auto/ProcesosBK.txt', # cambiar a la ruta del proceso de BK
        
        '/home/pi/Actualizador/db/Respuesta_Peticion_Firmware.txt',
        '/home/pi/Actualizador/db/Memoria_Actualizador.txt',
        '/home/pi/Actualizador/db/Estado_Actualizador.txt',
        '/home/pi/.ID/Datos_Creacion.txt',
        #-------        Control de pines     ----------
        '/home/pi/.ID/Key.txt'
        ]
tiempo_Alimatacion =0
tiempo_segundos =0
#se deve utilizar uuna memoria permanente
while (True):
        
        time.sleep(1.05)
        a= GPIO.input(CC_Pin_UPS)
        #print 'UPS:'+str(a)

        if a== 1:
                print 'Funcionando con Alimantacion'
                tiempo_Alimatacion = time.time()
                print tiempo_Alimatacion
                
        else:
                print 'Funcionando con Bateria'
                if tiempo_Alimatacion == 0:
                        tiempo_Alimatacion = time.time()
                        print tiempo_Alimatacion
                        
                tiempo_segundos = time.time()
                Tiempo_Sin_Fuente =int(tiempo_segundos - tiempo_Alimatacion)/60
                print Tiempo_Sin_Fuente

                if Tiempo_Sin_Fuente >= 1:#4
                        print 'Borrar Data base'
                if Tiempo_Sin_Fuente >= 15:
                        print 'Borrar Data del programa'
                        



        
        b= GPIO.input(CC_Pin_Seguridad)
        print 'Cinta:'+str(b)
        
        if b== 1:
                #find /home/pi/FirmwareBK2 -type f -exec shred -n 3 -zu {} \;
                for i in range(0, 5):
                    print SE_Carpeta + SE_Directorio[i]
                    #res = commands.getoutput('shred -n 10 -uvz '+SE_Carpeta + SE_Directorio[i])
                    #print 'Respuesta:'+ res
                    
                #res = commands.getoutput('shred -n 10 -uvz /home/pi/FirmwareBK2/README.md')
                #res = commands.getoutput('chmod -R 755 /home/pi/Actualizador/sh/app_Actualizando.sh')
                #res = 'que paso'
                #print 'Respuesta:'+ res
    
