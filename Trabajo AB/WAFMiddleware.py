
import json
import os
import re
import time
from collections import defaultdict
from flask import request, jsonify


class WAFMiddleware:
    """
    Middleware WAF (Web Application Firewall).

    Se ejecuta antes de que Flask procese una petición
    y analiza si contiene patrones de ataque conocidos.
    """

    # Patrones básicos de SQL Injection
    SQLI_PATTERNS = [
        r"(\bor\b\s+1=1)",
        r"(\band\b\s+1=1)",
        r"(union\s+select)",
        r"(drop\s+table)",
        r"(insert\s+into)",
        r"(delete\s+from)",
        r"(--)",
        r"(/\*)",
        r"(\*/)",
        r"(';)",
        r"(' OR ')",
    ]

    # Patrones básicos de XSS
    XSS_PATTERNS = [
        r"<script.*?>",
        r"</script>",
        r"javascript:",
        r"onerror=",
        r"onload=",
        r"<iframe",
        r"<img",
        r"<svg",
    ]

    # Patrones básicos de Path Traversal
    PATH_TRAVERSAL_PATTERNS = [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e%2f",
        r"%2e%2e\\",
    ]

    def __init__(self, app, requests_per_minute=60):
        """
        Constructor del WAF.

        Parámetros:
            app -> aplicación Flask a proteger
            requests_per_minute -> límite de peticiones por IP
        """

        self.app = app
        self.requests_per_minute = requests_per_minute

        # Diccionario para almacenar timestamps
        # de las peticiones realizadas por cada IP
        self.requests = defaultdict(list)

        # Flask ejecutará inspect_request()
        # antes de procesar cada petición
        app.before_request(self.inspect_request)

    def inspect_request(self):
        """
        Función principal del WAF.

        Se ejecuta antes de cada petición
        y comprueba:
        1. Rate limiting
        2. SQL Injection
        3. XSS
        4. Path Traversal
        """

        # Obtener IP del cliente
        ip = request.remote_addr or "unknown"

        # Verificar límite de peticiones
        if self._rate_limit_exceeded(ip):
            return self.block(
                "Rate limit excedido"
            )

        # Obtener todos los datos de la petición
        data = self._extract_request_data()

        # Buscar patrones SQL Injection
        if self._detect_attack(data, self.SQLI_PATTERNS):
            return self.block(
                "Intento de SQL Injection detectado"
            )

        # Buscar patrones XSS
        if self._detect_attack(data, self.XSS_PATTERNS):
            return self.block(
                "Intento de XSS detectado"
            )

        # Buscar patrones Path Traversal
        if self._detect_attack(data, self.PATH_TRAVERSAL_PATTERNS):
            return self.block(
                "Intento de Path Traversal detectado"

            )

    def _extract_request_data(self):
        """
        Extrae todos los datos relevantes
        de la petición para analizarlos.

        Incluye:
        - Parámetros GET
        - Datos POST
        - JSON
        - Ruta solicitada
        """

        content = []

        # Parámetros GET
        content.extend(request.args.values())

        # Datos enviados por formulario POST
        content.extend(request.form.values())

        # Si la petición contiene JSON
        if request.is_json:
            try:
                body = request.get_json()

                if isinstance(body, dict):
                    content.extend(
                        [str(v) for v in body.values()]
                    )

            except Exception:
                pass

        # Añadimos la ruta solicitada
        content.append(request.path)

        # Convertimos todo a minúsculas
        return " ".join(content).lower()

    def _detect_attack(self, content, patterns):
        """
        Comprueba si alguno de los patrones
        aparece dentro del contenido.

        Devuelve:
            True  -> ataque detectado
            False -> no detectado
        """

        for pattern in patterns:

            # Buscar coincidencias mediante regex
            if re.search(
                pattern,
                content,
                re.IGNORECASE
            ):
                return True

        return False

    def _rate_limit_exceeded(self, ip):
        """
        Control de peticiones por IP.

        Mantiene una lista de timestamps
        y elimina los que tengan más de 60 segundos.
        """

        now = time.time()

        # Conservar únicamente peticiones
        # realizadas durante el último minuto
        self.requests[ip] = [
            t for t in self.requests[ip]
            if now - t < 60
        ]

        # Si supera el límite configurado
        if len(self.requests[ip]) >= self.requests_per_minute:
            return True

        # Registrar petición actual
        self.requests[ip].append(now)

        return False

    def block(self, reason):
        """
        Bloquea la petición.

        Además registra el evento en el log.
        """

        self.log_attack(reason)

        response = jsonify({
            "status": "blocked",
            "reason": reason
        })

        # Código HTTP Forbidden
        response.status_code = 403

        return response

    def log_attack(self, reason):
        """
        Guarda los ataques detectados
        en el fichero waf_log.json.
        """

        entry = {

            # Fecha y hora del incidente
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            # Información de la petición
            "ip": request.remote_addr,
            "path": request.path,
            "method": request.method,

            # Motivo del bloqueo
            "reason": reason
        }

        logfile = "waf_log.json"

        # Si el archivo no existe,
        # se crea con una lista vacía
        if not os.path.exists(logfile):
            with open(logfile, "w") as f:
                json.dump([], f)

        # Leer logs existentes
        try:
            with open(logfile, "r") as f:
                logs = json.load(f)

        except Exception:
            logs = []

        # Añadir nueva entrada
        logs.append(entry)

        # Guardar cambios
        with open(logfile, "w") as f:
            json.dump(
                logs,
                f,
                indent=4
            )