
import commands
import Control_Archivos  as Ca
import Control_Ethernet


import socket
import fcntl
import struct
import time

#----------------------------------------------
#                   definiciones
#----------------------------------------------

Escrivir_Estados        = Ca.Escrivir_Estados
Generar		            = Ca.Generar_ID_Tarjeta
Escrivir_Archivo        = Ca.Escrivir_Archivo
Leer_Archivo            = Ca.Leer_Archivo
Leer_Lineas             = Ca.Leer_Lineas
Borrar                  = Ca.Borrar_Archivo
Link_servidor           = Ca.Mejor_Opcion_link
Escrivir_nuevo          = Ca.Escrivir_nuevo

Dominio_Valido          = Control_Ethernet.Dominio_Valido
Test_IP_Dom             = Control_Ethernet.Test_IP_Dominio

Comando_Antes           = Leer_Archivo(42)

CW_mensajes=0    # 0: NO print  1: Print

def Comando_Procesado(Comando):
    Escrivir_Estados(Comando,42)

def Nueva_wifi(Texto):
    Escrivir_Estados(Texto,43)

def Torniquete(Datos):

    if CW_mensajes:
        print('-----------------------------')
        print('Torniquete')
        print('info, Configurando Torniquete')

    Escrivir_Estados('info, Configurando Torniquete',46)
    Con =len(Datos)
    if Con == 5 :
        if CW_mensajes:
            print "Tiempo: "+Datos[2]+", Direccion: "+Datos[4]
            #print Datos[4][0]
        Escrivir_Estados(str(Datos[4][0]),13)
        Escrivir_Estados(Datos[2],30)
        time.sleep(3)
        if CW_mensajes:
            print('ok, Torniquete configurado')
        Escrivir_Estados('ok, Torniquete configurado',46)
        time.sleep(3)
        Borrar(46)
        return 1

    return 0


def Ip_Estatica(a,we,IP,GD,DNS):

        Borrar_Ip_Estatica(a,we)
        print 'colocando las ip statica'
        if we==0:   Escrivir_Archivo('interface wlan0',44)#f.write('interface wlan0'+'\n')
        else:       Escrivir_Archivo('interface eth0',44)#f.write('interface eth0'+'\n')
        Escrivir_Archivo('static ip_address='+IP,44)#f.write('static ip_address='+IP+'\n')
        Escrivir_Archivo('static routers='+ GD,44)#f.write('static routers='+ GD+'\n')
        Escrivir_Archivo('static domain_name_servers='+ DNS,44)#f.write('static domain_name_servers='+ DNS+'\n')


def Borrar_Ip_Estatica(a,we):

        contador =0
        lineas = Leer_Lineas(44)
        Borrar(44)
        for linea in lineas:
                if (linea[0]!='#') and (len(linea)>=4):
                        if (linea.find('interface')!=-1) or (linea.find('static')!=-1):
                                if (linea.find('option')==-1):
                                        if (linea.find('eth0')!=-1):
                                                contador =0
                                                wec = 1
                                        if (linea.find('wlan0')!=-1):
                                                contador =0
                                                wec = 0
                                        if contador>=0 and contador <=3:
                                                if we == wec:
                                                        print 'Eli: '+str(contador) + linea
                                                else:   Escrivir_Archivo(linea.replace('\n',""),44)
                                        contador =contador + 1
                                else:   Escrivir_Archivo(linea.replace('\n',""),44)
                        else:   Escrivir_Archivo(linea.replace('\n',""),44)
                else:   Escrivir_Archivo(linea.replace('\n',""),44)



