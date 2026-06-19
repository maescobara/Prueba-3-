# Prueba 3 de PROGRAMACION Y REDES VIRTUALIZADAS
# Implementación de Automatización de Red con Compliance Auditado

** Maximiliano Andrés Escobar Álvarez | **Código:** 001V-05

---

## 1. Objetivo del Proyecto
En el siguiente repositorio se evidencia la implementación de la automatización completa de un router "Cisco CSR1000v" a la red corporativa de la empresa "Operadora Logistica SA.", con el fin de  aplicar una configuración estándar de la empresa de forma automatizada, para así verificar su correcta aplicación mediante protocolos independientes y generar un certificado de "compliance" que certifique que el equipo está listo para operar.

---

## 2. Alcance
Dentro de las acciones que se realizaron se configuró el hostname corporativo, banner de acceso, servidor NTP, descripción de interfaz WAN y la interfaz Loopback de gestión. Se habilitaron los servicios NETCONF, RESTCONF y HTTP seguro, además quedó fuera del alcance la configuración de protocolos de enrutamiento dinámico y políticas de seguridad avanzadas. Las herramientas que se  utilizaron durante esta prueba fueron pyATS/Genie, Ansible, ncclient (NETCONF) y requests (RESTCONF), todo esto se realizo desde una maquina virtual con el sistema operativo DEVASC.

---

## 3. Herramientas Utilizadas

*|Router: Cisco CSR1000v — IOS-XE 16.9 
*|IP Router: 192.168.56.106 
*|Maquina virtual con DEVASC VM — Ubuntu (labvm)
*|Python (versión 3.8.10)
*|Ansible
*|pyATS/Genie (Última versión)
*|Librería NETCONF (ncclient)
*|Librería RESTCONF (requests)
*|Red  (VirtualBox Host-Only)

---

## 4. Tecnologías Empleadas y Justificación
- pyATS/Genie: Se usó durante la Fase 1 para documentar el estado inicial del router vía SSH, antes de aplicar cualquier cambio. También en la Fase 5 para comparar el estado final con el baseline.
- Ansible: Se utilizo en la Fase 2 ya que permite aplicar la configuración de forma declarativa e idempotente sobre múltiples dispositivos "IOS" sin la necesidad de usar scripting imperativo.
- NETCONF: Se usó en la Fase 3 para validar la configuración aplicada mediante un protocolo independiente de "Ansible", consultando directmente en el árbol XML nativo del dispositivo.
- RESTCONF: Se usó en la Fase 4 como segunda validación independiente, aprovechando su interfaz REST/JSON para poder verificar los endpoints específicos.

---

## 5. Configuración Aplicada

*|Hostname: RTR-OPLOG
*|Banner MOTD: ACCESO RESTRINGIDO - OPLOG
*|Servidor NTP: 1.1.1.1
*|Descripción GigabitEthernet1: Enlace-WAN-Antofagasta
*|Interfaz Loopback: Loopback10 — 10.1.5.1/24
*|NETCONF: Habilitado (puerto 830)
*|RESTCONF: Habilitado (HTTPS)
*||HTTP Seguro: Habilitado

---

## 6. Resultados de Validación
( Criterio           | NETCONF  | RESTCONF )
--------------------------------------------
*|Hostname corporativo | CONFORME | CONFORME |
*|IP Loopback          | CONFORME | CONFORME |
*|Máscara Loopback     | CONFORME | — |
*|Descripción WAN      | CONFORME | CONFORME |
*|Servidor NTP         | CONFORME | CONFORME |
*|Resultado global     | **5/5 CONFORME** | **4/4 CONFORME** |

---

## 7. Conclusiones
Una ver terminada la "configuración", el router "Cisco CSR1000v" fue incorporado exitosamente a la red corporativa de "Operadora Logistica SA." con toda la configuración solicitada, además, las validaciones independientes via NETCONF y RESTCONF confirman que los 5 criterios de compliance fueron cumplidos, incluso el análisis de diferencias con Genie Diff demostran los cambios que fueron realizados entre el estado inicial y el estado final del equipo. con todo eso realizado podemos decir que el dispositivo fue entregado a operaciones en estado CONFORME y listo para producción.
