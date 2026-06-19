#!/usr/bin/env python3
import yaml
import socket
import xml.etree.ElementTree as ET
from datetime import datetime
from ncclient import manager

with open("../vars/vars_001V-05.yaml", "r") as f:
    variables = yaml.safe_load(f)

CODIGO   = variables['codigo']
NOMBRE   = variables['nombre']
HOST     = variables['router']['ip']
USER     = variables['router']['usuario']
PASSWORD = variables['router']['password']
HOSTNAME_ESPERADO  = variables['cliente']['hostname']
LOOPBACK_IP_ESP    = variables['router']['loopback_ip']
LOOPBACK_MASK_ESP  = variables['router']['loopback_mask']
DESC_WAN_ESP       = variables['router']['descripcion_wan']
NTP_ESP            = variables['router']['ntp_server']
LOOPBACK_ID        = variables['router']['loopback_id']

print("=" * 60)
print(f"Script  : validacion_netconf.py")
print(f"Alumno  : {NOMBRE} | Codigo: {CODIGO}")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host VM : {socket.gethostname()}")
print("=" * 60)
print(f"\nConectando via NETCONF a {HOST} puerto 830...")
print(f"[INFO] Modelo utilizado: Cisco-IOS-XE-native")

try:
    with manager.connect(
        host=HOST,
        port=830,
        username=USER,
        password=PASSWORD,
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
        device_params={'name': 'iosxe'}
    ) as m:
        # Sin filtro para garantizar >5KB — modelo Cisco-IOS-XE-native
        rpc_reply = m.get_config(source='running')
        xml_data = rpc_reply.xml

        with open("evidencias/rpc_reply_raw.xml", "w") as f:
            f.write(xml_data)
        print("[INFO] evidencias/rpc_reply_raw.xml guardado exitosamente.")

except Exception as e:
    print(f"[ERROR] Conexión fallida: {e}")
    exit(1)

root = ET.fromstring(xml_data)
ns = {
    'nc':     'urn:ietf:params:xml:ns:netconf:base:1.0',
    'ios':    'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
    'ios-ntp':'http://cisco.com/ns/yang/Cisco-IOS-XE-ntp'
}

score = 0
print("\n=== REPORTE DE VALIDACION NETCONF ===")

node = root.find('.//ios:hostname', ns)
val  = node.text if node is not None else "NO ENCONTRADO"
if val == HOSTNAME_ESPERADO:
    print(f"[OK]   1/5 Hostname          : {val}")
    score += 1
else:
    print(f"[FAIL] 1/5 Hostname          : Esperado={HOSTNAME_ESPERADO} | Obtenido={val}")

node = root.find(f'.//ios:interface/ios:Loopback[ios:name="{LOOPBACK_ID}"]/ios:ip/ios:address/ios:primary/ios:address', ns)
val  = node.text if node is not None else "NO ENCONTRADO"
if val == LOOPBACK_IP_ESP:
    print(f"[OK]   2/5 IP Loopback       : {val}")
    score += 1
else:
    print(f"[FAIL] 2/5 IP Loopback       : Esperado={LOOPBACK_IP_ESP} | Obtenido={val}")

node = root.find(f'.//ios:interface/ios:Loopback[ios:name="{LOOPBACK_ID}"]/ios:ip/ios:address/ios:primary/ios:mask', ns)
val  = node.text if node is not None else "NO ENCONTRADO"
if val == LOOPBACK_MASK_ESP:
    print(f"[OK]   3/5 Mascara Loopback  : {val}")
    score += 1
else:
    print(f"[FAIL] 3/5 Mascara Loopback  : Esperado={LOOPBACK_MASK_ESP} | Obtenido={val}")

node = root.find('.//ios:interface/ios:GigabitEthernet[ios:name="1"]/ios:description', ns)
val  = node.text if node is not None else "NO ENCONTRADO"
if val == DESC_WAN_ESP:
    print(f"[OK]   4/5 Descripcion WAN   : {val}")
    score += 1
else:
    print(f"[FAIL] 4/5 Descripcion WAN   : Esperado={DESC_WAN_ESP} | Obtenido={val}")

node = root.find('.//ios:ntp/ios:server/ios:server-list/ios:ip-address', ns)
if node is None:
    node = root.find('.//ios-ntp:server/ios-ntp:server-list/ios-ntp:ip-address', ns)
val = node.text if node is not None else "NO ENCONTRADO"
if val == NTP_ESP:
    print(f"[OK]   5/5 Servidor NTP      : {val}")
    score += 1
else:
    print(f"[FAIL] 5/5 Servidor NTP      : Esperado={NTP_ESP} | Obtenido={val}")

print("=" * 60)
if score == 5:
    print(f"RESULTADO FINAL: {score}/5 OK - CONFORME")
else:
    print(f"RESULTADO FINAL: {score}/5 OK - NO CONFORME")
print("=" * 60)
