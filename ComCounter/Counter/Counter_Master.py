#!/home/pi/Firmware/ComCounter/Counter/bin/python3
from threading import Thread
from flask import Flask, request
from flask_cors import CORS
from Crypto.Cipher import AES
from waitress import serve
import websocket
import requests
import json
import time
import os
import base64
import hashlib
import uuid
import logging
import datetime
import subprocess
import ast

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Cloud server constants
CLOUD_SERVER_DOMAIN_PATH = CURRENT_DIR_PATH + \
    "/../../db/Config/Server/Dominio_Servidor.txt"
CLOUD_SERVER_IP_PATH = CURRENT_DIR_PATH + \
    "/../../db/Config/Server/IP_Servidor.txt"
CLOUD_SERVER_BEST_OPTION_PATH = CURRENT_DIR_PATH + \
    "/../../db/Config/Server/Mejor_Conexion.txt"
DEVICE_CURRENT_UUID = uuid.uuid1()

# Internal db constants
DB_DIR_NAME = CURRENT_DIR_PATH+"/db"
QR_LIST_PATH = DB_DIR_NAME+"/data.txt"
AUTH_LIST_PATH = DB_DIR_NAME+"/auth.txt"
OFFLINE_LIST_PATH = DB_DIR_NAME+"/offline.txt"
LAST_LOG_LIST_PATH = DB_DIR_NAME+"/lastLog.txt"
ACTIVE_CONECTION = CURRENT_DIR_PATH+"/../db/flagtosend.txt"

# Cloud server constants
SERVER_UPDATE_TIME = 3600

# Cloud server variables
cloud_server_domain = ""
login_token = ""
bookingOffice_id = ""
active_devices = []


def Get_Rout_server():
    mejor_opcion = ""
    IP_Ser = ""
    Domi_Ser = ""
    with open(CLOUD_SERVER_DOMAIN_PATH, 'r', encoding='utf-8', errors='replace') as df:
        Domi_Ser = df.read().strip()
        df.close()
    with open(CLOUD_SERVER_IP_PATH, 'r', encoding='utf-8', errors='replace') as df:
        IP_Ser = df.read().strip()
        df.close()
    with open(CLOUD_SERVER_BEST_OPTION_PATH, 'r', encoding='utf-8', errors='replace') as df:
        mejor_opcion = df.read().strip()
        df.close()

    opciones = {'0': 'http://' + IP_Ser,
                '1': 'http://' + Domi_Ser,
                '10': 'http://' + IP_Ser,
                '11': 'http://' + IP_Ser,
                '100': 'https://' + IP_Ser,
                '101': 'https://' + IP_Ser,
                '110': 'https://' + IP_Ser,
                '111': 'https://' + IP_Ser,
                '1000': 'https://' + Domi_Ser,
                '1001': 'https://' + Domi_Ser,
                '1010': 'http://' + IP_Ser,
                '1011': 'http://' + IP_Ser,
                '1100': 'https://' + IP_Ser,
                '1101': 'https://' + IP_Ser,
                '1110': 'https://' + IP_Ser,
                '1111': 'https://' + IP_Ser}

    # return 'https://solutions.fusepong.com'
    # return 'http://192.168.20.41:3000'
    return opciones[mejor_opcion]


def log_in():
    data = encrypt({"attributes": {'email': "admin_wicho@fusepong.com",
                                   'password': "password"}}).decode("utf-8")
    # data = encrypt({"attributes": {'email': "luding@counter.com",
    #                'password': "password"}}).decode("utf-8")
    try:
        petition = requests.post(
            url=cloud_server_domain+"/api/users/sign_in",
            data={"data": data},
            headers={'X-Device-ID': str(DEVICE_CURRENT_UUID)})
        if petition.status_code == 201:
            with open(LAST_LOG_LIST_PATH, 'w', encoding='utf-8', errors='replace') as dfw:
                dfw.write(data)
                dfw.close()
            return [petition.json()['data']['id'], petition.json()['meta']['authentication_token']]
    except:
        print("not internet connection")


def get_devices():
    try:
        petition = requests.get(
            url=cloud_server_domain+"/api/app/scan_devices/find_ip_devices",
            params={"id": bookingOffice_id},
            headers={'X-Device-ID': str(DEVICE_CURRENT_UUID), "Authorization": "Bearer "+login_token})
        if petition.status_code == 200:
            return petition.json()["data"]["scanners"]
        else:
            return []
    except:
        print("not internet connection")


