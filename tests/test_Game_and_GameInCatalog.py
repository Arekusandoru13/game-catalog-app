from game_catalog import *

try:
    game1 = GameInList("T","dendy","1999.q2", ['action', 'shooter'], 'paused', 'blahblah')
except Exception as e:
    print(e)
    
#game1.add_genres([' RPG   ', 'invalid', '  Music '])
#game1.remove_genres(['RPG'])
print(game1.info())