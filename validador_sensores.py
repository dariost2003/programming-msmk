lecturas = [45.2, -3.1, 102.5, 0, 78.4, -1.0, 55.0, 99.9, 33.1]

print(" Análisis de la lista de lecturas")

for lectura in lecturas:
    if 0 <= lectura <= 100:
        print(f"Lectura {lectura}: válida")
    else:
        print(f"Lectura {lectura}: anomalía")

while True:
    
    entrada = input("Introduce una lectura: ")
    
    if entrada.lower() == "salir":
    
    try:
        lectura_manual = float(entrada)
        
        if 0 <= lectura_manual <= 100:
            print(f"Lectura {lectura_manual}: válida")
        else:
            print(f"Lectura {lectura_manual}: anomalía")
            total_anomalias = total_anomalias + 1 
            
    except ValueError:
        print("Por favor, introduce un número válido o escribe 'salir'.")

print("\n--- Resumen final ---")
print(f"Cantidad total de anomalías registradas a mano: {total_anomalias}")

