# Ejercicio 3: Laboratorio de Ciberseguridad

## ADVERTENCIA

**ESTA APLICACION ES INTENCIONALMENTE VULNERABLE.**
**NO DESPLEGAR EN PRODUCCION NI EN REDES PUBLICAS.**
**Solo para uso educativo en entornos locales controlados.**

---

## Descripcion

Este ejercicio simula un escenario real de auditoria de seguridad. Se te proporciona una aplicacion web funcional (TechStore) que contiene multiples vulnerabilidades de seguridad. Tu objetivo es identificarlas, explotarlas de forma controlada, documentarlas y corregirlas.

## Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Como ejecutar la aplicacion

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicacion
python run.py
```

La aplicacion estara disponible en: `http://127.0.0.1:5000`

## Que debes entregar

Lee las instrucciones completas en `INSTRUCCIONES.md`. En resumen:

1. **Scripts de deteccion** - Identificar vulnerabilidades automaticamente
2. **Scripts de explotacion** - Demostrar el impacto de cada vulnerabilidad
3. **Aplicacion parcheada** - Corregir todas las vulnerabilidades
4. **Reporte de seguridad** - Documentar hallazgos usando `plantilla_reporte.md`

## Estructura de entrega esperada

```
entrega/
    scripts/
        deteccion/
            detectar_vuln_1.py
            detectar_vuln_2.py
            ...
        explotacion/
            explotar_vuln_1.py
            explotar_vuln_2.py
            ...
    patched_app/
        (copia corregida de vulnerable_app/)
    reporte.md
```

## Pista

Investiga **OWASP Top 10** - la referencia estandar de la industria para las vulnerabilidades web mas criticas. Presta atencion a como interactua la aplicacion con:

- La base de datos
- Los datos del usuario
- El sistema de archivos
- La autenticacion

## Criterios de evaluacion

Consulta `CRITERIOS.md` para ver la rubrica detallada.

## Recursos recomendados

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- Documentacion de Flask: https://flask.palletsprojects.com/
- Documentacion de la biblioteca `requests`: https://docs.python-requests.org/
