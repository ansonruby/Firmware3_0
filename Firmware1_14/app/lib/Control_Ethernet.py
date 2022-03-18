import socket
import urllib2
import os
import requests
import commands
import Control_Archivos  as Ca
import Control_Fecha

#----------------------------------------------
#                   definiciones
#----------------------------------------------

Generar		            = Ca.Generar_ID_Tarjeta
Escrivir_Archivo        = Ca.Escrivir_Archivo
Leer_Archivo            = Ca.Leer_Archivo
Borrar                  = Ca.Borrar_Archivo
Link_servidor           = Ca.Mejor_Opcion_link
Escrivir_nuevo          = Ca.Escrivir_nuevo

Tiempo                  = Control_Fecha.T_Actual

#-----------------------------------------------
#               constantes del aplicativo
#-----------------------------------------------
CE_V=1          # 0: servidor de prueba 1: las direciones del aplicativo
P_Mensajes=0    # 0: NO print  1: Print

CE_url = "http:"

MAC_DIRC        = 'cat /sys/class/net/wlan0/address'
MAC             = commands.getoutput(MAC_DIRC)
MAC             = MAC.replace(":","")
ID_Tarjeta      = Generar(MAC)
IP_servidor     = Link_servidor()

#------		Directorio

CE_rl =[        "/api/access/keyboard_access",      # Enviar Teclado
                "/api/access/grant",                # Enviar QR
                "/api/access/get_granted_users_pi", # Resivir usuarios
                "/api/access/set_in_out_activity",  # Enviar E/S sin Internet
                "/api/access/verify_conection",     # Verificar conexion
                "/api/firmware/review_update",      # Peticion Actualizacion
                "/api/firmware/confirm_update"      # Confirmacion Actualizacion
        ]

"""
CE_rl =[        "/api/access/keyboard_access/index.php",      # Enviar Teclado
                "/api/access/grant/index.php",                # Enviar QR
                "/api/access/get_granted_users_pi/index.php", # Resivir usuarios
                "/api/access/set_in_out_activity/index.php",  # Enviar E/S sin Internet
                "/api/access/verify_conection/index.php",     # Verificar conexion
                "/api/firmware/review_update/index.php",      # Peticion Actualizacion
                "/api/firmware/confirm_update/index.php"      # Confirmacion Actualizacion
        ]
"""
#-----------------------------------------------
#               ID_Tarjeta y IP_servidor Pruebas
#-----------------------------------------------
#ID_Tarjeta         = 'AAAA01092019b827eb371aaf000001' # dispositivo QR
#ID_Tarjeta         = 'ABDB23102020b827eb3a24df000002' # dispositivo SL_CHI_41
#ID_Tarjeta         = 'ABDB01062020b827ebaa4c01000004' # dispositivo SL_CHI_36
#ID_Tarjeta         = 'ABDB12022020b827eb5dce1e000014' # dispositivo SL_CHI_12
#ID_Tarjeta          = 'ABDB01062020b827eb929bfb000002' # dispositivo SL_CHI_34
#ID_Tarjeta         = 'ABDB12022020b827eb36f4c1000023' # dispositivo SL_CHI_3
#ID_Tarjeta         = 'CCCB23102020b827ebc30bd7000001' # dispositivo IF_CHI_01
#Dominio_Servidor   = 'sportlife.fuseaccess.com'         # Servidor
#IP_servidor        = 'http://192.168.1.109'            #servidor de pruebas local
#IP_servidor         = 'http://192.168.1.113'         # PC
#IP_servidor        = 'http://sportlife.fuseaccess.com'
#IP_servidor        = 'https://sportlife.fuseaccess.com'
#IP_servidor        = 'http://18.237.109.221'
#IP_servidor        = 'https://18.237.109.221'
#IP_servidor        = 'http://34.213.55.39'
#IP_servidor        = 'http://ec2-34-221-92-179.us-west-2.compute.amazonaws.com'
#IP_servidor        = 'http://34.213.55.39'
#IP_servidor        = 'http://34.221.92.179'

