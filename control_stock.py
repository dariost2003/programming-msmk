
#             SISTEMA DE CONTROL DE STOCK - MERCADONA

historial = []
MINIMO_STOCK = 10


def validar_entrada(texto):
    try:
        
        unidades = int(texto)
        return unidades
    except ValueError:

        print(f" ERROR: '{texto}' no es una cantidad válida.")
        return None


def stock_bajo(unidades, minimo=10):
    if unidades < minimo:
        return True
    else:
        return False

def registrar_producto(historial_lista, nombre, unidades):

    if stock_bajo(unidades, MINIMO_STOCK):
        estado_producto = "Stock bajo"
    else:
        estado_producto = "Normal"
        
    nueva_ficha = {
        "producto": nombre,
        "unidades": unidades,
        "estado": estado_producto
    }
    

    historial_lista.append(nueva_ficha)


def mostrar_resumen(historial_lista):
    print("\n")
    print("  INFORME FINAL DE STOCK (MERCADONA)       ")
    
    if len(historial_lista) == 0:
        print("No se registraron productos en este turno.")
        return
        
    contador_bajo_stock = 0
    
    for ficha in historial_lista:
        print(f" Producto: {ficha['producto']:18} | Cantidad: {ficha['unidades']:3} | Estado: {ficha['estado']}")
        
        if ficha['estado'] == "Stock bajo":
            contador_bajo_stock += 1
            
    total_productos = len(historial_lista)
    
    print(f" Alerta: {contador_bajo_stock} de {total_productos} productos necesitan reposición urgente.")


print(" [SIMULACIÓN] INICIO DE REVISIÓN DE STOCK EN MERCADONA")

datos_simulados = [
    {"nombre": "Leche ", "unidades": "15"},
    {"nombre": "Espaguetis",       "unidades": "4"},
    {"nombre": "Tomate ",    "unidades": "muchos"},
    {"nombre": "Pizza ",   "unidades": "8"}
]

for entrada in datos_simulados:
    nombre = entrada["nombre"]
    unidades_texto = entrada["unidades"]
    
    print(f"\n[Empleado introduce]: Producto -> '{nombre}' con cantidad -> '{unidades_texto}'")
    

    unidades_validadas = validar_entrada(unidades_texto)
    
    if unidades_validadas is None:
        print(f"   El sistema rechaza el registro de '{nombre}'.")
        continue
        
    registrar_producto(historial, nombre, unidades_validadas)
    print(f"   ÉXITO: '{nombre}' guardado en el sistema.")
    
    if stock_bajo(unidades_validadas, MINIMO_STOCK):
        print(f"   ALERTA INMEDIATA: ¡Quedan pocas unidades de '{nombre}'! Reponer pronto.")

mostrar_resumen(historial)
