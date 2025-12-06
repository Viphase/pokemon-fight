## Pokemon Game (Pygame)

A simple Pokemon-style mini game built with Pygame.

### Description
- You control a trainer on a scene where pokemons periodically appear.
- The game features a catching mode and a battle mode between two trainers.
- Sprites and scene are rendered using `pygame` with a fixed FPS.

### Game Rules
- Click a pokemon with the mouse to try to catch it into your team.
- In battle, each trainer has a team of up to 5 pokemons.
- Battle rounds proceed automatically: pokemons deal and receive damage in turns.
- The winner is the trainer with more surviving pokemons at the end of the rounds.

### Requirements
```
PyGame Library
```

### How to run
```bash
python main.py
```

### Project structure
```
pokemons/
  main.py          # the main file
  config.py        # settings and sprite paths
  facade.py        # a pygame facade
  world.py         # world rendering and update
  pokemons.py      # pokemons and behavior
  trainers.py      # trainers logic
  battle.py        # battle logic & UI
  images/          # sprites (png)
```