#-----------------------------------------------
#               Funciones
#-----------------------------------------------

# Print_ID_Tarjeta()           # No veo la necesidad
# Cambio_ID_Tarjeta(ID)        # No veo la necesidad
# Get_Post_try_catch(CE_url, CE_datos, CE_cabeceras, tout)    # Nuevo : filtro 1
# Confirmacion_Firmware(T_actual, vercion_Actual_Firmware,LOG)
# Verificar_Firmware(T_actual, vercion_Actual_Firmware)
# ping ()
# envio(dat,T_actual,QR_Te)
# Usuarios_Activos(T_actual)

def Ver_Link():
    global IP_servidor
    print 'Link :' + str(IP_servidor)

def Get_Post_try_catch(peticion, CE_url, CE_datos, CE_cabeceras, tout):
    try:
        if peticion == 'GET' : CE_peticion = requests.get(CE_url, data=CE_datos, headers=CE_cabeceras, timeout=tout)
        if peticion == 'POST': CE_peticion = requests.post(CE_url, data=CE_datos, headers=CE_cabeceras, timeout=tout)
        if peticion == 'GET_SIN_PARAMETROS': CE_peticion = requests.get(CE_url, timeout=tout)
        if peticion == 'GET_SOLO_CABECERA': CE_peticion = requests.get(CE_url, headers=CE_cabeceras, timeout=2)
        #print CE_peticion
        if CE_peticion.status_code == 200:
            Texto = CE_peticion.text
            if Texto.find("Access denied") == -1:
                if P_Mensajes:
                    print '200 :'+ CE_peticion.text
                return CE_peticion.text
            else:
                if P_Mensajes:
                    print 'Error :Access denied'
                return 'Error :Access denied'

        else :
            if P_Mensajes:
                print 'Error :'+str(CE_peticion.status_code)
                print CE_peticion.text
            return 'Error :'+str(CE_peticion.status_code)

    #except requests.ConnectionError, e:
    except :
        #print e
        if P_Mensajes:
            print  'Error :Conection'
        return 'Error :Conection'


def Confimacion_Firmware(T_actual, vercion_Actual_Firmware,LOG):
    global CE_url
    global CE_url_Teclado
    global CE_rl
    global CE_rlP
    global ID_Tarjeta
    global CE_V

    CE_peticion='NO'
    CE_cabeceras = {
        "Content-Type" : "application/json",
        "Fuseaccess-Id" : ID_Tarjeta,
        "Time-Scan" : T_actual
    }

    #CE_url = "http://35.161.178.60/api/firmware/confirm_update"
    if CE_V != 0	: CE_url = IP_servidor+CE_rl[6]         #CE_rl[4]
    else		: CE_url = IP_servidorP+CE_rl[6]        #CE_rlP[4]

    if P_Mensajes:
        print '-------------------------------------'
        print 'Confimacion_Firmware'
        print '-------------------------------------'
        print 'URL :'+ CE_url

    if len(LOG)>=2:
        CE_datos ='{"version":"'+vercion_Actual_Firmware+'","updated":"0","log":"'+LOG+'"}'
    else :
        CE_datos ='{"version":"'+vercion_Actual_Firmware+'","updated":"1"}'
    print CE_datos
    #CE_datos ='{"version":"2019.12.3.0","update":"1"}'#Formato actualisacion correcta
    #CE_datos ='{"version":"2019.12.3.0","update":"0","log":"2.3 herror ...."}' #Formato herror
    return Get_Post_try_catch('POST', CE_url, CE_datos, CE_cabeceras, 2)