def Comunicaciones(Datos):
    if CW_mensajes:
        print('-----------------------------')
        print('Comunicaciones')

    Con =len(Datos)
    if Con == 19 :
        if Datos[2].find("Ethernet") != -1  :
            if CW_mensajes:
                print "IP: "+Datos[4]+Datos[5]+Datos[6]+Datos[7] + "G: "+Datos[9]+Datos[10]+Datos[11]+Datos[12] + "DN: "+Datos[14]+Datos[15]+Datos[16]+Datos[17] +" Configura Ethernet"
            Ip_Estatica(1, 1, Datos[4]+'.'+Datos[5]+'.'+Datos[6]+'.'+Datos[7], Datos[9]+'.'+Datos[10]+'.'+Datos[11]+'.'+Datos[12], Datos[14]+'.'+Datos[15]+'.'+Datos[16]+'.'+Datos[17])
            return 1
        else                                :
            if CW_mensajes:
                print "IP: "+Datos[4]+Datos[5]+Datos[6]+Datos[7] + "G: "+Datos[9]+Datos[10]+Datos[11]+Datos[12] + "DN: "+Datos[14]+Datos[15]+Datos[16]+Datos[17] +"Configura wifi"
            Ip_Estatica(1, 0, Datos[4]+'.'+Datos[5]+'.'+Datos[6]+'.'+Datos[7], Datos[9]+'.'+Datos[10]+'.'+Datos[11]+'.'+Datos[12], Datos[14]+'.'+Datos[15]+'.'+Datos[16]+'.'+Datos[17])
            return 1
    if Con == 4 :
        if Datos[2].find("Ethernet") != -1  :
            if CW_mensajes:
                print Datos[2]+Datos[3]+"Ethernet Dinamico"
            Borrar_Ip_Estatica(1,1)
            return 1
        else                                :
            if CW_mensajes:
                print Datos[2]+Datos[3]+"Wifi Dinamico"
            Borrar_Ip_Estatica(1,0)
            return 1
    if Con == 5 :
        if CW_mensajes:
            print Datos[2]+Datos[4]+"Nueva wifi"
        red = Datos[2]
        clave = Datos[4]
        commands.getoutput('sudo chmod -R 777 /etc/wpa_supplicant/wpa_supplicant.conf')
        N_wifi='\nnetwork={\n\tssid="'+red+'"\n\tpsk="'+clave+'"\n\tkey_mgmt=WPA-PSK\n\n}'
        if CW_mensajes:
            print (N_wifi)
        Nueva_wifi(N_wifi)
        return 1
    if Con == 7 :
        if CW_mensajes:
            print "IP_counter: "+Datos[3]+'.'+Datos[4]+'.'+Datos[5]+'.'+Datos[6]

        Borrar(49)
        Escrivir_Archivo(Datos[3]+'.'+Datos[4]+'.'+Datos[5]+'.'+Datos[6],49)
        return 1





    return 0

def Restablecer(Datos, Comando):

    if CW_mensajes:
        print('-----------------------------')
        print('Restablecer')

    Con =len(Datos)

    if Datos[1].find("Borrar_Historial") != -1  :
        if CW_mensajes:
            print('info, Borrando el Historial')
        Escrivir_Estados('info, Borrando el Historial',46)
        #print "Borrardo his"
        Borrar(12)       #Borrar Numero de lecturas
        Escrivir_Estados('0',12) #dejar en 0 las lecturas

        Borrar(14)       #Borrar Numero de Reinicios
        Escrivir_Estados('0',14) #dejar en 0 los reinicios
        time.sleep(3)
        if CW_mensajes:
            print('ok,Borrado el Historial')
        Escrivir_Estados('ok,Borrado el Historial',46)
        time.sleep(3)
        Borrar(46)

        return 1

    if Datos[1].find("Borrar_Base_de_datos") != -1  :
        if CW_mensajes:
            print('info, Borrando Base de datos')
        #print "Borrardo bd"
        Escrivir_Estados('info, Borrando Base de datos',46)
        Borrar(0)       #borrar tabla servidor
        Borrar(1)       #borrar tabla lector
        Borrar(2)       #borrar tabla Enviar
        time.sleep(3)
        if CW_mensajes:
            print('ok,Borrada la Base de datos')
        Escrivir_Estados('ok,Borrada la Base de datos',46)
        time.sleep(3)
        Borrar(46)

        return 1

    if Datos[1].find("Valores_de_fabrica") != -1  :
        if CW_mensajes:
            print('info, Configuranco Valores fabrica')

        Escrivir_Estados('info, Configuranco Valores fabrica',46)

        #Base_Datos_Local()
        Borrar(0)       #borrar tabla servidor
        Borrar(1)       #borrar tabla lector
        Borrar(2)       #borrar tabla Enviar
        #Borrar_Historial ()
        Borrar(12)       #Borrar Numero de lecturas
        Escrivir_Estados('0',12) #dejar en 0 las lecturas

        Borrar(14)       #Borrar Numero de Reinicios
        Escrivir_Estados('0',14) #dejar en 0 los reinicios

        #estados de sensores y lecturas
        #led
        Borrar(10)      #led
        Escrivir_Estados('0',10)
        Borrar(3)      #Estado led
        Escrivir_Estados('0',3)
        #tecla
        Borrar(4)      #Esatado teclado
        Borrar(5)      #Teclas
        #chicharra
        Borrar(6)      #Esatado chicharra
        Escrivir_Estados('1',6)
        #Qr
        Borrar(7)      #QR
        Borrar(8)      #Estado QR
        Borrar(9)      #Estado sensor
        Escrivir_Estados('0',9)
        Borrar(11)      #Estado QR repetido
        #Torniquete
        Borrar(13)      #Direcion Torniquete
        Escrivir_Estados('D',13)
        #Tiempo Torniquete
        Borrar(30)      #Esatado chicharra
        Escrivir_Estados('1',30)

        #Escrivir_Estados(Estados,3)
        time.sleep(3)
        if CW_mensajes:
            print('ok, Valores fabrica')
        Escrivir_Estados('ok, Valores fabrica',46)
        time.sleep(3)
        Borrar(46)
        return 1

    if Datos[1].find("TS") != -1  :
        if CW_mensajes:
            print('info, Comenzando Test')

        Escrivir_Estados('info, Comenzando Test',46)
        Test_Nuevo_Servidor(Comando,"Test")
        return 1

    if Datos[1].find("CS") != -1  :
        if CW_mensajes:
            print('info, Comenzando Conexion')

        Escrivir_Estados('info, Comenzando Conexion',46)
        Test_Nuevo_Servidor(Comando,"Conectando")
        return 1

    return 0

