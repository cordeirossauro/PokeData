from bs4 import BeautifulSoup
import pandas as pd
import re

def find_string(soup, string, tag):
    i = 0
    inds = []

    for elem in soup.find_all(tag):
        if string in elem.get_text():
            inds.append(i)
            matched_string = string
        i = i + 1

    return inds


def gen_inf_extractor(soup):
    header_ind = find_string(soup, "Other Names", "tr")

    gen_inf_raw = soup.find_all("tr")[header_ind[0] + 1]

    male_ratio_raw = gen_inf_raw.find_all("td", class_ = "fooinfo")[3].get_text()

    if "Genderless" in male_ratio_raw:
        male_ratio = -100.0
    else:
        male_ratio = re.findall(r"\d+", male_ratio_raw)[0]

    types = []
    types_raw_list = gen_inf_raw.find_all("img")
    for type_raw in types_raw_list:
        types.append(type_raw.get("alt").split("-")[0])

    type1 = types[0]
    if len(types) == 2:
        type2 = types[1]
    else:
        type2 = "-"

    gen_inf = pd.DataFrame(columns = ["male_ratio", "type1", "type2"])

    gen_inf.loc[0] = [round(float(male_ratio)/100, 4), type1, type2]

    return gen_inf


def phys_inf_extractor(soup):
    header_ind = find_string(soup, "Classification", "tr")

    phys_inf_raw = soup.find_all("tr")[header_ind[0] + 1].find_all("td")

    classification = phys_inf_raw[0].get_text()
    height = (phys_inf_raw[1].get_text()).split("\t")[-1].split("m")[0]
    weight = (phys_inf_raw[2].get_text()).split("\t")[-1].split("kg")[0]
    capture_rate = phys_inf_raw[3].get_text().split(" ")[0]
    base_egg_steps = (phys_inf_raw[4].get_text()).replace(",", "")

    phys_inf = pd.DataFrame(columns = ["classification", "base_egg_steps",
                                       "capture_rate", "weight", "height"])

    phys_inf.loc[0] = [classification, int(base_egg_steps),
                       int(capture_rate), float(weight), float(height)]

    return phys_inf



def ment_inf_extractor(soup):
    header_ind = find_string(soup, "Experience Growth", "tr")

    ment_inf_raw = soup.find_all("tr")[header_ind[0] + 1].find_all("td")

    base_happiness = ment_inf_raw[-3].get_text()
    experience_growth = ment_inf_raw[-4].get_text().split(" ")[0]

    ment_inf = pd.DataFrame(columns = ["base_happiness", "experience_growth"])

    ment_inf.loc[0] = [int(base_happiness), int(experience_growth.replace(",", ""))]

    return ment_inf

def abilities_extractor(soup):
    header_ind = find_string(soup, "Abilities", "tr")

    abilities_raw = soup.find_all("tr")[header_ind[0]].find_all("td")

    abilities = abilities_raw[0].get_text().split(":")[1].split("-")
    abilities = [ability.strip() for ability in abilities]

    abilities_df = pd.DataFrame(columns = ["Abilities"])
    abilities_df.loc[0] = [abilities]

    return abilities_df


def weaknesses_extractor(soup):
    header_ind = find_string(soup, "Weakness", "tr")

    weakness_raw = soup.find_all("tr")[header_ind[0] + 2].find_all("td")
    
    weaknesses = []
    for index in range(len(weakness_raw)):
        weakness = weakness_raw[index].get_text().split("*")[1]
        weaknesses.append(weakness)

    poketypes = ["normal", "fire", "water", "electric", "grass", "ice",
                 "fight", "poison", "ground","flying", "psychic", "bug",
                 "rock", "ghost", "dragon", "dark", "steel", "fairy"]

    weaknesses_df = pd.DataFrame(columns = [poketype + "_weakness" for poketype
                                            in poketypes])

    weaknesses_df.loc[0] = weaknesses

    return weaknesses_df


def base_stats_extractor(soup):
    header_ind = find_string(soup, "Base Stats", "tr")

    base_stats_raw = soup.find_all("tr")[header_ind[0]].find_all("td")

    base_stats = pd.DataFrame(columns = ["base_HP", "base_attack", "base_defense",
                                         "base_sp_attack", "base_sp_defense", "base_speed"])

    base_stats.loc[0] = [int(base_stats_raw[1].get_text()),
                         int(base_stats_raw[2].get_text()),
                         int(base_stats_raw[3].get_text()),
                         int(base_stats_raw[4].get_text()),
                         int(base_stats_raw[5].get_text()),
                         int(base_stats_raw[6].get_text())]

    return base_stats


def max_stats_extractor(soup):
    header_ind = find_string(soup, "Beneficial Nature", "tr")

    max_stats_raw = soup.find_all("tr")[header_ind[0] + 1].find_all("td")

    max_stats = pd.DataFrame(columns = ["max_HP_low", "max_HP_high", "max_attack_low", "max_attack_high", 
                                        "max_defense_low", "max_defense_high", "max_sp_attack_low",
                                        "max_sp_attack_high", "max_sp_defense_low", "max_sp_defense_high",
                                        "max_speed_low", "max_speed_high"])

    max_stats.loc[0] = [int(max_stats_raw[1].get_text().split("-")[0]),
                        int(max_stats_raw[1].get_text().split("-")[1]),
                        int(max_stats_raw[2].get_text().split("-")[0]),
                        int(max_stats_raw[2].get_text().split("-")[1]),
                        int(max_stats_raw[3].get_text().split("-")[0]),
                        int(max_stats_raw[3].get_text().split("-")[1]),
                        int(max_stats_raw[4].get_text().split("-")[0]),
                        int(max_stats_raw[4].get_text().split("-")[1]),
                        int(max_stats_raw[5].get_text().split("-")[0]),
                        int(max_stats_raw[5].get_text().split("-")[1]),
                        int(max_stats_raw[6].get_text().split("-")[0]),
                        int(max_stats_raw[6].get_text().split("-")[1])]

    return max_stats


def full_extractor(soup):
    gen_inf = gen_inf_extractor(soup)
    phys_inf = phys_inf_extractor(soup)
    ment_inf = ment_inf_extractor(soup)
    abilities = abilities_extractor(soup)
    weaknesses = weaknesses_extractor(soup)
    base_stats = base_stats_extractor(soup)
    max_stats = max_stats_extractor(soup)

    return pd.concat([gen_inf, 
                      phys_inf,
                      ment_inf,
                      abilities, 
                      weaknesses, 
                      base_stats,
                      max_stats],
                    axis = 1)
