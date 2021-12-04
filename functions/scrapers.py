import requests
from bs4 import BeautifulSoup
import pandas as pd


def create_gen_1to7_list(page = requests.get("https://serebii.net/pokedex-sm/")):
    pokemon_list = pd.DataFrame(columns = ['link', 'number', 'name'])

    soup = BeautifulSoup(page.content, 'html.parser')
    for index in range(0, 7):
        temp_list = pd.DataFrame(columns = ['link', 'number', 'name'])
        pokemon_raw_list = soup.find_all('table')[1]
        pokemon_raw_list = pokemon_raw_list.find_all('td')[index]
        pokemon_raw_list = pokemon_raw_list.find_all('option')

        temp_list['link'] = [item.get('value') for item
                             in pokemon_raw_list]

        temp_list['number'] = [item.get_text().split(' ')[0] for item
                               in pokemon_raw_list]

        temp_list['name'] = [item.get_text().split(' ', 1)[1].strip(" ") for item
                             in pokemon_raw_list]

        pokemon_list = pd.concat([pokemon_list, temp_list], axis = 0)

    pokemon_list.set_index('number', inplace = True)
    pokemon_list = pokemon_list[pokemon_list['link'] != "#"]
    
    return pokemon_list


def create_gen_8_list(page = requests.get("https://serebii.net/pokedex-swsh/")):
    pokemon_list = pd.DataFrame(columns = ['link', 'number', 'name'])

    soup = BeautifulSoup(page.content, 'html.parser')
    pokemon_raw_list = soup.find_all('table')[1]
    pokemon_raw_list = pokemon_raw_list.find_all('td')[7]
    pokemon_raw_list = pokemon_raw_list.find_all('option')

    pokemon_list['link'] = [item.get('value') for item
                            in pokemon_raw_list]

    pokemon_list['number'] = [item.get_text().split(' ')[0] for item
                              in pokemon_raw_list]

    pokemon_list['name'] = [item.get_text().split(' ', 1)[1].strip(" ") for item
                            in pokemon_raw_list]

    pokemon_list.set_index('number', inplace = True)
    pokemon_list = pokemon_list[pokemon_list['link'] != "#"]

    return pokemon_list


def scrape_pokesoup(pokelink):
    page = requests.get("https://serebii.net/" + pokelink)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup