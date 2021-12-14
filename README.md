This repo is divided into two different parts, each one with its individual folder:

- pokescraper: A web scraper designed to get data for all the pokemon available at [serebii.net](https://serebii.net/) and store it locally in a .csv file;
- data analysis: Basic Exploratory Data Analysis of the pokemon data obtained using the pokescraper.

# pokescraper

To use the scraper, navigate to the pokescraper folder and run the pokedex.py file using the command:

```
python3 pokedex.py
```

The command above doesn't actually initializes the scraper. To do that, it's necessary to run the file with one of the options below:

- -c: Creates a new pokedex.csv file inside the data/ folder (if there is no data/ folder, one is created) and fills it with data;
- -f: Fills an existing pokedex with the missing pokemon (useful if you started the scraping process but didn't finish it).

When initialized, the scraper will start going through all pokemon, collecting the following data:

- **General Details**: Name, Generation, Number, Male Ratio, Type(s), Classification
- **Physical Details**: Base Egg Steps, Capture Rate, Weight, Height
- **Mental Details**: Base Happiness, Experience Growth, Abilities
- **Weaknesses**: One weakness against each pokemon type (18 in total)
- **Base Stats**: HP, Attack, Defense, Special Attack, Special Defense, Speed

Since the algorithm writes the details of each pokemon to the .csv as soon as it reads them, there's no progress lost when the scraping is stopped before being fully completed.

And lastly, the pokedex.py file also comes with an option to look up and print the details of a specific pokemon from the local pokedex, and it can be used with:

```
python3 pokedex.py -l pokemon_number
```

# data analysis

Inside this folder there's a notebook with some basic exploratory analysis of the data obtained using the pokescraper and all images created to illustrate the most interesting findings.

### Pokemon Types

There are 18 different types, and since each pokemon can be either single-type (ST) or dual-type (DT), they have 324 (18²) possible combinations. The image below shows the distribution of pokemon according to their type; the x axis represents the main type (or type1), and the y axis represents the second type (or type2). The squares on the main diagonal (where type1 = type2) are for the ST pokemon.

<p align="center">
  <img src="data analysis/type/types_heatmap.png" height=750>
</p>

Some conclusions that we can make by analysing the graph:

- Some type combinations are much more populated than others, and many are not even represented by a pokemon;
- Among the most common combinations, almost all of them are single-type;
- Flying is the only type whose ST combination is not the most common one (only 3 Flying ST pokemon, the least common ones among the STs);

For the statistical analysis of the data we want to ensure that all the combinations being studied have enough examples in them, so we focus only on the 12 most common ones. They are represented on the table below, and as expected, all except one are STs.

| **Combination** | **n of Pokemon** |   |  **Combination**  | **n of Pokemon** |
|:-----------:|:------------:|:-:|:-------------:|:------------:|
|    Normal   |      68      |   |    Fighting   |      29      |
|    Water    |      67      |   | Normal/Flying |      26      |
|    Grass    |      44      |   |      Bug      |      20      |
|   Psychic   |      39      |   |     Fairy     |      19      |
|     Fire    |      33      |   |     Ground    |      17      |
|   Electric  |      33      |   |      Rock     |      16      |

## Base Stats

According to Bulpedia's [article about stats](https://bulbapedia.bulbagarden.net/wiki/Stat), they are values related to some aspects of combat. There are six different stat, and they are:

- **HP**: Determines how much damage a pokemon can receive before fainting (losing the combat);
- **Attack**: Partly determines how much damage a pokemon deals when using a **physical** move;
- **Defense**: Partly determines how much damage a pokemon receives when hit with a **physical** move;
- **Special Attack**: Partly determines how much damage a pokemon deals when using a **special** move;
- **Special Defense**: Partly determines how much damage a pokemon receives when hit with a **special** move;
- **Speed**: Determines the order that pokemon can act in a battle (pokemon with higher speed will generally act first).

If we look at the base stats (values for a specimen of level 1) distribution for each one of the 12 combinations choosen on the last topic, we see that they can be split in three different categories (based on a comparison of physical stats and special stats):

- **Physical**: Combinations in this category have pokemon with higher physical stats (Attack > Sp.Attack, Defense >  Sp. Defense);
- **Special**: Combinations in this category have pokemon with higher special stats (Attack < Sp. Attack, Defense < Sp. Defense);
- **Balanced**: This category holds the combinations that don't fit the other two. This happens if a combination has pokemon with balanced physical and special stats or if a combination has an equal number of physical and special pokemon.

Below we show all the stats distribution, organized according to the categories that we defined:

### Physical Types

<p align="center">
  <img src="data analysis/stats/Ground.png" height=250>
  <img src="data analysis/stats/Rock.png" height=250>
</p>
<p align="center">
  <img src="data analysis/stats/Fighting.png" height=250>
  <img src="data analysis/stats/Normal - Flying.png" height=250>
</p>

### Special Types

<p align="center">
  <img src="data analysis/stats/Fairy.png" height=250>
  <img src="data analysis/stats/Psychic.png" height=250>
</p>

### Balanced Types

<p align="center">
  <img src="data analysis/stats/Bug.png" height=250>
  <img src="data analysis/stats/Electric.png" height=250>
</p>
<p align="center">
  <img src="data analysis/stats/Fire.png" height=250>
  <img src="data analysis/stats/Grass.png" height=250>
</p>
<p align="center">
  <img src="data analysis/stats/Normal.png" height=250>
  <img src="data analysis/stats/Water.png" height=250>
</p>

The difference between these categories is even more pronounced on scatter plots of Physical vs Special stats, as can be seen below. The pokemon from Balanced types aren't included because, since they're present in both regions of the graph, they would clutter the visualization.

<p align="center">
  <img src="data analysis/stats/combat stats.png" height=500>
</p>

Specially on the Attack vs Sp. Attack plot, pokemon from the physical types are almost always above the dotted line, which means that they all have Attack > Sp. Attack. When it comes to the defense, the separation between the categories isn't as pronounced, and some pokemon end up crossing the line to the opposing region of the graph (but even in these cases, the pokemon that cross tend to stay close to the line).

## Abilities
Again, according to a Bulbedia's [article about abilities](https://bulbapedia.bulbagarden.net/wiki/Ability#Hidden_Abilities), they are a game mechanic that provides a passive effect to the pokemon during battle or in the overworld. Even though a pokemon can only have one active ability some species have two possible ones, and one of them is choosen at random when the pokemon appears. Also, some species have what is called a hidden ability that can be activated (in that case, the previous one is deactivated) through a specific route inside the game.

With that in mind, the most 10 common regular and hidden abilities among the types choosen for out study were studied separately, as can be seen in the sections below.

### Regular Abilities

<p align="center">
  <img src="data analysis/abilities/reg abilities distribution.png" height=500>
</p>

The graph on the left shows that four of the most common regular abilities (Swift Swim, Torrent, Blaze and Overgrown) are present in only one type of pokemon (the first two on Water, the thrid one on Fire and the fourth on Grass). This is somewhat expected when we consider that an "exclusive" ability would only be among the most common ones if it came from an equally common type of pokemon, and in all four this is the case.

When it comes to Normal pokemon (the most common ones), we see that all five of the regular abilities in the graph present in this type are also present in other types, and this most likely means that there's no "exclusive" ability among Normal pokemon, since if this were the case, it would probably show up in the graph.

### Hidden Abilities
<p align="center">
  <img src="data analysis/abilities/hidden abilities distribution.png" height=500>
</p>

The first thing to note in this case is that the hidden abilities are much less common (the one with the highest count only appears 12 times, compared to 25 in the regular case), and this ratio actually agrees with the fact that pokemon can have up to 2 regular abilities, but only a single hidden one. 

Another difference between the distribution is that, in this case, there is no hidden ability among the most common ones that is exclusive to a single type, which seems to indicate that hidden abilities are much more "distributed" than regular ones.
