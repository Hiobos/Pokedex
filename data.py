import requests


API_URL = 'https://pokeapi.co/api/v2/pokemon/'
param = {
    'offset': 0,
    'limit': 151
}

class GetData:
    def __init__(self):
        self.pokemon_list = []
        self.pokemon_sprite_list = []

    def fetch_data(self):
        response = requests.get(API_URL, params=param)
        response = response.json()
        list_of_pokemon = response['results']
        list_test = list(list_of_pokemon)
        for i in range(0, len(list_test)):
            self.pokemon_list.append(list_test[i]['name'])
            self.pokemon_sprite_list.append(list_test[i]['url'])

        print(self.pokemon_list)
        return self.pokemon_list, self.pokemon_sprite_list


