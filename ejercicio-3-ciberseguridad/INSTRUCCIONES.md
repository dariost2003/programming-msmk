# Mision: Auditoria de Seguridad - TechStore

## Briefing

Eres un auditor de seguridad contratado por la empresa **TechStore** para analizar su aplicacion web de comercio electronico. La empresa sospecha que su aplicacion podria tener vulnerabilidades criticas, pero no sabe cuales ni cuantas son.

Tu trabajo consiste en realizar una auditoria completa de seguridad sobre la aplicacion.

---

## Contexto

TechStore es una tienda en linea que vende productos tecnologicos. La aplicacion permite:

- Buscar productos en el catalogo
- Dejar comentarios y opiniones
- Iniciar sesion como usuario o administrador
- Descargar archivos (manuales, catalogos)
- Acceder a un panel de administracion

La aplicacion fue desarrollada rapidamente por un equipo sin experiencia en seguridad. Tu mision es encontrar **todas** las vulnerabilidades antes de que un atacante real las explote.

---

## Lo que debes entregar

### 1. Scripts de deteccion (`scripts/deteccion/`)
Scripts en Python que automaticen la **identificacion** de cada vulnerabilidad encontrada. Cada script debe:
- Probar la existencia de la vulnerabilidad
- Mostrar evidencia clara (respuesta del servidor, datos obtenidos, etc.)
- NO causar dano permanente a la aplicacion

### 2. Scripts de explotacion (`scripts/explotacion/`)
Scripts en Python que demuestren la **explotacion** controlada de cada vulnerabilidad. Cada script debe:
- Explotar la vulnerabilidad de forma controlada
- Mostrar el impacto potencial
- Incluir comentarios explicando cada paso

### 3. Escaner de vulnerabilidades (`scanner/`)
Una herramienta CLI reutilizable que reciba la URL base de cualquier aplicacion web y ejecute automaticamente todas las pruebas de seguridad que hayas desarrollado. El escaner debe:
- Aceptar una URL base como argumento: `python scanner.py http://127.0.0.1:5000`
- Ejecutar todos los tests de deteccion en secuencia
- Mostrar un resumen con codigo de colores en terminal (rojo=critico, amarillo=medio, verde=sin hallazgo)
- Generar un reporte automatico en formato Markdown con los resultados
- Ser extensible: cada test debe ser una funcion o clase independiente, de modo que anadir un nuevo test sea sencillo
- Manejar errores de conexion y timeouts de forma elegante

### 4. WAF (Web Application Firewall) basico (`waf/`)
Un middleware Flask que actue como capa de proteccion frente a ataques comunes. Debe:
- Funcionar como un middleware que se inserta en la aplicacion parcheada
- Detectar y bloquear intentos de SQL Injection (patrones comunes en parametros)
- Detectar y bloquear intentos de XSS (etiquetas HTML/script en inputs)
- Detectar y bloquear intentos de Path Traversal (secuencias `../` en rutas)
- Implementar rate limiting basico (limitar peticiones por IP por minuto)
- Registrar todos los intentos bloqueados en un archivo de log (`waf_log.json`)
- Devolver una respuesta HTTP 403 con mensaje descriptivo cuando bloquee un ataque
- Incluir al menos 5 tests unitarios que demuestren que el WAF bloquea ataques reales

### 5. Aplicacion parcheada (`patched_app/`)
Una copia de la aplicacion con **todas** las vulnerabilidades corregidas y el WAF integrado. Cada correccion debe:
- Eliminar la vulnerabilidad sin romper la funcionalidad
- Seguir buenas practicas de seguridad
- Incluir comentarios explicando por que se hizo el cambio
- Tener el WAF activado como capa de defensa adicional

### 6. Reporte de seguridad (`reporte.md`)
Un reporte profesional documentando todo el proceso. Usa la plantilla proporcionada en `plantilla_reporte.md`.

### BONUS: Dashboard de monitoreo de seguridad (`dashboard/`)
**(Opcional, puntos extra)** Un panel web que muestre en tiempo real los intentos de ataque detectados por el WAF. Puede usar Streamlit, Flask con templates, o cualquier otra libreria. Deberia mostrar:
- Log de ataques bloqueados en tiempo real
- Graficas de ataques por tipo y por IP
- Estadisticas generales (total bloqueados, tipo mas frecuente, IPs mas activas)

---

## Reglas de engagement

1. **Solo atacar la aplicacion local** - nunca dirigir ataques a sistemas externos
2. **Documentar todo** - cada paso, cada hallazgo, cada evidencia
3. **No destruir datos** - las pruebas deben ser no destructivas cuando sea posible
4. **Usar Python** para todos los scripts de deteccion y explotacion
5. **La biblioteca `requests`** esta disponible para hacer peticiones HTTP

---

## Como empezar

1. Instala las dependencias: `pip install -r requirements.txt`
2. Ejecuta la aplicacion: `python run.py`
3. Abre tu navegador en `http://127.0.0.1:5000`
4. Explora la aplicacion como lo haria un usuario normal
5. Luego, piensa como un atacante...

---

## Pista

Investiga el **OWASP Top 10**. Es el recurso mas importante para cualquier auditor de seguridad web.

Buena suerte, auditor.
