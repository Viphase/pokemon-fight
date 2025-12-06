from pathlib import Path

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

SPEED = 5
SIZE = 100

MAX_POKEMON_ATK = 5
MAX_POKEMON_DF = 5

NOT_STARTED = -1
STARTED = 0
HIT_DELAY = 50
BATTLE_TEAM_SIZE = 5

FIRE_SPRITE = str(Path(__file__).parent / "images" / "fire.png")
WATER_SPRITE = str(Path(__file__).parent / "images" / "water.png")
ELECTRIC_SPRITE = str(Path(__file__).parent / "images" / "electric.png")
GRASS_SPRITE = str(Path(__file__).parent / "images" / "grass.png")
TRAINER_1_SPRITE = str(Path(__file__).parent / "images" / "trainer_1.png")
TRAINER_2_SPRITE = str(Path(__file__).parent / "images" / "trainer_2.png")
BG_SPRITE = str(Path(__file__).parent / "images" / "bg.png")