def Resolver_Comando_Web():

    global Comando_Antes

    Comando = Leer_Archivo(45)
    #print Comando

    if Comando_Antes != Comando :
        #print Comando
        Datos = Comando.replace(':','.')
        if CW_mensajes:
            print Datos
        Datos = Datos.split('.')
        #print len(Datos)

        if Datos[0] == 'F':
            if Firmware(Datos, Comando) == 1:    # print('Restablecer')
                Comando_Procesado(Comando)
                Comando_Antes = Comando
        if Datos[0] == 'R':
            if Restablecer(Datos, Comando) == 1:    # print('Restablecer')
                Comando_Procesado(Comando)
                Comando_Antes = Comando
        if Datos[0] == 'T':
            if Torniquete(Datos) == 1:    # print('Comunicaciones')#
                Comando_Procesado(Comando)
                Comando_Antes = Comando
        if Datos[0] == 'C':
            if Comunicaciones(Datos) == 1:    # print('Comunicaciones')#
                Comando_Procesado(Comando)
                Comando_Antes = Comando
                #commands.getoutput('sudo reboot')

def Firmware(Datos, Comando):
    if CW_mensajes:
        print('-----------------------------')
        print('firmware')

    Escrivir_Estados('1',40)

    Escrivir_Estados('info, Forzando Actualizacion',46)
    time.sleep(3)
    if CW_mensajes:
        print('info, ejecutando  Actualizacion')
    Escrivir_Estados('info, ejecutando  Actualizacion',46)
    time.sleep(3)
    Borrar(46)
    return 1

    return 0

def Check_Respuestas(Respuesta):
    #print Respuesta
    #print Respuesta.status_code
    if Respuesta == 'OK':
        #print 'Respuesta correcta'
        return True
    else:
        #print 'Respuesta incorrecta'
        #print Respuesta.text
        return False


