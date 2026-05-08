#Generamos un archivo .py que es ejecutado una unica vez, al iniciar la app, o posteriormente si lo aztualizamos;
#este codigo genera un archivo .json, que será usado como un diccionario comprimido para buscar de forma rapida y 
#eficiente cuando el usuario quiera usar filtros.

import json
import requests
import time

def minibiblioteca_pokemon():
       
    url_base = 'https://pokeapi.co/api/v2/pokemon?limit=1025'
    minibiblioteca = []
    session = requests.Session()

    print('Generando indice primordial Pokemon... tardará unos minutos')

    try:
        response = session.get(url_base, timeout=10)
        response.raise_for_status()
        respuesta = response.json()
    except Exception as e:
        print(f'Ha ocurrido un Error al conectar con la API: {e}')
        return
    
    for i, entry in enumerate(respuesta['results'], 1):
        intentos = 3
        while intentos >0:
            try:
                respuesta_individual = session.get(entry['url'], timeout=10)
                respuesta_individual.raise_for_status()
                datos_individuales = respuesta_individual.json()

                mini_datos = {
                    'id': datos_individuales['id'],
                    'name': datos_individuales['name'],
                    'types': [t['type']['name'] for t in datos_individuales['types']],
                    'hp': datos_individuales['stats'][0]['base_stat'],
                    'atk': datos_individuales['stats'][1]['base_stat'],
                    'def': datos_individuales['stats'][2]['base_stat'],
                    'speed': datos_individuales['stats'][5]['base_stat'],
                    'base_exp': datos_individuales['base_experience'],
                    'sprite': datos_individuales['sprites']['other']['official-artwork']['front_default']
                }
                minibiblioteca.append(mini_datos)
                break
            except Exception as e:
                intentos -= 1
                print(f'Error con {entry["name"]}, reintentando... ({3-intentos}/3)')
                time.sleep(1)
        if i % 50 == 0:
            print(f'Cargados {i} Pokemon...')

    
    try:
        with open('datos_basicos_filtro.json', 'w', encoding= 'utf-8') as f:
            json.dump(minibiblioteca, f, indent=4, ensure_ascii=False)
        print('\n¡Archivo datos_basicos_filtro.json generado!')
    except Exception as e:
        print(f'Error al escribir el archivo: {e}')
    
    

if __name__ == '__main__':
    minibiblioteca_pokemon()