from __future__ import annotations

from pokemons import *
from facade import *

class Trainer:
    #Trainer can pick Pokemons from his box
    #and fight them with another team
    def __init__(self, name: str, x: int, y: int, image, facade: PygameFacade):
        self.facade = facade
        
        self.name = name
        self.box = []
        self.wins = 0

        self.x = x
        self.y = y
        self.image = image
        
        self.rect = self.facade.create_rect(0, 0, int(self.image.get_width() * 0.6), int(self.image.get_height() * 0.6))
        self.rect.center = (int(self.x), int(self.y))
    
    def add(self, pokemon: Pokemon) -> None:
        #This function adds pokemon to trainer's box
        self.box.append(pokemon)

    def best_team(self, amount: int) -> list:
        # Return first `amount` pokemons without mutating the box
        return self.box[:amount]
    
    def draw(self) -> None:
        #This function draws the trainer on the screen
        sprite_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.rect.center = sprite_rect.center
        self.facade.screen.blit(self.image, sprite_rect)


class SmartTrainer(Trainer):
    #SmartTrainer is a trainer that can pick Pokemons
    #better than a regular Trainer
    def best_team(self, amount: int) -> list:
        team = []
        fire = []
        water = []
        grass = []
        electric = []
        for pokemon in self.box:
                if type(pokemon) == FirePokemon:
                    fire.append(pokemon)
                elif type(pokemon) == WaterPokemon:
                    water.append(pokemon)
                elif type(pokemon) == GrassPokemon:
                    grass.append(pokemon)
                elif type(pokemon) == ElectricPokemon:
                    electric.append(pokemon)    

        for pokemon in water:
            if pokemon.atk >= 5 and pokemon.df >= 5:
                team.append(pokemon)

        for pokemon in electric:
            if pokemon.atk >= 5 and pokemon.df >= 5:
                team.append(pokemon)

        for pokemon in grass:
            if pokemon.atk >= 5 and pokemon.df >= 5:
                team.append(pokemon)

        for pokemon in fire:
            if pokemon.atk >= 5 and pokemon.df >= 5:
                team.append(pokemon)
                
        if len(team) < amount:
            for pokemon in self.box:
                if pokemon not in team:
                    team.append(pokemon)
                    if len(team) >= amount:
                        break

        return team[:amount]
