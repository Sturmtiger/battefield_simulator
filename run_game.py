"""
This module runs the game
"""

from battlefield import Game


if __name__ == '__main__':
    modes = ['create_new_structure', 'load_json_structure']
    print('Choose your option:',
          '\t1. New game',
          '\t2. Replay last game', sep='\n')
    mode_index = int(input('Enter the number of chosen option: ')) - 1
    chosen_mode = modes[mode_index]
    x = getattr(Game, chosen_mode)()
    x.run_game()
