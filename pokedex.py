import time
import random
import os
import sys

import importlib
from bs4 import BeautifulSoup
import pandas as pd


try:
    sys.path.append("functions")
    import scrapers as scrp
    import extractors as ext
    import progress_bar as pb
except ModuleNotFoundError:
    print("Could not find the necessary functions inside their folder...")
    time.sleep(1)
    sys.exit()


def pokecrawler(pokelist, verbose = 1):
    if verbose == 1:
        total_pokemon = str(len(pokelist))
        print(f"Looks like there's {total_pokemon} pokemon to read in the website...")
        time.sleep(1)
        print("Our Spinaraks will start going through them now!\n")
        time.sleep(1)
        progress_bar = pb.ProgressBar(total_pokemon = total_pokemon,
                                      current_pokename = "-", 
                                      current_pokenumber = 0, 
                                      bar_size = 30)

    index = 1
    for number in pokelist.index:
        if verbose == 1:
            name = pokelist.loc[number]["name"]
            progress_bar.update_bar(current_pokename = name, current_pokenumber = index)

        pokesoup = scrp.scrape_pokesoup(pokelist.loc[number]["link"])

        pokedata = ext.full_extractor(pokesoup)
        pokedata["number"] = number
        pokedata.set_index("number", inplace = True)

        pokedex_entry = pd.concat([pokelist.loc[[number]], pokedata], axis = 1)

        if index == 1:
            pokedex_entry.drop("link", axis = 1).to_csv("data/pokedex.csv")
        else:
            pokedex_entry.drop("link", axis = 1).to_csv("data/pokedex.csv", mode = "a", header = False)

        time.sleep(random.randint(1, 5))
        index = index + 1

    print("All set! Your pokedex is complete, and can be found inside the data folder")


if __name__ == "__main__":
    gen_1to7_list = scrp.create_gen_1to7_list()
    gen_8_list = scrp.create_gen_8_list()
    pokelist = pd.concat([gen_1to7_list, gen_8_list], axis = 0)
    
    os.makedirs("data", exist_ok = True)
    pokecrawler(pokelist)
