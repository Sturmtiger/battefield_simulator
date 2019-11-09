"""
This module runs the game
"""

from battlefield import Game


if __name__ == '__main__':
    MODES = ['create_new_structure', 'create_from_json_structure']
    print('Choose your option:',
          '\t1. New game',
          '\t2. Replay last game', sep='\n')
    MODE_INDEX = int(input('Enter the number of chosen option: ')) - 1
    CHOSEN_MODE = MODES[MODE_INDEX]
    PREPARED_GAME_INSTANCE = getattr(Game, CHOSEN_MODE)()
    PREPARED_GAME_INSTANCE.run_game()
