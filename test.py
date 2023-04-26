from game import *
g = Game()
gameDifficulty = "hard"
r = [random.choices(
    GAME_CONFIG[gameDifficulty]['treasure']['types'], weights=GAME_CONFIG[gameDifficulty]['treasure']['weights'], k=GAME_CONFIG[gameDifficulty]['treasure']['count'])][0]
print(r)