def Veri_Firmware(T_actual, vercion_Actual_Firmware):
    global CE_url
    global CE_url_Teclado
    global CE_rl
    global CE_rlP
    global ID_Tarjeta
    global CE_V

    CE_peticion='NO'
    CE_cabeceras = {
        "Content-Type" : "application/json",
        "Fuseaccess-Id" : ID_Tarjeta,
        "Time-Scan" : T_actual
    }

    #CE_url = "http://35.161.178.60/api/firmware/review_update"
    if CE_V != 0    : CE_url = IP_servidor+CE_rl[5]
    else            : CE_url = IP_servidorP+CE_rl[5]
    if P_Mensajes:
        print '-------------------------------------'
        print 'Veri_Firmware'
        print '-------------------------------------'
        print 'URL :'+ CE_url

    CE_datos ='{"data":"'+vercion_Actual_Firmware+'"}'#ya con la vercion del dispsotivo
    #CE_datos ='{"data":"2019.12.3.0"}' #firmware actual
    if P_Mensajes:
        print 'Datos :'+ CE_datos

    return Get_Post_try_catch('GET', CE_url, CE_datos, CE_cabeceras, 2)


def ping ():

        global CE_url
        global IP_servidorP
        global IP_servidor
        global CE_V

        CE_peticion='NO'

        if CE_V != 0	: CE_url = IP_servidor+CE_rl[4]         #CE_rl[4]
        else		: CE_url = IP_servidorP+CE_rl[4]        #CE_rlP[4]

        if P_Mensajes:
            print '-------------------------------------'
            print 'ping'
            print '-------------------------------------'
            print 'URL :'+ CE_url

        return Get_Post_try_catch('GET_SIN_PARAMETROS', CE_url, '', '', 1)


def envio(dat,T_actual,QR_Te):

        global CE_url
        global CE_url_Teclado
        global CE_rl
        global CE_rlP
        global ID_Tarjeta
        global CE_V

        CE_peticion='NO'
        CE_cabeceras = {
        "Content-Type" : "application/json",
        "Fuseaccess-Id" : ID_Tarjeta,
        "Time-Scan" : T_actual
        }

        QR_ruta = QR_Te

        if QR_Te == 0:  QR_ruta = 0 # para rut
        if QR_Te == 1:  QR_ruta = 1 # para qr
        if QR_Te == 2:  QR_ruta = 0 # para pin

        if CE_V != 0 : CE_url = IP_servidor+CE_rl[QR_ruta]
        else		 : CE_url = IP_servidorP+CE_rl[QR_ruta]

        if QR_Te == 0: CE_datos ='{"rut":"'+dat+'"}'    #'{"rut":"99158441"}'
        if QR_Te == 1: CE_datos ='{"data":"'+dat+'"}'	#'{"data":"991584411234"}'
        if QR_Te == 2: CE_datos ='{"rut":"'+dat+'"}'	#'{"pin":"'+dat+'"}'	#'{"pin":"99158441"}' los cuatro ultimos son el pin
        if QR_Te == 3: CE_datos = dat					# datos leidos para enviar

        if P_Mensajes:
            print '-------------------------------------'
            print 'envio'
            print '-------------------------------------'
            print 'URL :'+ CE_url
            print 'Datos :'+ CE_datos

        return Get_Post_try_catch('POST', CE_url, CE_datos, CE_cabeceras, 2)


def Usuarios_Activos(T_actual):

        global ID_Tarjeta
        global CE_V

        CE_peticion='NO'
        CE_cabeceras = {
        "Content-Type" : "application/json",
        "Fuseaccess-Id" : ID_Tarjeta,
        "Time-Scan" : T_actual
        }

        if CE_V != 0 : CE_url = IP_servidor+CE_rl[2]
        else		 : CE_url = IP_servidorP+CE_rl[2]

        if P_Mensajes:
            print '-------------------------------------'
            print 'Usuarios_Activos'
            print '-------------------------------------'
            print 'URL :'+ CE_url

        return Get_Post_try_catch('GET_SOLO_CABECERA', CE_url,'', CE_cabeceras, 2)




