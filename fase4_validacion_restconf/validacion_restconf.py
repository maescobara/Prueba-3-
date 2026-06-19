#!/usr/bin/env python3
import yaml
import socket
import json
import requests
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cargar variables
with open("../vars/vars_001V-05.yaml", "r") as f:
    variables = yaml.safe_load(f)

CODIGO   = variables['codigo']
NOMBRE   = variables['nombre']
HOST     = variables['router']['ip']
USER     = variables['router']['usuario']
PASSWORD = variables['router']['password']
HOSTNAME_ESP  = variables['cliente']['hostname']
LOOPBACK_IP_ESP = variables['router']['loopback_ip']
DESC_WAN_ESP  = variables['router']['descripcion_wan']
NTP_ESP       = variables['router']['ntp_server']
LOOPBACK_ID   = variables['router']['loopback_id']

# Metadatos
print("=" * 60)
print(f"Script  : validacion_restconf.py")
print(f"Alumno  : {NOMBRE} | Codigo: {CODIGO}")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host VM : {socket.gethostname()}")
print("=" * 60)

BASE_URL = f"https://{HOST}/restconf/data"
HEADERS  = {"Accept": "application/yang-data+json"}
AUTH     = (USER, PASSWORD)

def consultar(endpoint, archivo):
    url = f"{BASE_URL}/{endpoint}"
    print(f"\n[GET] {url}")
    resp = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)
    data = resp.json()
    with open(f"evidencias/responses/{archivo}", "w") as f:
        json.dump(data, f, indent=2)
    print(f"[INFO] Guardado en evidencias/responses/{archivo}")
    return data

# 4 consultas independientes
data_hostname  = consultar("Cisco-IOS-XE-native:native/hostname", "get_hostname.json")
data_loopback  = consultar(f"ietf-interfaces:interfaces/interface=Loopback{LOOPBACK_ID}", "get_loopback.json")
data_interface = consultar("ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
data_ntp       = consultar("Cisco-IOS-XE-native:native/ntp", "get_ntp.json")

# Extraer valores
val_hostname = data_hostname.get("Cisco-IOS-XE-native:hostname", "NO ENCONTRADO")

try:
    addrs = data_loopback["ietf-interfaces:interface"]["ietf-ip:ipv4"]["address"]
    val_loopback_ip = addrs[0]["ip"]
except:
    val_loopback_ip = "NO ENCONTRADO"

try:
    val_desc = data_interface["ietf-interfaces:interface"]["description"]
except:
    val_desc = "NO ENCONTRADO"

try:
    val_ntp = data_ntp["Cisco-IOS-XE-native:ntp"]["Cisco-IOS-XE-ntp:server"]["server-list"][0]["ip-address"]
except:
    val_ntp = "NO ENCONTRADO"

# Reporte
score = 0
print("\n=== REPORTE DE VALIDACION RESTCONF ===")

def verificar(criterio, esperado, obtenido):
    global score
    if str(esperado).strip() == str(obtenido).strip():
        print(f"[OK]   {criterio}: {obtenido}")
        score += 1
    else:
        print(f"[FAIL] {criterio}: Esperado={esperado} | Obtenido={obtenido}")

verificar("Hostname corporativo", HOSTNAME_ESP,     val_hostname)
verificar("IP Loopback",          LOOPBACK_IP_ESP,  val_loopback_ip)
verificar("Descripcion WAN",      DESC_WAN_ESP,     val_desc)
verificar("Servidor NTP",         NTP_ESP,          val_ntp)

print("=" * 60)
if score == 4:
    print(f"RESULTADO FINAL: {score}/4 OK - CONFORME")
else:
    print(f"RESULTADO FINAL: {score}/4 OK - NO CONFORME")
print("=" * 60)