def Test_Nuevo_Servidor(Comando,tipo):
            N_Servidor1 = Comando.split(':')
            N_Servidor = N_Servidor1[1].strip()
            if CW_mensajes:
                print '-----------------------------'
                print N_Servidor
                print '-----------------------------'
            Variable_Dominio=''
            Variable_IP=''
            #print 'hola'

            try:
                    socket.inet_aton(N_Servidor)
                    if N_Servidor.count('.') == 3:
                        if CW_mensajes:
                            print '---------------------------------'
                            print '1. revicion de conexion por IP'
                            print '---------------------------------'
                        Escrivir_Estados('info, 1. revicion de conexion por IP',46)
                        if CW_mensajes:
                            print 'IP :' +str(N_Servidor)
                        Respuesta = Test_IP_Dom(N_Servidor, 'http')
                        #print Respuesta
                        #if Respuesta !='NO':
                        if Respuesta.find("Error") == -1:
                            Check_Res= Check_Respuestas(Respuesta)
                            if Check_Res == True:
                                if CW_mensajes:
                                    print 'Esta IP es valida'

                                #Mensajes('Test OK,Esta IP es valida se cambiara, pero el dominio sera el mismo.','OK')
                            else:
                                if CW_mensajes:
                                    print 'Test Error,La IP no Funciona'
                                #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                        else:
                            if CW_mensajes:
                                print 'Test Error,La IP no contesto'
                            #Mensajes('Test Error,La IP no contesto.','Error')



            except socket.error:
                    if CW_mensajes:
                        print '---------------------------------'
                        print 'NO es una IP revision por Dominio'
                        print '---------------------------------'
                    Escrivir_Estados('info, Revision por Dominio',46)
                    IP = Dominio_Valido(N_Servidor)
                    Variable_Dominio = N_Servidor
                    Variable_IP = str(IP)
                    #print IP
                    if IP != False:
                            Test_IP_Dominio=0
                            if CW_mensajes:
                                print '---------------------------------'
                                print 'Prueba de coneccion por IP'
                                print '---------------------------------'
                                print 'IP :' +str(IP)
                                print 'Con http'

                            Escrivir_Estados('info, Revision por Ip con http',46)

                            Respuesta= Test_IP_Dom(IP, 'http')
                            #print Respuesta
                            #if Respuesta !='NO':
                            if Respuesta.find("Error") == -1:
                                Check_Res= Check_Respuestas(Respuesta)

                                if Check_Res == True:
                                    if CW_mensajes:
                                        print 'Esta IP es valida'
                                    Test_IP_Dominio=10
                                    #Mensajes('Test OK,Esta IP es valida se cambiara, pero el dominio sera el mismo.','OK')
                                else:
                                    if CW_mensajes:
                                        print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                    #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                            else:
                                if CW_mensajes:
                                    print 'Test Error,La IP no contesto'

                            if CW_mensajes:
                                print 'Con https'
                            Escrivir_Estados('info, Revision por IP con https',46)

                            Respuesta= Test_IP_Dom(IP, 'https')
                            #print Respuesta
                            #if Respuesta !='NO':
                            if Respuesta.find("Error") == -1:
                                Check_Res= Check_Respuestas(Respuesta)

                                if Check_Res == True:
                                    if CW_mensajes:
                                        print 'Esta IP es valida'
                                    Test_IP_Dominio=Test_IP_Dominio+100
                                    #Mensajes('Test OK,Esta IP es valida se cambiara, pero el dominio sera el mismo.','OK')
                                else:
                                    if CW_mensajes:
                                        print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                    #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                            else:
                                if CW_mensajes:
                                    print 'Test Error,La IP no contesto'

                            if CW_mensajes:
                                print '---------------------------------'
                                print 'Prueba de coneccion por Dominio'
                                print '---------------------------------'
                            Escrivir_Estados('info, Revision por Dominio',46)
                            if CW_mensajes:
                                print 'Dominio :' +N_Servidor
                                print 'Con http'
                            Escrivir_Estados('info, Revision por Dominio con http',46)

                            Respuesta= Test_IP_Dom(N_Servidor, 'http')
                            #print Respuesta
                            if Respuesta !='NO':
                                Check_Res= Check_Respuestas(Respuesta)
                                if Check_Res == True:
                                    if CW_mensajes:
                                        print 'Esta Dominio es valida'
                                    Test_IP_Dominio=Test_IP_Dominio+1
                                else:
                                    if CW_mensajes:
                                        print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                    #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                            else:
                                if CW_mensajes:
                                    print 'Test Error,El dominio no contesto'
                            if CW_mensajes:
                                print 'Con https'
                            Escrivir_Estados('info, Revision por Dominio con https',46)

                            Respuesta= Test_IP_Dom(N_Servidor, 'https')
                            #print Respuesta
                            #if Respuesta !='NO':
                            if Respuesta.find("Error") == -1:
                                Check_Res= Check_Respuestas(Respuesta)
                                if Check_Res == True:
                                    if CW_mensajes:
                                        print 'Esta Dominio es valida'
                                    Test_IP_Dominio=Test_IP_Dominio+1000
                                else:
                                    if CW_mensajes:
                                        print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                    #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                            else:
                                if CW_mensajes:
                                    print 'Test Error,El dominio no contesto'

                            if CW_mensajes:
                                print '--------------fin -------------'
                            print Test_IP_Dominio


                            if Test_IP_Dominio == 0:    Escrivir_Estados('error,'+tipo+' 0 Error, http Dominio NO. IP NO; https Dominio NO. IP NO.',46)
                            if Test_IP_Dominio == 1:    Escrivir_Estados('ok,'+tipo+' 25%  OK. http Dominio OK. IP NO; https Dominio NO. IP NO.',46)
                            if Test_IP_Dominio == 10:   Escrivir_Estados('ok,'+tipo+' 25%  OK. http Dominio NO. IP OK; https Dominio NO. IP NO.',46)
                            if Test_IP_Dominio == 11:   Escrivir_Estados('ok,'+tipo+' 50%  OK. http Dominio OK. IP OK; https Dominio NO. IP NO.',46)

                            if Test_IP_Dominio == 100:  Escrivir_Estados('ok,'+tipo+' 25%  OK. http Dominio NO. IP NO; https Dominio NO. IP OK.',46)
                            if Test_IP_Dominio == 101:  Escrivir_Estados('ok,'+tipo+' 50%  OK. http Dominio OK. IP NO; https Dominio NO. IP OK.',46)
                            if Test_IP_Dominio == 110:  Escrivir_Estados('ok,'+tipo+' 50%  OK. http Dominio NO. IP OK; https Dominio NO. IP OK.',46)
                            if Test_IP_Dominio == 111:  Escrivir_Estados('ok,'+tipo+' 75%  OK. http Dominio OK. IP OK; https Dominio NO. IP OK.',46)

                            if Test_IP_Dominio == 1000: Escrivir_Estados('ok,'+tipo+' 25%  OK. http Dominio NO. IP NO; https Dominio OK. IP NO.',46)
                            if Test_IP_Dominio == 1001: Escrivir_Estados('ok,'+tipo+' 50%  OK. http Dominio OK. IP NO; https Dominio OK. IP NO.',46)
                            if Test_IP_Dominio == 1010: Escrivir_Estados('ok,'+tipo+' 50%  OK. http Dominio NO. IP OK; https Dominio OK. IP NO.',46)
                            if Test_IP_Dominio == 1011: Escrivir_Estados('ok,'+tipo+' 75%  OK. http Dominio OK. IP OK; https Dominio OK. IP NO.',46)

                            if Test_IP_Dominio == 1100: Escrivir_Estados('ok,'+tipo+' 50%  OK. http Dominio NO. IP NO; https Dominio OK. IP OK.',46)
                            if Test_IP_Dominio == 1101: Escrivir_Estados('ok,'+tipo+' 75%  OK. http Dominio OK. IP NO; https Dominio OK. IP OK.',46)
                            if Test_IP_Dominio == 1110: Escrivir_Estados('ok,'+tipo+' 75%  OK. http Dominio NO. IP OK; https Dominio OK. IP OK.',46)
                            if Test_IP_Dominio == 1111: Escrivir_Estados('ok,'+tipo+' 100% OK. http Dominio OK. IP OK; https Dominio OK. IP OK.',46)

                            if tipo == 'Conectando':
                                if Test_IP_Dominio !=0:
                                    if CW_mensajes:
                                        print 'guardando y reiniciando'
                                    print Test_IP_Dominio
                                    print Variable_IP
                                    print Variable_Dominio


                                    #print Variable_IP
                                    Borrar(32)
                                    Escrivir_Archivo(Variable_IP,32)#N_A_IP_Servidor
                                    Borrar(31)
                                    Escrivir_Archivo(Variable_Dominio,31)#N_A_Dominio_Servidor
                                    Borrar(36)
                                    Escrivir_Archivo(str(Test_IP_Dominio),36)#N_A_Dominio_Servidor
                                    #time.sleep(3)
                                    #Borrar(46)

                                    #commands.getoutput('sudo reboot')


                    else:
                            if CW_mensajes:
                                print 'Dominio NO Valido, no hay IP asociada'
                            Escrivir_Estados('error, Dominio NO Valido, no hay IP asociada',46)
                            #Mensajes('Dominio NO Valido, no hay IP asociada.','Error'

                    time.sleep(3)
                    Borrar(46)

"""
print 'listo'
while 1:
    time.sleep(0.05)
    Resolver_Comando_Web()
"""
"""

R.Borrar_Historial
R.Borrar_Base_de_datos
R.Valores_de_fabrica
R.Nuevo_servidor
T.T:6.D:Izquierda
T.T:9.D:Derecha
C.W:NEWNET2020.P:567uytyu
C.R:WIFI.D
C.W:ACAMRO.P:12312
C.R:Ethernet.I:5464.G:456.D:54646.E

"""
