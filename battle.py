import pygame
from config import *
from trainers import *

SHOWING_RESULTS = 1

class Battle:
    def __init__(self, n: int, x: int, y: int):
        self.n = n
        self.x = x
        self.y = y
        self.turn = 1
        self.state = NOT_STARTED
        self.result_display_time = 0
        self.result_duration = 3000
        self.winner = None

    def draw(self, surface: pygame.Surface, facade: PygameFacade, world_sprites=None) -> None:
        #A function to draw UI and pokemons on the screen
        if self.state == NOT_STARTED:
            return
        
        if self.state == SHOWING_RESULTS:
            winner_name = self.trainer1.name if self.winner == 1 else self.trainer2.name

            facade.draw_text(f"Battle Over! {winner_name} wins!", 
                           SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 80, 
                            color=(255, 255, 0), size=36)
            facade.draw_text(f"{self.trainer1.name}: {self.trainer1.wins} wins", 
                           SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 
                            color=(255, 255, 255), size=24)
            facade.draw_text(f"{self.trainer2.name}: {self.trainer2.wins} wins", 
                           SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 
                            color=(255, 255, 255), size=24)
            return
            
        for pokemon in self.team1 + self.team2:
            pokemon.draw()
        if len(self.team1) > 0 and len(self.team2) > 0:
            pygame.draw.line(
                surface,
                    (255, 0, 0),
                    self.team1[0].rect.midright,
                    self.team2[0].rect.midleft,
                    3
                )
            
            hit_circle = pygame.Surface((self.team1[0].rect.width, self.team1[0].rect.height), pygame.SRCALPHA)
            pygame.draw.circle(hit_circle, (255, 0, 0, 100), hit_circle.get_rect().center, hit_circle.get_rect().width//2 - 5, 0)            
            
            if self.turn == 1:
                surface.blit(hit_circle, self.team2[0].rect.topleft)
            else:
                surface.blit(hit_circle, self.team1[0].rect.topleft)


    def start(self, trainer1: Trainer, trainer2: Trainer) -> None:
        #A function that starts the battle
        if self.state == NOT_STARTED:
            self.trainer1 = trainer1
            self.trainer2 = trainer2
            self.team1 = trainer1.best_team(self.n)
            self.team2 = trainer2.best_team(self.n)
            if len(self.team1) < self.n or len(self.team2) < self.n:
                return

            for pokemon in self.team1:
                if pokemon in self.trainer1.box:
                    self.trainer1.box.remove(pokemon)
            for pokemon in self.team2:
                if pokemon in self.trainer2.box:
                    self.trainer2.box.remove(pokemon)

            y = self.y
            for pokemon in self.team1:
                pokemon.x, pokemon.y = self.x, y
                y += 42 + 20
                pokemon.dir_x = pokemon.dir_y = 0
                pokemon.rect.center = (int(pokemon.x), int(pokemon.y))
                pokemon.facing_reversed = True
            y = self.y
            for pokemon in self.team2:
                pokemon.x, pokemon.y = self.x + 280, y
                y += 42 + 20
                pokemon.dir_x = pokemon.dir_y = 0
                pokemon.rect.center = (int(pokemon.x), int(pokemon.y))
                pokemon.facing_reversed = False
            
            for pokemon in self.team1 + self.team2:
                pokemon.hp = 100
            self.state = STARTED
            self.last_update = pygame.time.get_ticks()


    def update(self) -> None:
        #An function to update the battle and the attack to happen
        if self.state == STARTED:
            nowTime = pygame.time.get_ticks() 
            if nowTime - self.last_update > HIT_DELAY:
                self.last_update = nowTime
            else:
                return
            
            if self.turn == 1 and len(self.team1) > 0 and len(self.team2) > 0:
                self.team1[0].attack(self.team2[0])
                if self.team2[0].hp <= 0:
                    self.team2.remove(self.team2[0])
                if len(self.team2) == 0:
                    return self.finish(1)
                
            elif self.turn == 2 and len(self.team1) > 0 and len(self.team2) > 0:
                self.team2[0].attack(self.team1[0])
                if self.team1[0].hp <= 0:
                    self.team1.remove(self.team1[0])
                if len(self.team1) == 0:
                    return self.finish(2)
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
                
        elif self.state == SHOWING_RESULTS:
            if pygame.time.get_ticks() - self.result_time > self.result_duration:
                self.state = NOT_STARTED
                self.reset_battle()

    def finish(self, result: int) -> None:
        #A function to finish the battle and get the results
        self.winner = result
        self.state = SHOWING_RESULTS
        self.result_time = pygame.time.get_ticks()
        
        if result == 1:
            for pokemon in self.team1:
                self.trainer1.add(pokemon)
            self.trainer1.wins += 1 
        else:
            for pokemon in self.team2:
                self.trainer2.add(pokemon)
            self.trainer2.wins += 1

        for pokemon in self.team1 + self.team2:
            pokemon.facing_reversed = False


    def started(self) -> bool:
        return True if self.state == STARTED else False
    
    def reset_battle(self) -> None:
        #A function to reset battle state and clear teams
        self.team1 = []
        self.team2 = []
        self.turn = 1
        self.winner = None