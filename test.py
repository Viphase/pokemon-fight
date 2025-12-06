import os
import pygame
import pytest

from trainers import Trainer, SmartTrainer
from pokemons import Pokemon, FirePokemon, WaterPokemon, GrassPokemon, ElectricPokemon


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    yield
    pygame.quit()


class MinimalFacade:
    def __init__(self):
        self.screen = pygame.Surface((10, 10))

    def create_rect(self, x, y, w, h):
        return pygame.Rect(x, y, w, h)


def make_surface():
    return pygame.Surface((10, 10), pygame.SRCALPHA)


def test_hp_never_negative():
    facade = MinimalFacade()
    p = Pokemon("p", 1, 1, 0, 0, make_surface(), [], facade)
    p.hp = -50
    assert p.hp == 0


def test_attack_basic_damage():
    facade = MinimalFacade()
    a = Pokemon("a", atk=5, df=1, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    b = Pokemon("b", atk=1, df=3, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    b.hp = 10
    a.attack(b)  # 5 - 3 = 2
    assert b.hp == 8


def test_water_vs_fire_triple_damage():
    facade = MinimalFacade()
    water = WaterPokemon("w", atk=4, df=1, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    fire = FirePokemon("f", atk=1, df=3, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    fire.hp = 20
    water.attack(fire)  # 3*4 - 3 = 9
    assert fire.hp == 11


def test_grass_halves_fire_defense():
    facade = MinimalFacade()
    grass = GrassPokemon("g", atk=6, df=1, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    fire = FirePokemon("f", atk=1, df=5, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    fire.hp = 20
    grass.attack(fire)  # 6 - (5//2 = 2) = 4
    assert fire.hp == 16


def test_electric_ignores_water_defense():
    facade = MinimalFacade()
    electric = ElectricPokemon("e", atk=7, df=1, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    water = WaterPokemon("w", atk=1, df=100, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    water.hp = 25
    electric.attack(water)  # deals atk directly (7)
    assert water.hp == 18


def test_trainer_add_and_best_team_slice():
    facade = MinimalFacade()
    t = Trainer("t", 0, 0, make_surface(), facade)
    p1 = Pokemon("p1", 1, 1, 0, 0, make_surface(), [], facade)
    p2 = Pokemon("p2", 1, 1, 0, 0, make_surface(), [], facade)
    p3 = Pokemon("p3", 1, 1, 0, 0, make_surface(), [], facade)
    t.add(p1)
    t.add(p2)
    t.add(p3)
    team = t.best_team(2)
    assert team == [p1, p2]
    # Ensure original box not mutated
    assert t.box == [p1, p2, p3]


def test_smart_trainer_picks_strong_then_fills():
    facade = MinimalFacade()
    t = SmartTrainer("s", 0, 0, make_surface(), facade)
    strong_water = WaterPokemon("sw", atk=6, df=6, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    weak_fire = FirePokemon("wf", atk=2, df=2, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    weak_grass = GrassPokemon("wg", atk=1, df=3, x=0, y=0, image=make_surface(), pokemon_list=[], facade=facade)
    t.add(strong_water)
    t.add(weak_fire)
    t.add(weak_grass)
    team = t.best_team(2)
    assert strong_water in team
    assert len(team) == 2

