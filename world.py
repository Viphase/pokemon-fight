from pokemons import *
from config import *
from trainers import *
import random


class World:
    pokemons = []
    _instance = None

    def __new__(cls, *args):
        #It is a singleton pattern so it makes only one world instance
        if cls._instance is None:
            cls._instance = super(World, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, n_pok: int, x1: int, y1: int, x2: int, y2: int, facade: PygameFacade):
        self.facade = facade
        self.n_poc = n_pok
        self.rect = facade.create_rect(x1, y1, x2 - x1, y2 - y1)
        self.trainers = []
        self.next_trainer = 0
        self.SPRITES = {
            "electrc": self.facade.load_image(ELECTRIC_SPRITE, SIZE, SIZE),
            "fire": self.facade.load_image(FIRE_SPRITE, SIZE, SIZE),
            "water": self.facade.load_image(WATER_SPRITE, SIZE, SIZE),
            "grass": self.facade.load_image(GRASS_SPRITE, SIZE, SIZE),
            "trainer_1": self.facade.load_image(TRAINER_1_SPRITE, SIZE, 2*SIZE),
            "trainer_2": self.facade.load_image(TRAINER_2_SPRITE, 1.6*SIZE, 2*SIZE),
            "bg": self.facade.load_image(BG_SPRITE, SCREEN_WIDTH, SCREEN_HEIGHT)
        }
        self.generate_pokemones()
        self.generate_trainers()

    def generate_pokemones(self) -> None:
        #A function to generate random types pokemons on screen
        for _ in range(self.n_poc):
            pokemon_type = random.randint(0, 3)
            if pokemon_type == 0:
                self.pokemons.append(ElectricPokemon("ep", random.randint(1, MAX_POKEMON_ATK), random.randint(1, MAX_POKEMON_DF), self.rect.center[0], self.rect.center[1], self.SPRITES["electrc"], self.pokemons, self.facade))
            if pokemon_type == 1:
                self.pokemons.append(FirePokemon("fp", random.randint(1, MAX_POKEMON_ATK), random.randint(1, MAX_POKEMON_DF), self.rect.center[0], self.rect.center[1], self.SPRITES["fire"], self.pokemons, self.facade))
            if pokemon_type == 2:
                self.pokemons.append(WaterPokemon("wp", random.randint(1, MAX_POKEMON_ATK), random.randint(1, MAX_POKEMON_DF), self.rect.center[0], self.rect.center[1], self.SPRITES["water"], self.pokemons, self.facade))
            if pokemon_type == 3:
                self.pokemons.append(GrassPokemon("gp", random.randint(1, MAX_POKEMON_ATK), random.randint(1, MAX_POKEMON_DF), self.rect.center[0], self.rect.center[1], self.SPRITES["grass"], self.pokemons, self.facade))
    
    def generate_trainers(self) -> None:
        #A function to generate trainers on screen
        self.trainers.append(SmartTrainer("Left Trainer", 60, SCREEN_HEIGHT // 2, self.SPRITES["trainer_1"], self.facade))
        self.trainers.append(SmartTrainer("Right Trainer", SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2, self.SPRITES["trainer_2"], self.facade))

    def draw(self, battle_state=None) -> None:
        #A function to draw all pokemons and trainers on screen
        for pokemon in self.pokemons:
            pokemon.draw(battle_state)
        for trainer in self.trainers:
            trainer.draw()

    def update(self, battle_state=None) -> None:
        #A function to update the world
        if battle_state != STARTED:
            for pokemon in self.pokemons:
                pokemon.move()
                pokemon.check_evolution()

        trainer1_count = len(self.trainers[0].box)
        trainer2_count = len(self.trainers[1].box)
        
        self.facade.draw_text(f"Trainer 1: {trainer1_count} pokemon", 10, 10, (255, 255, 255), 20)
        self.facade.draw_text(f"Trainer 2: {trainer2_count} pokemon", 10, 35, (255, 255, 255), 20)
        self.facade.draw_text(f"Need: {BATTLE_TEAM_SIZE} each for battle", 10, 60, (255, 255, 255), 20)
        
        # Count evolved pokemon in world and trainer boxes
        evolved_in_world = sum(1 for p in self.pokemons if hasattr(p, 'evolution_stage') and p.evolution_stage > 0)
        evolved_in_boxes = sum(1 for trainer in self.trainers for p in trainer.box if hasattr(p, 'evolution_stage') and p.evolution_stage > 0)
        evolved_count = evolved_in_world + evolved_in_boxes
        self.facade.draw_text(f"Evolved Pokemon: {evolved_count}", 10, 85, (255, 215, 0), 20)
        
        if trainer1_count >= BATTLE_TEAM_SIZE and trainer2_count >= BATTLE_TEAM_SIZE:
            team1 = self.trainers[0].best_team(BATTLE_TEAM_SIZE)
            team2 = self.trainers[1].best_team(BATTLE_TEAM_SIZE)
            self.facade.draw_text(f"Team 1 selected: {len(team1)}", 10, 110, (255, 255, 0), 20)
            self.facade.draw_text(f"Team 2 selected: {len(team2)}", 10, 135, (255, 255, 0), 20)

    def catch_pokemon(self, pos) -> None:
        #A function to catch pokemons on mouse click
        catched = []
        for pokemon in self.pokemons[:]:
            rect = pokemon.image.get_rect()
            if rect.left + pokemon.x <= pos[0] <= rect.right + pokemon.x and rect.top + pokemon.y <= pos[1] <= rect.bottom + pokemon.y:
                self.pokemons.remove(pokemon)
                catched.append(pokemon)
        for pokemon in catched:
            self.trainers[self.next_trainer].box.append(pokemon)
            self.next_trainer = 1 - self.next_trainer
