# 🛡️ Technical Whitepaper: Advanced Network Infrastructure Automation
**Proyecto:** Ep3 - Automatización de Infraestructura de Red para Transporte Andino SpA  
**Autor:** Javier Ignacio Valenzuela Chacana (004D-05)  
**Entorno:** Cisco IOS-XE CSR1kv / Python 3.8 / Linux environment  

---

## 📖 1. Resumen Ejecutivo
Este repositorio constituye el entregable técnico final de la asignatura de Automatización de Redes. El proyecto implementa una arquitectura **NetDevOps** completa, pivotando desde procesos manuales hacia un paradigma de **Infraestructura como Código (IaC)**. Se garantiza la integridad operativa mediante auditorías de estado (State-based validation) y la ejecución de pipelines de automatización bajo control de versiones Git.

## 2. Especificaciones Técnicas y Stack de Automatización
El entorno fue diseñado bajo estándares de alta disponibilidad y seguridad programable:

* **Orquestación:** Ansible (Playbooks para configuración, `ios_config` y `ios_command` para tareas de bajo nivel).
* **Validación de Estado:** pyATS/Genie (Librerías de Cisco para parsing de estados operativos y detección de derivas de configuración).
* **APIs Programables:** 
    * `NETCONF`: Protocolo base XML sobre SSH.
    * `RESTCONF`: Interfaz RESTful basada en modelos YANG.
* **Trazabilidad:** Sistema de control de versiones Git con estrategias de branching para el ciclo de vida del código.

## 3. Análisis Técnico por Fases

### Fase 1: Ingeniería de Línea Base (Golden State)
La fase inicial se centró en la creación de un "Snapshot" del estado de la red. Utilizando la librería Genie, se extrajeron modelos operativos de `interface`, `platform` y `routing`. 
* **Importancia:** Permite establecer una referencia para cualquier proceso de *Compliance Audit* futuro.

### Fase 2: Automatización y Despliegue de Configuración
Se implementaron tácticas de aprovisionamiento declarativo. La idempotencia se logró mediante el manejo de archivos `host_vars` y plantillas YAML.
* **Componentes:** Configuración de interfaces Loopback, estandarización de nombres de host y aseguramiento de acceso vía banners y permisos de modo privilegiado.

### Fase 3 & 4: Interfaces Programables
Se abandonó el parsing de texto plano para adoptar el paradigma de **Redes Basadas en Datos**.
* **NETCONF:** Implementación de flujos RPC (Remote Procedure Call) para la consulta de bases de datos de configuración (running vs candidate).
* **RESTCONF:** Consumo de recursos mediante verbos HTTP (GET/POST), permitiendo la integración de la infraestructura con sistemas de terceros.

### Fase 5: Auditoría de Compliance (Continuous Verification)
La etapa final ejecuta un proceso de comparación diferencial (`Diff`). Se calculó la desviación técnica entre el snapshot de la fase 1 y el estado actual, generando automáticamente un certificado de cumplimiento (`certificado_compliance_004D-05.txt`).

---

## 4. Matriz de Resolución de Conflictos (Troubleshooting)

| Error Técnico | Causa Raíz | Acción Correctiva |
| :--- | :--- | :--- |
| **Connection Timeout** | Líneas VTY saturadas/fantasmas | Reinicio de control de proceso CSR1kv y purga de sesiones SSH. |
| **Parser Mismatch** | Banner de acceso malformado | Eliminación vía `ios_config` para normalizar el prompt. |
| **Genie Diff Failure** | Conflicto de Hostname | Estandarización de `hostname` en la capa de aprovisionamiento. |
| **Privilege Escalation** | Falta de `enable` secret | Inyección de credenciales explícitas en testbed.yaml. |

---

## 5. Guía de Despliegue Automatizado
Para ejecutar el ciclo completo de validación, siga estas instrucciones en su terminal:

1. **Setup:** `source venv/bin/activate`
2. **Sync:** `./sincronizar_todo.sh` (Script personalizado para manejo de evidencias).
3. **Audit:** `ansible-playbook site.yml --check` (Modo verificación).
4. **Report:** `python3 fase5_reporte/generar_certificado.py`.

---

## 6. Estructura de Repositorio (Source of Truth)
```bash
/ep3-automatizacion-004D-05
├── fase1_baseline/          # Referencias de estado (Golden Configs)
├── fase2_aprovisionamiento/ # Orquestación (Playbooks)
├── fase3_validacion_netconf/# Operaciones RPC vía NETCONF
├── fase4_validacion_restconf/# Datos estructurados JSON (REST)
└── fase5_reporte/           # Logs, auditorías y certificaciones

