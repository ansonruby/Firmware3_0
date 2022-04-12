#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor: Anderson Amaya Pulido

Libreria personal para el manejo de rutas del aplicativo.











"""
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
#                                   Rutas Generales
#---------------------------------------------------------------------------------------
FIRMBK    = '/home/pi/FirmwareBK/'
FIRM    = '/home/pi/Firmware/'                                          # Ruta      Firmware
COMMA   = 'db/Command/'                                                 # Ruta      Comandos
CONF    = 'db/Config/'                                                  # Ruta      Configuraciones
STATUS  = 'db/Status/'                                                  # Ruta      Estados
IMG     = 'img/'                                                        # Ruta      Imagenes del firmware
DISP    = '/home/pi/.ID/'                                               # Ruta      Informacion Dispositivo
DATA    = 'db/Data/'                                                    # Ruta      Base de datos
DWEB    = '/var/www/html/'                                              # Ruta      WEB
ACTUALI    = '/home/pi/Actualizador/'                                      # Ruta      Actualizador

#---------------------------------------------------------------------------------------
#                                  Datos del dispositivo
#---------------------------------------------------------------------------------------

INF_FIRMWARE    = FIRM + 'README.md'                                    # Datos y contenido del repositorio git
INF_VERCION     = FIRM + CONF + 'Vercion/Vercion_Firmware.txt'          # Datos de la vercion del Firmware
INF_DISPO       = DISP + 'Datos_Creacion.txt'                           # Datos propios del dispositivo pieza 1 UUID
KEY_DISPO       = DISP + 'Key.txt'                                      # Datos propios del dispositivo

#---------------------------------------------------------------------------------------
#                                  Firmware
#---------------------------------------------------------------------------------------

COM_FIRMWARE    = FIRM + COMMA + 'Firmware/Com_Firmware.txt'            # Configuraciones personalizadas del Firmware

#---------------------------------------------------------------------------------------
#                                  Base de datos separacion por tipos de qr
#---------------------------------------------------------------------------------------
TAB_USER_TIPO_1_1   = FIRM + DATA + 'Tipo_1_1/Tabla_Usuarios.txt'         # Usuarios del servidor o counter
TAB_AUTO_TIPO_1_1   = FIRM + DATA + 'Tipo_1_1/Tabla_Autorizados.txt'      # Registro de usuarios autorizados entrada y salida
TAB_USER_TIPO_1     = FIRM + DATA + 'Tipo_1/Tabla_Usuarios.txt'         # Usuarios del servidor o counter
TAB_AUTO_TIPO_1     = FIRM + DATA + 'Tipo_1/Tabla_Autorizados.txt'      # Registro de usuarios autorizados entrada y salida
TAB_PINES_TIPO_1    = FIRM + DATA + 'Tipo_1/Tabla_Pines.txt'            # pines de usuarios generados
TAB_USER_TIPO_2     = FIRM + DATA + 'Tipo_2/Tabla_Usuarios.txt'         # Usuarios del servidor o counter
TAB_AUTO_TIPO_2     = FIRM + DATA + 'Tipo_2/Tabla_Autorizados.txt'      # Registro de usuarios autorizados entrada y salida
TAB_USER_TIPO_2_1   = FIRM + DATA + 'Tipo_2_1/Tabla_Usuarios.txt'       # Usuarios del servidor o counter
TAB_AUTO_TIPO_2_1   = FIRM + DATA + 'Tipo_2_1/Tabla_Autorizados.txt'    # Registro de usuarios autorizados entrada y salida
TAB_USER_TIPO_3     = FIRM + DATA + 'Tipo_3/Tabla_Usuarios.txt'         # Usuarios del servidor o counter
TAB_AUTO_TIPO_3     = FIRM + DATA + 'Tipo_3/Tabla_Autorizados.txt'      # Registro de usuarios autorizados entrada y salida

TAB_ENV_SERVER      = FIRM + DATA + 'Autorizaciones/Tabla_Envio_server.txt'      # Registro de usuarios autorizados por el dispositivo

#---------------------------------------------------------------------------------------
#                                  Led RGB -> WS2812B
#---------------------------------------------------------------------------------------

COM_LED         = FIRM + COMMA + 'Led_RGB/Com_Led.txt'                  # Comandos para el control de los led

#---------------------------------------------------------------------------------------
#                                  Rele dual
#---------------------------------------------------------------------------------------

CONF_TIEM_RELE  = FIRM + CONF + 'Rele/Tiempo_Rele.txt'                  # Configuracion rele
CONF_DIREC_RELE = FIRM + CONF + 'Rele/Direccion_Rele.txt'               # Configuracion Direccion rele
CONF_COMU_RELE  = FIRM + CONF + 'Rele/Tipo_Rele.txt'                    # Configuracion de tipo de relevos
COM_TX_RELE     = FIRM + COMMA + 'Rele/Com_Tx_Rele.txt'                 # Comando de comunicaiones relevos serial
COM_RELE        = FIRM + COMMA + 'Rele/Com_Rele.txt'                    # Comando relevos

#---------------------------------------------------------------------------------------
#                                  Buzzer 5V
#---------------------------------------------------------------------------------------

COM_BUZZER      = FIRM + COMMA + 'Buzzer/Com_Buzzer.txt'                # Archivo de comandos

#---------------------------------------------------------------------------------------
#                                  Sensor QR
#---------------------------------------------------------------------------------------

COM_QR          = FIRM + COMMA + 'Qr/Com_Qr.txt'                        # Datos leidos del qr
STATUS_QR       = FIRM + STATUS + 'Qr/Status_Qr.txt'                    # Estado del qr
STATUS_REPEAT_QR= FIRM + STATUS + 'Qr/Repeat_Qr.txt'                    # Estado de repeticion del qr

#---------------------------------------------------------------------------------------
#                                   Teclado
#---------------------------------------------------------------------------------------
#-------------- imagenes
FONDO_1             = FIRM + IMG + "Teclado/keypad-fondo.png"           # Imagen Teclado normal
FONDO_2             = FIRM + IMG + "Teclado/Keypad-Borrar_Amarillo.png" # Imagen Teclado Borrar amarillo
Link_Denegado       = FIRM + IMG + "Teclado/denegado.png"               # Imagen X denegado
Link_Permitido      = FIRM + IMG + "Teclado/permitido.png"              # Imagen chulo permitido
Link_Per_Derecha    = FIRM + IMG + "Teclado/derecha.png"                # Imagen flecha a la derecha
Link_Alerta         = FIRM + IMG + "Teclado/alerta2.png"                # Imagen Alerta de qr repetido
#-------------- comados y estados
COM_TECLADO         = FIRM + COMMA + 'Teclado/Com_Teclado.txt'          # comandos teclados o lo digitado
STATUS_TECLADO      = FIRM + STATUS + 'Teclado/Status_Teclado.txt'      # Estados teclados o si digito
#-------------- Configuraciones ----
CONF_FLECHA_TECLADO = FIRM + CONF + 'Teclado/Flecha_Teclado.txt'

#---------------------------------------------------------------------------------------
#                                   Red
#---------------------------------------------------------------------------------------

STATUS_RED          = FIRM + STATUS + 'Red/Status_Red.txt'              # Estados de la red ethernet y wifi
#-------------- Configuraciones
CONF_WIF_ETHE       ='/etc/wpa_supplicant/wpa_supplicant.conf'
CONF_IP_STATIC      ='/etc/dhcpcd.conf'
#---------------------------------------------------------------------------------------
#                                   Usuarios
#---------------------------------------------------------------------------------------

STATUS_USER     = FIRM + STATUS + 'Usuario/Status_User.txt'             # Estado de Usuarios

#---------------------------------------------------------------------------------------
#                                   CONTER_Comunicaciones
#---------------------------------------------------------------------------------------

CONT_SEND_DATA_PATH = '/home/pi/Firmware/ComCounter/db/datatosend.txt'          # datos autorizados por el dispositivo
CONT_SEND_FLAG_PATH = '/home/pi/Firmware/ComCounter/db/flagtosend.txt'          # Bandera de control de escritura

CONT_RECEIVED_DATA_PATH = '/home/pi/Firmware/ComCounter/db/datareceived.txt'    # Actualizar Usuarios
CONT_RECEIVED_FLAG_PATH = '/home/pi/Firmware/ComCounter/db/flagreceived.txt'    # Bandera de control de escritura

#---------------------------------------------------------------------------------------
#                                   Configuracion de autorizaciones
#---------------------------------------------------------------------------------------

CONF_AUTORIZACION_QR       = FIRM + CONF + 'Autorizaciones/Qr/Tipos.txt'        #
CONF_AUTORIZACION_TECLADO  = FIRM + CONF + 'Autorizaciones/Teclado/Tipos.txt'   #

#---------------------------------------------------------------------------------------
#                                   Servidor
#---------------------------------------------------------------------------------------
CONF_DOMI_SERVER      = FIRM + CONF + 'Server/Dominio_Servidor.txt'           #
CONF_IP_SERVER        = FIRM + CONF + 'Server/IP_Servidor.txt'                #
CONF_M_CONEX_SERVER   = FIRM + CONF + 'Server/Mejor_Conexion.txt'             #

#---------------------------------------------------------------------------------------
#                                   Menu Web
#---------------------------------------------------------------------------------------
COM_WEB_ANTES         = FIRM + STATUS+ 'Web/Comandos_Web.txt'
PRO_WEB               = FIRM + STATUS+ 'Web/Procesos_web.txt'
COM_WEB               = DWEB +'Admin/include/Control_Web.txt'

#---------------------------------------------------------------------------------------
#                                   Actualizador
#---------------------------------------------------------------------------------------

RESP_PET_FIRMWARE       = ACTUALI + 'db/Respuesta_Peticion_Firmware.txt'
STATUS_ACTUALIZADOR     = ACTUALI + 'db/Estado_Actualizador.txt'
MEM_ACTUALIZADOR        = ACTUALI + 'db/Memoria_Actualizador.txt'
COM_ACTUALIZADOR        = FIRM + COMMA + 'Actualizador/Forzar_Actualizador.txt'
