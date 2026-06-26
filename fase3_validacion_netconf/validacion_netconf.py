import yaml
from ncclient import manager
import xml.dom.minidom
import datetime
import socket

print(f"=== SCRIPT: validacion_netconf.py ===")
print(f"Fecha/Hora: {datetime.datetime.now()}")
print(f"Host VM: {socket.gethostname()}")
print("=====================================\n")

with open('../vars/vars_004D-05.yaml', 'r') as file:
    vars_data = yaml.safe_load(file)

router_ip = vars_data['router']['ip']
user = vars_data['router']['usuario']
password = vars_data['router']['password']

netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
"""

try:
    with manager.connect(host=router_ip, port=830, username=user, password=password, hostkey_verify=False, look_for_keys=False, allow_agent=False) as m:
        rpc_reply = m.get_config(source='running', filter=netconf_filter)
        xml_data = rpc_reply.xml
        
        with open("evidencias/rpc_reply_raw.xml", "w") as xml_file:
            xml_file.write(xml.dom.minidom.parseString(xml_data).toprettyxml())
            
        print("XML guardado en evidencias/rpc_reply_raw.xml")
        print("\n--- INICIANDO VALIDACION ---")
        
        ok_count = 0
        
        if vars_data['router']['hostname'] in xml_data:
            print("[OK] Hostname coincide.")
            ok_count += 1
        else:
            print("[FAIL] Hostname no coincide.")
            
        if vars_data['router']['loopback_ip'] in xml_data:
            print("[OK] IP Loopback coincide.")
            ok_count += 1
        else:
            print("[FAIL] IP Loopback no coincide.")
            
        if vars_data['router']['loopback_mask'] in xml_data:
            print("[OK] Mascara Loopback coincide.")
            ok_count += 1
        else:
            print("[FAIL] Mascara Loopback no coincide.")
            
        if vars_data['router']['descripcion_wan'] in xml_data:
            print("[OK] Descripcion WAN coincide.")
            ok_count += 1
        else:
            print("[FAIL] Descripcion WAN no coincide.")
            
        if vars_data['router']['ntp_server'] in xml_data:
            print("[OK] Servidor NTP coincide.")
            ok_count += 1
        else:
            print("[FAIL] Servidor NTP no coincide.")
            
        print("\n==============================")
        if ok_count == 5:
            print(f"RESULTADO: {ok_count}/5 CONFORME")
        else:
            print(f"RESULTADO: {ok_count}/5 NO CONFORME")

except Exception as e:
    print(f"Error conectando por NETCONF: {e}")