def Test_IP_Dominio (IP, Protoc):

        global CE_url
        global IP_servidorP
        global IP_servidor
        global CE_V

        #print Protoc

        CE_peticion='NO'

        #CE_url = 'http://' + IP+CE_rl[4]         #CE_rl[4]
        CE_url = str(Protoc) + '://' + IP + CE_rl[4]         #CE_rl[4]
        #print CE_url

        if P_Mensajes:
            print '-------------------------------------'
            print 'Test_IP_Dominio'
            print '-------------------------------------'

        print 'URL :'+ CE_url

        return Get_Post_try_catch('GET_SIN_PARAMETROS', CE_url, '', '', 1)

        """
        try:
                CE_peticion = requests.get(CE_url, timeout=1)
                return CE_peticion
        except:
                #print requests.error
                return CE_peticion
        """

#--------------------------------------------------------
#--------------------------------------------------------
#               revicion de conecion e Internet
#--------------------------------------------------------
#--------------------------------------------------------

def Estatus_Coneccion (c):
        res2 = commands.getoutput('cat /sys/class/net/'+c+'/carrier')
        if res2 == '0':     return 0 #  print 'Desconectado'
        else:               return 1 # print 'Conectado'


def Estados_Internet():
        Sres = ""
        Cantidad =0
        res = commands.getoutput('ls /sys/class/net/')
        redes =res.split("\n")

        for x1 in range(len(redes)):
                c= redes[x1]
                #print c
                if c.find('eth') != -1: #print 'ethernet'
                        if Estatus_Coneccion (c) == 0:  #print 'ED'
                            Sres = Sres + 'ED'
                            Cantidad+=1
                        else:                           #print 'EC'
                            Sres = Sres + 'EC'
                            Cantidad+=1
                if c.find('wlan') != -1: #print 'Wifi'

                        if Estatus_Coneccion (c) == 0:  #print 'WD'
                                Sres = Sres + 'WD'
                                Cantidad+=1
                        else:                           #print 'WC'
                                Sres = Sres + 'WC'
                                Cantidad+=1
        #print str(Cantidad) + Sres
        return  str(Cantidad) + Sres

def IP_Valido(IP):
    try:
        socket.inet_aton(IP)
        if IP.count('.') == 3:
            return True
        else:
            return False
    except socket.error:
        return False

def Dominio_Valido(Dominio):
    Resolver = "host -t A  " + Dominio + "   | grep address | awk {'print $4'}"
    address = commands.getoutput(Resolver)
    try:
        if IP_Valido(address):
            return address
        else:
            return False
    except socket.error:
        return False

def Cambiar_LINK():
    global IP_servidor
    IP_servidor = Link_servidor()




#--------------------------------------------------------
def Check_Respuestas(Respuesta):
    print Respuesta
    #print Respuesta.status_code
    #.find(Respuesta.strip())
    if Respuesta.strip() == 'OK':
        #print 'Respuesta correcta'
        return True
    else:
        #print 'Respuesta incorrecta'
        #print Respuesta.text
        return False

def Filtro_C(s): # eliminar los caracteres y estructura Jason

    s = s.replace('"',"")
    s = s.replace('[',"")
    s = s.replace('{',"")
    s = s.replace(']',"")
    s = s.replace('}',"")
    s = s.replace('data:',"")
    s = s.replace(',',"\r\n")
    return s


