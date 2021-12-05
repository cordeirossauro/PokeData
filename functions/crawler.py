import time
import sys
import random
import pandas as pd

try:
    sys.path.append("functions")
    import scrapers as scrp
    import extractors as ext
    import progress_bar as pb
except ModuleNotFoundError:
    print("Could not find the necessary functions inside their folder...")
    sys.exit()

def pokecrawler(pokelist, fill, verbose):
    if verbose is True:
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
        if verbose is True:
            name = pokelist.loc[number]["name"]
            progress_bar.update_bar(current_pokename = name, current_pokenumber = index)

        pokesoup = scrp.scrape_pokesoup(pokelist.loc[number]["link"])

        pokedata = ext.full_extractor(pokesoup)
        pokedata["number"] = number
        pokedata.set_index("number", inplace = True)

        pokedex_entry = pd.concat([pokelist.loc[[number]], pokedata], axis = 1)

        if (index == 1) & (fill is False):
            pokedex_entry.drop("link", axis = 1).to_csv("data/pokedex.csv")
        else:
            pokedex_entry.drop("link", axis = 1).to_csv("data/pokedex.csv", mode = "a", header = False)

        time.sleep(random.randint(1, 5))
        index = index + 1

    if verbose is True:
        print("All set! Your pokedex is complete, and can be found inside the data folder")