import time
import random
import os
import sys
import argparse

import importlib
from bs4 import BeautifulSoup
import pandas as pd


try:
    sys.path.append("functions")
    import scrapers as scrp
    import crawler as crwl
except ModuleNotFoundError:
    print("Could not find the necessary functions inside their folder...")
    sys.exit()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", 
                        help = "create a new pokedex and fill it", 
                        action = "store_true")
    parser.add_argument("-f", "--fill", 
                        help = "fill the existing pokedex", 
                        action = "store_true")
    parser.add_argument("-l", "--lookup",
                        help = "look up an entry in the local pokedex",
                        type = int,
                        action = "store",
                        required = False,
                        metavar = "pokemon_number",
                        dest = "number")

    args = parser.parse_args()

    args_given = sum(bool(e) for e in vars(args).values())

    if args_given == 0:
        print("No action requested, check --help to see the available ones...")
        exit()
    elif args_given > 1:
        print("The code can only perform one action at a time.")
        exit()
    else:
        return args


def create_pokedex():
    pokelist = scrp.get_pokelist()
    os.makedirs("data", exist_ok = True)
    crwl.pokecrawler(pokelist, fill = False, verbose = True)


def fill_pokedex():
    pokelist = scrp.get_pokelist()
    try:
        current_pokedex = pd.read_csv("data/pokedex.csv", 
                                    usecols = ["number", "name"],
                                    dtype = {"number": str})
        current_pokedex.set_index("number", inplace = True)

        pokelist = pokelist.loc[[(number not in current_pokedex.index) for number in pokelist.index]]
        if len(pokelist) == 0:
            print("Looks like your pokedex is already complete, well done!")
        else:
            crwl.pokecrawler(pokelist, fill = True, verbose = True)
    except FileNotFoundError:
        print("No pokedex available to fill, try creating one by using the -c option")


def check_pokedex(number):
    if number > 0:
        try:
            print("Checking your pokedex for pokemon number " + f"{args.number:03d}" + "...")
            columns = pd.read_csv("data/pokedex.csv", nrows = 0).columns
            pokedata = pd.read_csv("data/pokedex.csv", skiprows = number - 1, nrows = 1)
            pokedata.columns = columns
            pokedata.set_index("number", inplace = True)
            pokedata["type"] = "/".join([pokedata["type1"].values[0], pokedata["type2"].values[0]])
            print(pokedata[['generation', 'name', 'type', 'HP', 'attack', 
                            'defense', 'sp_attack', 'sp_defense', 'speed']])
        except FileNotFoundError:
            print("No pokedex available to fill, try creating one by using the -c option")
        except pd.errors.EmptyDataError:
            print("Entry not found in your pokedex")
    else:
        print("Invalid pokemon number")


if __name__ == "__main__":
    args = get_args()
    
    if args.fill is True:
        fill_pokedex()
    elif args.create is True:
        create_pokedex()
    elif args.number is not None:
        check_pokedex(args.number)
