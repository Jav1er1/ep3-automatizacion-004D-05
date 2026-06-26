import requests
import json
import yaml
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('../vars/vars_004D-05.yaml', 'r') as file:
    v = yaml.safe_load(file)

base_url = f"https://{v['router']['ip']}/restconf/data"
auth = (v['router']['usuario'], v['router']['password'])
headers = {"Accept": "application/yang-data+json"}

endpoints = {
    "hostname": f"{base_url}/Cisco-IOS-XE-native:native/hostname",
    "loopback": f"{base_url}/ietf-interfaces:interfaces/interface=Loopback10",
    "wan": f"{base_url}/ietf-interfaces:interfaces/interface=GigabitEthernet1",
    "ntp": f"{base_url}/Cisco-IOS-XE-native:native/ntp"
}

ok_count = 0
print("--- INICIANDO VALIDACION RESTCONF ---")

r1 = requests.get(endpoints["hostname"], auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_hostname.json", "w") as f:
    f.write(r1.text)
if v['router']['hostname'] in r1.text:
    print("[OK] Hostname validado.")
    ok_count += 1
else:
    print("[FAIL] Hostname.")

r2 = requests.get(endpoints["loopback"], auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_loopback.json", "w") as f:
    f.write(r2.text)
if v['router']['loopback_ip'] in r2.text:
    print("[OK] IP Loopback validada.")
    ok_count += 1
else:
    print("[FAIL] IP Loopback.")

r3 = requests.get(endpoints["wan"], auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_interfaces.json", "w") as f:
    f.write(r3.text)
if v['router']['descripcion_wan'] in r3.text:
    print("[OK] Descripcion WAN validada.")
    ok_count += 1
else:
    print("[FAIL] Descripcion WAN.")

r4 = requests.get(endpoints["ntp"], auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_ntp.json", "w") as f:
    f.write(r4.text)
if v['router']['ntp_server'] in r4.text:
    print("[OK] Servidor NTP validado.")
    ok_count += 1
else:
    print("[FAIL] Servidor NTP.")

print("\n==============================")
if ok_count == 4:
    print(f"RESULTADO: {ok_count}/4 CONFORME")
else:
    print(f"RESULTADO: {ok_count}/4 NO CONFORME")
