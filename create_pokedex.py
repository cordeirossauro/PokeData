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
except ModuleNotFoundError:
    print("Could not find the necessary functions inside their folder...")
    time.sleep(1)
    sys.exit()



def pokecrawler(pokelist, verbose = 1):

    total_pokemon = str(len(pokelist))
    if verbose == 1:
        print(f"Looks like there's {total_pokemon} pokemon to read in the website...")
        time.sleep(1)
        print("Our Spinaraks will start going through them now!\n")
        time.sleep(1)


    pokedata = pd.DataFrame()
    index = 1
    for number in pokelist.index:
        if verbose == 1:
            name = pokelist.loc[number]["name"]
            print(" " * 50, end = "\r")
            print(f"[{index}/{total_pokemon}] Scraping data for {name}", end = '\r')

        pokesoup = scrp.scrape_pokesoup(pokelist.loc[number]["link"])

        gen_inf = ext.gen_inf_extractor(pokesoup)
        phys_inf = ext.phys_inf_extractor(pokesoup)
        ment_inf = ext.ment_inf_extractor(pokesoup)
        abilities = ext.abilities_extractor(pokesoup)
        weaknesses = ext.weaknesses_extractor(pokesoup)
        stats = ext.stats_extractor(pokesoup)

        pokedata = pd.concat([gen_inf, phys_inf, ment_inf,
                              abilities, weaknesses, stats],
                             axis = 1)
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
