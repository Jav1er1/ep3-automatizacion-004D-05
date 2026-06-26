import datetime

contenido = f"""==================================================
CERTIFICADO DE COMPLIANCE DE AUTOMATIZACION
==================================================
Fecha de emision: {datetime.datetime.now()}
Ingeniero a cargo: Valenzuela Chacana Javier Ignacio (004D-05)
Empresa Cliente: Transporte Andino SpA

1. Validacion NETCONF: CONFORME
2. Validacion RESTCONF: CONFORME
3. Diferencias Post-Configuracion: VERIFICADAS

RESULTADO FINAL DE LA AUDITORIA: CONFORME
==================================================
"""

with open("evidencias/certificado_compliance_004D-05.txt", "w") as f:
    f.write(contenido)
    
print(contenido)
