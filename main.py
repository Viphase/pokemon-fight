from facade import *
from config import *
from trainers import *
from pokemons import *
from world import *
from battle import *

pygame_facade = PygameFacade((SCREEN_WIDTH, SCREEN_HEIGHT), "Pokemon Game")

world = World(20, 0, 0, 800, 600, pygame_facade)
battle = Battle(5, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 100)

running = True
finished = False

while running:
    pygame_facade.handle_events()
    pygame_facade.clear_screen()

    if "bg" in world.SPRITES:
        pygame_facade.draw_image(world.SPRITES["bg"], 0, 0)
    
    if finished and battle.state == NOT_STARTED:
        finished = False

    if not battle.started():
        battle.start(world.trainers[0], world.trainers[1])

    if battle.state == STARTED or battle.state == SHOWING_RESULTS:
        if battle.state == SHOWING_RESULTS and not finished:
            finished = True
            
        world.draw(battle.state)
        battle.draw(pygame_facade.screen, pygame_facade, world.SPRITES)
        battle.update()

    else:
        world.draw()

    if pygame_facade.mouse_clicked and battle.state != STARTED:
        world.catch_pokemon(pygame_facade.mouse_pos)
        
    world.update(battle.state)

    pygame_facade.sprites.update()
    pygame_facade.update_screen()
    pygame_facade.clock.tick(FPS)
