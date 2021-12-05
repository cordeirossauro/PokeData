import math

class ProgressBar:
    def __init__(self, total_pokemon, current_pokename, current_pokenumber, bar_size):
        self.total_pokemon = int(total_pokemon)
        self.current_pokename = current_pokename
        self.current_pokenumber = current_pokenumber
        self.bar_size = bar_size


    def print_bar(self):
        steps_done = math.floor(self.current_pokenumber/self.total_pokemon * self.bar_size)
        
        bar = " [" + ("=" * steps_done) + ">" + (" " * (self.bar_size - 1 - steps_done)) + "]"
        progress = f" [{self.current_pokenumber}/{self.total_pokemon}]"
        details = f" Scraping data for {self.current_pokename}"

        print(progress + bar + details + 10 * " ", end = "\r")


    def update_bar(self, current_pokename, current_pokenumber):

        self.current_pokename = current_pokename
        self.current_pokenumber = current_pokenumber
        self.print_bar()
