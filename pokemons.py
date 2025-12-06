from __future__ import annotations

from config import *
from facade import *
import pygame

import random
from math import sin, cos, pi


class Pokemon:
    def __init__(self, name: str, atk: int, df: int, x: int, y: int, image: pygame.Surface, pokemon_list: list, facade: PygameFacade):
        #In constructor we have PyGame facade
        #name, hit points, attack power,
        #defense value, x, y, speed,
        #direction and rect of a Pokemon
        self.facade = facade
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.atk = atk
        self.df = df
        self.evolution_stage = 0
        self.evolution_flash_timer = 0
        self.spawn_time = pygame.time.get_ticks()
        self.active_time = 0

        self.x = x
        self.y = y
        self.speed = SPEED

        self.dir_x, self.dir_y = 0, 0
        angle = random.uniform(0.0, 2 * pi)
        self.dir_x = cos(angle) * self.speed
        self.dir_y = sin(angle) * self.speed

        self.image = image
        self.original_image = image
        self.flipped_image = pygame.transform.flip(image, True, False)
        self.facing_reversed = False
        self.pokemon_list = pokemon_list

        self.rect = self.facade.create_rect(0, 0, int(self.image.get_width() * 0.6), int(self.image.get_height() * 0.6))
        self.rect.center = (int(self.x), int(self.y))

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        #It's a function to set hit points value
        self._hp = max(0, value)

    @property
    def atk(self) -> int:
        return self._atk
    
    @atk.setter
    def atk(self, value: int) -> None:
        #It's a function to set attack power value
        if value <= 0:
            self._atk = 0
        else:
            self._atk = value

    @property
    def df(self) -> int:
        return self._df
    
    @df.setter
    def df(self, value: int) -> None:
        #It's a function to set defense value
        if value <= 0:
            self._df = 0
        else:
            self._df = value

    def attack(self, other: Pokemon) -> None:
        #It's a function to attack enemies
        if self.hp > 0 and other.hp > 0:
            if self.atk <= other.df:
                other.hp -= 1
            else:
                other.hp -= self.atk - other.df
            

    def check_evolution(self) -> None:
        #A function to check if pokemon should evolve
        current_time = pygame.time.get_ticks()
        self.active_time += current_time - self.spawn_time
        self.spawn_time = current_time
        
        if self.active_time >= 10000 and self.evolution_stage == 0:
            self.evolve()
            
    def evolve(self) -> None:
        #A function that evolves the pokemon
        if self.evolution_stage == 0:
            self.evolution_stage = 1
            
            self.atk += 2
            self.df += 1
            self.max_hp += 20
            self.hp = self.max_hp
            
            self.evolution_flash_timer = 60

    def draw(self, battle_state=None) -> None:
        #A function that draws the pokemon on the screen
        current_image = self.flipped_image if self.facing_reversed else self.image
        
        if self.evolution_flash_timer > 0:
            self.evolution_flash_timer -= 1
            if self.evolution_flash_timer % 10 < 5:
                glowing_image = current_image.copy()
                glowing_image.fill((255, 255, 0, 150), special_flags=pygame.BLEND_ADD)
                self.facade.screen.blit(glowing_image, self.rect)
            else:
                self.facade.screen.blit(current_image, self.rect)
        elif battle_state == STARTED:
            transparent_image = current_image.copy()
            transparent_image.set_alpha(90)
            self.facade.screen.blit(transparent_image, self.rect)
        else:
            self.facade.screen.blit(current_image, self.rect)

        if self.evolution_stage > 0:
            self.draw_golden_border()

    def draw_golden_border(self) -> None:
        #A function to draw golden border around evolved pokemon
        border_rect = pygame.Rect(self.rect.left - 2, self.rect.top - 2, 
                                self.rect.width + 4, self.rect.height + 4)
        pygame.draw.rect(self.facade.screen, (255, 215, 0), border_rect, 3)

    def move(self) -> None:
        #Obviosly function that
        #makes our Pokemon move
        if self.hp <= 0:
            return
        
        self.x += self.dir_x
        self.y += self.dir_y

        if self.x <= 0:
            self.dir_x = -self.dir_x
        elif self.x >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
            self.dir_x = -self.dir_x

        if self.y <= 0:
            self.dir_y = -self.dir_y
        elif self.y >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.dir_y = -self.dir_y

        self.rect.center = (int(self.x), int(self.y))

    def check_attack_collision(self, obstacle: Pokemon) -> None:
        #This function is needed to check
        #collisions with other Pokemons
        if isinstance(obstacle, Pokemon):
            if self.rect.colliderect(obstacle.rect):
                self.attack(obstacle)

    def die(self) -> None:
        # Obviously to remove Pokemon from screen
        if self in self.pokemon_list:
            self.pokemon_list.remove(self)


class FirePokemon(Pokemon):
    def __init__(self, name: str, atk: int, df: int, x: int, y: int, image, pokemon_list: list, facade: PygameFacade):
        super().__init__(name, atk, df, x, y, image, pokemon_list, facade)


class WaterPokemon(Pokemon):
    def __init__(self, name: str, atk: int, df: int, x: int, y: int, image, pokemon_list: list, facade: PygameFacade):
        super().__init__(name, atk, df, x, y, image, pokemon_list, facade)

    def attack(self, other: Pokemon) -> None:
        #It's a function to attack enemies, 
        #but WaterPokemon deals 3x damage to FirePokemons
        if self.hp > 0 and other.hp > 0:
            if isinstance(other, FirePokemon):
                if 3 * self.atk <= other.df:
                    other.hp -= 1
                else:
                    other.hp -= 3 * self.atk - other.df
            else:
                if self.atk <= other.df:
                    other.hp -= 1
                else:
                    other.hp -= self.atk - other.df
                    


class GrassPokemon(Pokemon):
    def __init__(self, name: str, atk: int, df: int, x: int, y: int, image, pokemon_list: list, facade: PygameFacade):
        super().__init__(name, atk, df, x, y, image, pokemon_list, facade)

    def attack(self, other: Pokemon) -> None:
        #It's a function to attack enemies, 
        #but GrassPokemon makes FirePokemons 
        #defense value less in 2 times
        if self.hp > 0 and other.hp > 0:
            if isinstance(other, FirePokemon):
                if self.atk <= other.df // 2:
                    other.hp -= 1
                else:
                    other.hp -= self.atk - other.df // 2
            else:
                if self.atk <= other.df:
                    other.hp -= 1
                else:
                    other.hp -= self.atk - other.df
                    


class ElectricPokemon(Pokemon):
    def __init__(self, name: str, atk: int, df: int, x: int, y: int, image, pokemon_list: list, facade: PygameFacade):
        super().__init__(name, atk, df, x, y, image, pokemon_list, facade)

    def attack(self, other: Pokemon) -> None:
        #It's a function to attack enemies, 
        #but ElectricPokemon makes WaterPokemons 
        #defense value set to 0ы
        if self.hp > 0 and other.hp > 0:
            if isinstance(other, WaterPokemon):
                if self.atk == 0:
                    other.hp -= 1
                else:
                    other.hp -= self.atk
            else:
                if self.atk <= other.df:
                    other.hp -= 1
                else:
                    other.hp -= self.atk - other.df
                    