def Nuevo_Firmware_Listado_Dominios():

    Vinculado = Leer_Archivo(41).replace('\n','')
    Domino_Actual = Leer_Archivo(31).replace('\n','')
    Dominio_Listado  = Leer_Archivo(35).replace('\n','')

    #print Vinculado
    #print Domino_Actual

    #por el moneto el link deve ser compelto

    #if Dominio_Listado.find("http://") == -1:
    #    Dominio_Listado = "http://" + Dominio_Listado
    #elif Dominio_Listado.find("https://") == -1:
    #    Dominio_Listado = "https://" + Dominio_Listado

    #print 'S: ' + Dominio_Listado

    try:
        #CE_peticion = requests.get("http://192.168.1.113/Actualizar/", timeout=2)
        CE_peticion = requests.get(Dominio_Listado, timeout=2)
        if CE_peticion.status_code == 200:
            Texto =  Filtro_C(CE_peticion.text)
            Texto = Texto.split("\r\n")
            for x in Texto:
                T = x.split(":")
                #print T
                #print T[0].find(Vinculado)
                #print Vinculado.strip()
                #print T[0]
                if T[0].find(Vinculado.strip()) != -1:
                    #print T[1]
                    if T[1].strip() != Domino_Actual.strip():
                        if P_Mensajes:
                            print 'Cambiar Dominio' # para por un test previo
                        return T[1].strip() #retorna el Dominio
                    else:
                        if P_Mensajes:
                            print  'Error : Es Igual el Dominio'
                        return 'Error : Es Igual el Dominio'
            if P_Mensajes:
                print  'Error : No Estoy en la Lista'
            return 'Error : No Estoy en la Lista'
        else :
            if P_Mensajes:
                print 'Error :'+str(CE_peticion.status_code)
                print CE_peticion.text
            return 'Error :'+str(CE_peticion.status_code)

    #except requests.ConnectionError, e:
    except :
        #print e
        if P_Mensajes:
            print  'Error :Conection Dominio Listado'
        return 'Error :Conection Dominio Listado'





