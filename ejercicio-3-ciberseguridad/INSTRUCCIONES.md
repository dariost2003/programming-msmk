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

### 3. Aplicacion parcheada (`patched_app/`)
Una copia de la aplicacion con **todas** las vulnerabilidades corregidas. Cada correccion debe:
- Eliminar la vulnerabilidad sin romper la funcionalidad
- Seguir buenas practicas de seguridad
- Incluir comentarios explicando por que se hizo el cambio

### 4. Reporte de seguridad (`reporte.md`)
Un reporte profesional documentando todo el proceso. Usa la plantilla proporcionada en `plantilla_reporte.md`.

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