def get_users():
    tickets_offline = None
    with open(OFFLINE_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
        tickets_offline_text = df.read().strip()
        df.close()
        if tickets_offline_text != "":
            tickets_offline = tickets_offline_text.split("\n")
    if tickets_offline:
        tickets_offline_json = []
        for ticket in tickets_offline:
            ticket_json = {}
            if ticket.strip() == "":
                continue

            ticket_json = json.loads(ticket)
            if not "user_id" in ticket_json:
                ticket_json["user_id"] = bookingOffice_id
            tickets_offline_json.append(ticket_json)
        petition = requests.post(
            url=cloud_server_domain+"/api/app/bookings/create_ticket",
            data={"data": encrypt(
                {"tickets": tickets_offline_json})},
            headers={'X-Device-ID': str(DEVICE_CURRENT_UUID), "Authorization": "Bearer "+login_token})
        if petition.status_code == 201 or petition.status_code == 202:
            with open(OFFLINE_LIST_PATH, 'w', encoding='utf-8', errors='replace') as dfw:
                dfw.write("")
                dfw.close()

    in_out = None
    with open(AUTH_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
        auth_list_text = df.read().strip()
        df.close()
        if auth_list_text != "":
            in_out = auth_list_text.split("\n")
    # print(in_out)
    if in_out:
        # print("in_out")
        petition = requests.post(
            url=cloud_server_domain+"/api/access/update_scan_actions",
            data={"data": encrypt(
                {"bookingOffice_id": bookingOffice_id, "in_out": in_out})},
            headers={'X-Device-ID': str(DEVICE_CURRENT_UUID), "Authorization": "Bearer "+login_token})
        if petition.status_code == 200 or petition.status_code == 202:
            with open(AUTH_LIST_PATH, 'w', encoding='utf-8', errors='replace') as dfw:
                dfw.write("")
                dfw.close()
    petition = requests.get(
        url=cloud_server_domain+"/api/access/get_granted_users_pi",
        params={"bookingOffice_id": bookingOffice_id},
        headers={'X-Device-ID': str(DEVICE_CURRENT_UUID), "Authorization": "Bearer "+login_token})
    if petition.status_code == 200:
        return save_users(petition.json())


def save_users(data):
    granted_users = []
    granted_users.extend(data["data"])
    with open(QR_LIST_PATH, 'w', encoding='utf-8', errors='replace') as dfw:
        dfw.write("\n".join(granted_users)+"\n")
        dfw.close()

    offline_list = []
    with open(OFFLINE_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
        offline_list_text = df.read().strip()
        df.close()
        if offline_list_text != "":
            offline_list = offline_list_text.split("\n")
            with open(OFFLINE_LIST_PATH, 'w', encoding='utf-8', errors='replace') as dfw:
                dfw.write("")
                dfw.close()

    for ticket in offline_list:
        if ticket.strip() != "":
            create_ticket(json.loads(ticket))

    for ticket in data["tickets"]:
        create_ticket(ticket)

    with open(QR_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
        qr_list = df.read().strip()
        df.close()
        granted_users = qr_list.split("\n")
    return granted_users


def auth_petition(qr, ws):
    qr_list = []
    data = qr.split(".")
    ans = False
    access_identifier = "1"
    with open(QR_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
        qr_list_text = df.read().strip()
        df.close()
        qr_list = qr_list_text.split("\n")
    for compare_qr in qr_list:
        if compare_qr == "":
            continue
        compare_data = compare_qr.split(".")
        if compare_data[0] == "6" and data[0] == "6" and compare_data[2] == data[1]:
            access_identifier = "11"
            ans = True
            break
        if len(data) == 2 and len(compare_data) == 2 and data[1] == compare_data[0]:
            access_identifier = "1"
            ans = True
            break
        elif len(data) == 2 and len(compare_data) == 2 and data[0] == "" and data[1] == compare_data[1]:
            access_identifier = "2"
            ans = True
            break
        elif len(data) == 5 and len(compare_data) == 5 and ".".join(data[0:-1]) == ".".join(compare_data[0:-1]):
            access_identifier = "1"
            offline_list = []
            with open(OFFLINE_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
                offline_list_text = df.read().strip()
                df.close()
                if offline_list_text.strip() != "":
                    offline_list = offline_list_text.split("\n")
            for existent_ticket_text in offline_list:
                if existent_ticket_text.strip() == "":
                    continue
                existent_ticket = json.loads(existent_ticket_text)
                if existent_ticket["qr"] == compare_qr:
                    if int(existent_ticket["uses"]) > 1:
                        existent_ticket["uses"] = str(
                            int(existent_ticket["uses"])-1)
                        offline_position = offline_list.index(
                            existent_ticket_text)
                        existent_ticket_text = json.dumps(existent_ticket)
                        offline_list[offline_position] = existent_ticket_text
                    else:
                        offline_list.remove(existent_ticket_text)
                    break
            with open(OFFLINE_LIST_PATH, 'w', encoding='utf-8', errors='replace') as dfw:
                dfw.write("\n".join(offline_list))
                dfw.close()
            qr_list.remove(compare_qr)
            ans = True
            with open(QR_LIST_PATH, 'w', encoding='utf-8', errors='replace') as dfw:
                dfw.write("\n".join(qr_list))
                dfw.close()
            break
    if ans == True:
        with open(AUTH_LIST_PATH, 'a', encoding='utf-8', errors='replace') as dfw:
            dfw.write(qr+"."+str(int(time.time()*1000.0)) +
                      "."+access_identifier+".0.1."+str(ws.server_id)+"\n")
            dfw.close()
    return ans


def create_ticket(ticket):
    offline_list = []
    with open(OFFLINE_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
        offline_list_text = df.read().strip()
        df.close()
        if offline_list_text.strip() != "":
            offline_list = offline_list_text.split("\n")
    valid_ref_number = True
    for existent_ticket in offline_list:
        if existent_ticket.strip() == "":
            continue
        existent_ticket = json.loads(existent_ticket)
        if existent_ticket["ref_number"] == ticket["ref_number"]:
            valid_ref_number = False
            break
    if valid_ref_number:
        if True:  # Add logic for time validation
            qr_type = 3
            encrypted_rut = encrypt(
                ticket["identification_number"]).decode("utf-8")
            if not "uses" in ticket:
                ticket["uses"] = ticket["quantity"]
            ticket["qr"] = str(qr_type) + "." + encrypt(bookingOffice_id).decode("utf-8") + \
                "." + encrypted_rut + "." + "1" + ".0"
            if not "user_id" in ticket:
                ticket["user_id"] = bookingOffice_id
            qrs = (ticket["qr"]+"\n")*int(ticket["uses"])
            with open(QR_LIST_PATH, 'a', encoding='utf-8', errors='replace') as dfw:
                dfw.write(qrs)
                dfw.close()
            with open(OFFLINE_LIST_PATH, 'a', encoding='utf-8', errors='replace') as dfw:
                dfw.write(json.dumps(ticket)+"\n")
                dfw.close()
    return valid_ref_number


def search_user_tickets(identification_number):
    offline_list = []
    with open(OFFLINE_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
        offline_list_text = df.read().strip()
        df.close()
        if offline_list_text.strip() != "":
            offline_list = offline_list_text.split("\n")
    for existent_ticket_text in offline_list:
        if existent_ticket_text.strip() == "":
            continue
        existent_ticket = json.loads(existent_ticket_text)
        if int(existent_ticket["identification_number"]) == int(identification_number):
            return ";".join(
                ["<" + ".".join(existent_ticket["qr"].split(".")[0:-1]) +
                 "." + str(int(time.time()*1000.0)) +
                 ">"] * int(existent_ticket["uses"])
            )
    return None


def encrypt(data):
    iv = base64.b64decode("G7qeaR2Yb4DAgk92ZQHdjQ==")
    passphraseDgst = hashlib.sha256('ImAwesomeAndHappy'.encode()).digest()
    cipher = AES.new(passphraseDgst, AES.MODE_CBC, iv)
    data = json.dumps(data)
    pad = 16 - len(data) % 16
    data += pad * chr(pad)
    encyrpted_data = base64.b64encode(cipher.encrypt(data)).strip()
    return encyrpted_data


def server_updater():
    while True:
        desconnection = True
        if os.path.exists(ACTIVE_CONECTION):
            with open(ACTIVE_CONECTION, 'r', encoding='utf-8', errors='replace') as df:
                desconnection = df.read().strip() == "3"
                df.close()
        if desconnection:
            # print("desconected")
            break
        if login_token != "":
            get_users()
        time.sleep(SERVER_UPDATE_TIME)


def socket_guardian():
    global active_devices
    while True:
        new_active_devices = []
        for device in active_devices:
            try:
                if not "ws" in device or device["ws"].sock == None:
                    def ws_run():
                        ws = websocket.WebSocketApp(device["ip"],
                                                    on_open=socket_on_open,
                                                    on_message=socket_on_message,
                                                    on_error=socket_on_error,
                                                    on_close=socket_on_close)
                        ws.procesing = True
                        ws.server_id = device["id"]
                        device["ws"] = ws
                        ws.run_forever()
                    Thread(target=ws_run).start()
                elif not device["ws"].procesing:
                    device["ws"].send(json.dumps(
                        {'type': "Test connection", 'status': "1"}))
            except:
                print("error in "+device["ip"])
            finally:
                new_active_devices.append(device)

        active_devices = new_active_devices

        time.sleep(0.8)

        desconnection = True
        if os.path.exists(ACTIVE_CONECTION):
            with open(ACTIVE_CONECTION, 'r', encoding='utf-8', errors='replace') as df:
                desconnection = df.read().strip() == "3"
                df.close()
        if desconnection:
            # print("desconected")
            break


def socket_on_open(ws):
    ws.procesing = True
    if not os.path.exists(DB_DIR_NAME):
        os.makedirs(DB_DIR_NAME)
    if not os.path.exists(QR_LIST_PATH):
        open(QR_LIST_PATH, 'w', encoding='utf-8', errors='replace').close()


def socket_on_message(ws, msg):
    # print(ws.url)
    try:
        msg = msg.strip()
        # print(msg)
        ws.procesing = True
        req = msg.split("////\n")
        header = json.loads(req[0])
        if header["type"] == "update":
            qr_list_size = 0
            with open(QR_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
                qr_list = df.read().strip()
                df.close()
                qr_list_size = len(qr_list.split("\n"))

            ws.send(json.dumps({'type': 'updateDevice',
                    'size': [qr_list_size, 0], 'status': "1"})+"////\n" + datetime.datetime.now().strftime("%mFu%dse%Ypong"))
        else:
            if header["type"] == "authTicket":
                access = ""
                if auth_petition(req[1], ws) == True:
                    access = "Access granted-E.0"
                else:
                    access = "Access denied.-1"
                # print(access)
                ws.send(json.dumps(
                    {'type': "authTicket", 'status': "1", 'size': 1})+"////\n"+access)
            ws.send(json.dumps({'type': "recived", 'status': "1"}))

        ws.procesing = False
    except:
        # print("message error")
        ws.close()


def socket_on_error(ws, error):
    ws.sock = None
    ws.close()
    # print(error)


def socket_on_close(ws, close_status_code, close_msg):
    ws.sock = None
    ws.close()
    # print("Closed")


def server_http():
    app = Flask(__name__)

    @app.route('/scannersPetition', methods=['GET'])
    def scannersPetition():
        if request.args.get('scannerAccessKey') == datetime.datetime.now().strftime("%mFu%dse%Ypong"):
            granted_users = get_users()
            tickets = "\n".join(granted_users)
            return {"status": 201, "tickets": tickets}, 201
        else:
            return {"status": 401, "error": "Invalid terminal"}, 401

    @app.route('/api_authentication', methods=['POST'])
    def api_authentication():
        last_log_data = []
        with open(LAST_LOG_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
            last_log_text = df.read().strip()
            df.close()
            last_log_data = last_log_text.split("\n")
        credentials = encrypt({"attributes": ast.literal_eval(base64.b64decode(
            request.json['credentials']).decode('utf-8'))}).decode("utf-8")
        if last_log_data[0] == credentials:
            return {"status": 201, "authorization_token": last_log_data[0]}, 201
        else:
            return {"status": 422, "error_message": "Credenciales incorrectas"}, 422

    @app.route('/process_voucher', methods=['POST'])
    def process_voucher():
        last_log_data = []
        with open(LAST_LOG_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
            last_log_text = df.read().strip()
            df.close()
            last_log_data = last_log_text.split("\n")
        auth = request.headers.get("Authorization") or request.headers.get(
            "authorization") or request.headers.get("AUTHORIZATION")
        if auth.strip() == "Bearer "+last_log_data[0]:
            valid_ref = create_ticket(ast.literal_eval(base64.b64decode(
                request.json['ticket']).decode('utf-8')))
            if valid_ref:
                return {"status": 201, "message": "Informacion recibida y procesada correctamente"}, 201
            else:
                return {"status": 400, "error_message": "ref_number repetido"}, 400
        else:
            return {"status": 401, "error_message": "Token de acceso invalido"}, 401

    @app.route('/search_active_tickets', methods=['POST'])
    def search_active_tickets():
        last_log_data = []
        with open(LAST_LOG_LIST_PATH, 'r', encoding='utf-8', errors='replace') as df:
            last_log_text = df.read().strip()
            df.close()
            last_log_data = last_log_text.split("\n")
        auth = request.headers.get("Authorization") or request.headers.get(
            "authorization") or request.headers.get("AUTHORIZATION")
        if auth.strip() == "Bearer "+last_log_data[0]:
            ticket_list = search_user_tickets(base64.b64decode(
                request.json['identification_number']).decode('utf-8'))
            if ticket_list:
                return {"status": 200, "tickets": ticket_list}, 200
            else:
                return {"status": 422, "error_message": "EL usuario no posee acceso"}, 422
        else:
            return {"status": 401, "error_message": "Token de acceso invalido"}, 401

    log = logging.getLogger("werkzeug")
    log.disabled = True
    app.logger.disabled = True
    CORS(app)
    serve(app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
    Thread(target=server_http).start()
    time.sleep(0.8)
    while True:
        try:
            exisṭ_other_connection = False
            if os.path.exists(ACTIVE_CONECTION):
                with open(ACTIVE_CONECTION, 'r', encoding='utf-8', errors='replace') as df:
                    exisṭ_other_connection = df.read().strip() != "3"
                    df.close()
            if not exisṭ_other_connection:
                ips = subprocess.getstatusoutput('hostname -I')
                if ips[0] == 0:
                    await_time = 0
                    try:
                        ips_list = ips[1].strip().split(" ")
                        ip_min_number = float(ips_list[0].split(".")[-1])
                        for ip in ips_list:
                            ip_numbers = ip.split(".")
                            if len(ip_numbers) == 4 and float(ip_numbers[-1]) < ip_min_number:
                                ip_min_number = float(ip_numbers[-1])
                        await_time = int(ip_min_number/2)
                    except:
                        await_time = 0
                        print("error find ip, defaut await time 0")
                    time.sleep(await_time)
                    if os.path.exists(ACTIVE_CONECTION):
                        with open(ACTIVE_CONECTION, 'r', encoding='utf-8', errors='replace') as df:
                            exisṭ_other_connection = df.read().strip() != "3"
                            df.close()
                    if exisṭ_other_connection:
                        continue
                    if not os.path.exists(DB_DIR_NAME):
                        os.makedirs(DB_DIR_NAME)
                    if not os.path.exists(QR_LIST_PATH):
                        open(QR_LIST_PATH, 'w', encoding='utf-8',
                             errors='replace').close()
                    if not os.path.exists(OFFLINE_LIST_PATH):
                        open(OFFLINE_LIST_PATH, 'w', encoding='utf-8',
                             errors='replace').close()

                    cloud_server_domain = Get_Rout_server()
                    credentials = log_in()
                    if credentials:
                        [bookingOffice_id, login_token] = credentials

                    active_devices = []
                    for device_ip in get_devices():
                        if device_ip[0] and device_ip[0].strip() != "":
                            device = {"ip": "ws://"+device_ip[0] +
                                      ":1234/", "id": device_ip[1], "active": True}
                            active_devices.append(device)
                    # #print(active_devices)
                    Thread(target=server_updater).start()
                    # get_users()

                    socket_guardian()
                # else:
                    # print('Custom Error {}'.format(ips[1]))
        except:
            print("not internet connection")
        time.sleep(0.5)