def Agregar_Nuevo_Servidor(N_Servidor):

        print 'guardar en archivos'


        #N_Servidor = Nuevo_Servidor.get()
        N_Servidor = N_Servidor.strip()
        print '-----------------------------'
        print N_Servidor
        print '-----------------------------'

        Variable_Dominio=''
        Variable_IP=''
        #print 'hola'

        try:
                socket.inet_aton(N_Servidor)
                if N_Servidor.count('.') == 3:
                    print '---------------------------------'
                    print '1. Prueba de coneccion por IP'
                    print '---------------------------------'

                    print 'IP :' +str(N_Servidor)

                    Respuesta = Test_IP_Dominio(N_Servidor, 'http')
                    #print Respuesta
                    #if Respuesta !='NO':
                    if Respuesta.find("Error") == -1:
                        Check_Res= Check_Respuestas(Respuesta)
                        if Check_Res == True:
                            print 'Esta IP es valida'
                            Variable_IP=str(N_Servidor)

                            print Variable_IP
                            #---------------------------------
                            Borrar(32)
                            Escrivir_Archivo(Variable_IP,32) #N_A_IP_Servidor
                            Borrar(36)
                            Escrivir_Archivo('10',36) ## tipo de link a formar 11 0 10

                            #---------------------------------
                            # commands.getoutput('sudo reboot')
                            #Mensajes('Test OK,Esta IP es valida se cambiara, pero el dominio sera el mismo.','OK')
                            return True
                        else:
                            #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                            print 'Test Error,La IP no Funciona'
                            return False

                    else:
                        #Mensajes('Test Error,La IP no contesto.','Error')
                        print 'Test Error,La IP no contesto'
                        return False

        except socket.error:
                print '---------------------------------'
                print 'NO es una IP revision por Dominio'
                print '---------------------------------'
                IP = Dominio_Valido(N_Servidor)
                Variable_Dominio = N_Servidor
                Variable_IP = str(IP)
                #print IP
                if IP != False:

                        Test_IP_Dom=0
                        print '---------------------------------'
                        print 'Prueba de coneccion por IP'
                        print '---------------------------------'

                        print 'IP :' +str(IP)
                        print 'Con http'

                        Respuesta= Test_IP_Dominio(IP, 'http')
                        #print Respuesta
                        #if Respuesta !='NO':
                        if Respuesta.find("Error") == -1:
                            Check_Res= Check_Respuestas(Respuesta)

                            if Check_Res == True:
                                print 'Esta IP es valida'
                                Test_IP_Dom=10
                                #Variable_IP = str(Respuesta)
                                #Mensajes('Test OK,Esta IP es valida se cambiara, pero el dominio sera el mismo.','OK')
                            else:
                                print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                        else:
                            print 'Test Error,La IP no contesto'


                        print 'Con https'

                        Respuesta= Test_IP_Dominio(IP, 'https')
                        #print Respuesta
                        #if Respuesta !='NO':
                        if Respuesta.find("Error") == -1:
                            Check_Res= Check_Respuestas(Respuesta)

                            if Check_Res == True:
                                print 'Esta IP es valida'
                                Test_IP_Dom=Test_IP_Dom+100
                                #Variable_IP = str(Respuesta)
                                #Mensajes('Test OK,Esta IP es valida se cambiara, pero el dominio sera el mismo.','OK')
                            else:
                                print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                        else:
                            print 'Test Error,La IP no contesto'


                        print '---------------------------------'
                        print 'Prueba de coneccion por Dominio'
                        print '---------------------------------'

                        print 'Dominio :' +N_Servidor
                        print 'Con http'

                        Respuesta= Test_IP_Dominio(N_Servidor, 'http')
                        #print Respuesta
                        #if Respuesta !='NO':
                        if Respuesta.find("Error") == -1:
                            Check_Res= Check_Respuestas(Respuesta)
                            if Check_Res == True:
                                print 'Esta Dominio es valida'
                                Test_IP_Dom=Test_IP_Dom+1
                                #Variable_Dominio = N_Servidor
                            else:
                                print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                        else:
                            print 'Test Error,El dominio no contesto'

                        print 'Con https'

                        Respuesta= Test_IP_Dominio(N_Servidor, 'https')
                        #print Respuesta
                        #if Respuesta !='NO':
                        if Respuesta.find("Error") == -1:

                            Check_Res= Check_Respuestas(Respuesta)
                            if Check_Res == True:
                                print 'Esta Dominio es valida'
                                Test_IP_Dom=Test_IP_Dom+1000
                                #Variable_Dominio = N_Servidor
                            else:
                                print 'Test Error, '+ str(Check_Res)+' La IP no Funciona'
                                #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
                        else:
                            print 'Test Error,El dominio no contesto'


                        print Test_IP_Dom

                        if Test_IP_Dom == 0:
                            print 'Test 0 Error, http Dominio NO, IP NO; https Dominio NO, IP NO.','Error'
                            return False
                        """
                        if Test_IP_Dominio == 1:    Mensajes('Test 25%  OK, http Dominio OK, IP NO; https Dominio NO, IP NO.','OK')
                        if Test_IP_Dominio == 10:   Mensajes('Test 25%  OK, http Dominio NO, IP OK; https Dominio NO, IP NO.','OK')
                        if Test_IP_Dominio == 11:   Mensajes('Test 50%  OK, http Dominio OK, IP OK; https Dominio NO, IP NO.','OK')

                        if Test_IP_Dominio == 100:  Mensajes('Test 25%  OK, http Dominio NO, IP NO; https Dominio NO, IP OK.','OK')
                        if Test_IP_Dominio == 101:  Mensajes('Test 50%  OK, http Dominio OK, IP NO; https Dominio NO, IP OK.','OK')
                        if Test_IP_Dominio == 110:  Mensajes('Test 50%  OK, http Dominio NO, IP OK; https Dominio NO, IP OK.','OK')
                        if Test_IP_Dominio == 111:  Mensajes('Test 75%  OK, http Dominio OK, IP OK; https Dominio NO, IP OK.','OK')

                        if Test_IP_Dominio == 1000: Mensajes('Test 25%  OK, http Dominio NO, IP NO; https Dominio OK, IP NO.','OK')
                        if Test_IP_Dominio == 1001: Mensajes('Test 50%  OK, http Dominio OK, IP NO; https Dominio OK, IP NO.','OK')
                        if Test_IP_Dominio == 1010: Mensajes('Test 50%  OK, http Dominio NO, IP OK; https Dominio OK, IP NO.','OK')
                        if Test_IP_Dominio == 1011: Mensajes('Test 75%  OK, http Dominio OK, IP OK; https Dominio OK, IP NO.','OK')

                        if Test_IP_Dominio == 1100: Mensajes('Test 50%  OK, http Dominio NO, IP NO; https Dominio OK, IP OK.','OK')
                        if Test_IP_Dominio == 1101: Mensajes('Test 75%  OK, http Dominio OK, IP NO; https Dominio OK, IP OK.','OK')
                        if Test_IP_Dominio == 1110: Mensajes('Test 75%  OK, http Dominio NO, IP OK; https Dominio OK, IP OK.','OK')
                        if Test_IP_Dominio == 1111: Mensajes('Test 100% OK, http Dominio OK, IP OK; https Dominio OK, IP OK.','OK')
                        """

                        if Test_IP_Dom !=0:
                            print 'guardando y reiniciando'
                            print Test_IP_Dom
                            print Variable_IP
                            print Variable_Dominio


                            #print Variable_IP
                            #--------------- para cambior ----
                            Borrar(32)
                            Escrivir_Archivo(Variable_IP,32)#N_A_IP_Servidor
                            Borrar(31)
                            Escrivir_Archivo(Variable_Dominio,31)#N_A_Dominio_Servidor
                            Borrar(36)
                            Escrivir_Archivo(str(Test_IP_Dom),36)#N_A_Dominio_Servidor

                            # commands.getoutput('sudo reboot')
                            return True

                else:
                        print 'Dominio NO Valido, no hay IP asociada'
                        #Mensajes('Dominio NO Valido, no hay IP asociada.','Error')
                        return False


