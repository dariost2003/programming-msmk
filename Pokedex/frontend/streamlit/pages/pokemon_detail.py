from api.backend_client import BackendClient

client = BackendClient()

def render_pokemon_detail(identifier):

    pokemon = client.get_pokemon(identifier)

    evolution = client.get_evolution(identifier)