#Generamos un archivo .py que es ejecutado una unica vez, al iniciar la app, o posteriormente si lo aztualizamos;
#este codigo genera un archivo .json, que será usado como un diccionario comprimido para buscar de forma rapida y 
#eficiente cuando el usuario quiera usar filtros.

import json
import requests
import time
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent / 'datos_basicos_filtro.json'

def fetch_with_retry(session, url, name, max_retries=3):
    for attempt in range(max_retries):

        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == max_retries -1:
                print(f'[ERROR FINAL] {name}: {e}')
                return None
    return None


def dataset_pokemon():
       
    url_base = 'https://pokeapi.co/api/v2/pokemon?limit=1025'
    minibiblioteca = []

    session = requests.Session()

    print('Generando indice primordial Pokemon... tardará unos minutos')

    try:
        response = session.get(url_base, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Ha ocurrido un Error al conectar con la API: {e}')
        return
    
    for i, entry in enumerate(data['results'], 1):

        pokemon_data = fetch_with_retry(
            session,
            entry['url'],
            entry['name']
        )

        if not pokemon_data:
            continue

        mini_datos = {
            'id': pokemon_data['id'],
            'name': pokemon_data['name'],
            'types': [t['type']['name'] for t in pokemon_data['types']],
            'hp': pokemon_data['stats'][0]['base_stat'],
            'attack': pokemon_data['stats'][1]['base_stat'],
            'defense': pokemon_data['stats'][2]['base_stat'],
            'speed': pokemon_data['stats'][5]['base_stat'],
            'base_exp': pokemon_data.get('base_experience', 0),
            'sprite': pokemon_data['sprites']['other']['official-artwork']['front_default']
        }
        
        minibiblioteca.append(mini_datos)
      
        if i % 50 == 0:
            print(f'Cargados {i} Pokemon...')

    
    try:
        with open(OUTPUT_FILE, 'w', encoding= 'utf-8') as f:
            json.dump(minibiblioteca, f, indent=4, ensure_ascii=False)

        print('\n¡Archivo generado correctamente en: {OUTPUT_FILE}!')
        
    except Exception as e:
        print(f'Error al escribir el archivo: {e}')
    
    

if __name__ == '__main__':
    dataset_pokemon()


def load_dataset():

    try:
        with open('datos_basicos_filtro.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    except FileNotFoundError:
        return[]