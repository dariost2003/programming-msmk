temperaturas = [72.1, 85.4, 91.0, 103.2, 78.5, 110.8, 88.3, 95.1, 67.4, 104.5]

def es_critica(temp):

    if temp < 60 or temp > 100:
        return True
    else:
        return False
    
    def encontrar_criticas(lista_temps):
    lista_filtrada = [] 
    
    for t in lista_temps:
        if es_critica(t):
            lista_filtrada.append(t) 
            
    return

def resumen(lista_temps):
    total_lecturas = len(lista_temps) #
    
    criticas = len(encontrar_criticas(lista_temps))
    
    normales = total_lecturas - criticas
    
    print("RESUMEN DEL DÍA")
    print(f"Total de lecturas: {total_lecturas}")
    print(f"Temperaturas críticas encontradas: {criticas}")
    print(f"Temperaturas normales encontradas: {normales}")


print(f"Lista de temperaturas críticas: {lista_de_fallos}")

resumen(temperaturas)