if P_Mensajes:
    print 'ID   :' + ID_Tarjeta
    Ver_Link()

#-----------------------------------------------
#                   Pruebas
#-----------------------------------------------

#Agregar_Nuevo_Servidor("192.168.1.113")

#print Nuevo_Firmware_Listado_Dominios()

#Firm = Leer_Archivo(17).replace('\n','')
#T = Tiempo()
#Firm = '2020.7.30.0'
#print Firm
#print T

#Respuesta = Veri_Firmware(T, Firm)

#Respuesta = Confimacion_Firmware(T, Firm,'') #revizar la perivion de errores
#Respuesta = ping()
#Respuesta = envio('dD3Wmu0p3f1lv9JGBTpWZfYXosQmMaBezhCJr9m2gKYjBDSIXU9t4sW55adM8PqnpF9yJjjHLd8bsz1fWdl0qg==.gm7dmny',T, 1)
#Respuesta = envio('1234',T, 1)
#Respuesta = envio('1234',T, 0)
#Respuesta = envio('que a pasado',T, 3)
#Respuesta = envio('"in_out":["8mhECm5D0KD5fKoDl2IuQQDN1AHeGEAvlZ788dfqrKg3kybxrdPHgkADCA6SAv/7nZGCy5WLVuvbOkOIgPUzbg==.gm7dmny.1606925351281.1.0.1"]}',T, 3)
#Respuesta = Usuarios_Activos(T)

#print 'Return:' + Respuesta

"""

print '---------------------------------'
print '1. Prueba de coneccion por IP'
print '---------------------------------'

print 'IP :' +str(IP)
Respuesta = Test_IP_Dominio(IP, 'http')
print Respuesta
#if Respuesta !='NO':
if Respuesta.find("Error") == -1:
    Check_Res= Check_Respuestas(Respuesta)
    if Check_Res == True:
        print 'Esta IP es valida'
        #Mensajes('Test OK,Esta IP es valida se cambiara, pero el dominio sera el mismo.','OK')
        return True
    else:
        print 'Test Error,La IP no Funciona'
        #Mensajes('Test Error, '+ str(Check_Res)+' La IP no Funciona.','Error')
        return False
else:
    print 'Test Error,La IP no contesto'
    #Mensajes('Test Error,La IP no contesto.','Error')
    return False

"""
