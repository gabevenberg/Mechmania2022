from random import Random
from game.game_state import GameState
import game.character_class

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy

class StartPosEnum():
    top_left = 1
    top_right = 2
    bottom_left = 3
    bottom_right = 4

class DumbKnight(Strategy):

    def __init__(self):
        self.start_pos = -1

    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.KNIGHT

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        self.get_start_pos((game_state.player_state_list[my_player_index].position.x,  game_state.player_state_list[my_player_index].position.y))

        pos_to_move = self.go_to_middle((game_state.player_state_list[my_player_index].position.x,  game_state.player_state_list[my_player_index].position.y))
        game_state.player_state_list[my_player_index].position.x = pos_to_move[0]
        game_state.player_state_list[my_player_index].position.y = pos_to_move[1]

        return game_state.player_state_list[my_player_index].position

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        return Random().randint(0, 3)

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        my_pos = (game_state.player_state_list[my_player_index].position.x,game_state.player_state_list[my_player_index].position.y) 
        if my_pos == (0,0) or my_pos == (0,9) or my_pos == (9,0) or my_pos == (9,9):
            if game_state.player_state_list[my_player_index].gold >= 5:
                return Item.SHIELD
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False


    def get_start_pos(self, curr_pos):
        if curr_pos == (0, 0):
            self.start_pos = StartPosEnum.top_left
        elif curr_pos == (9, 0):
            self.start_pos = StartPosEnum.top_right
        elif curr_pos == (0, 9):
            self.start_pos = StartPosEnum.bottom_left
        elif curr_pos == (9, 9):
            self.start_pos = StartPosEnum.bottom_right
    

    def go_to_middle(self, curr_pos):
        if self.start_pos == StartPosEnum.top_left:
            if curr_pos[0] < 4:
                return (curr_pos[0] + 2, curr_pos[1])
            elif curr_pos[1] < 4:
                return (curr_pos[0], curr_pos[1] + 2)

        if self.start_pos == StartPosEnum.top_right:
            if curr_pos[0] > 6:
                return (curr_pos[0] - 2, curr_pos[1])
            elif curr_pos[1] < 4:
                return (curr_pos[0], curr_pos[1] + 2)

        if self.start_pos == StartPosEnum.bottom_left:
            if curr_pos[0] < 4:
                return (curr_pos[0] + 2, curr_pos[1])
            elif curr_pos[1] > 6:
                return (curr_pos[0], curr_pos[1] - 2)

        if self.start_pos == StartPosEnum.bottom_right:
            if curr_pos[0] > 6:
                return (curr_pos[0] - 2, curr_pos[1])
            elif curr_pos[1] > 6:
                return (curr_pos[0], curr_pos[1] - 2)

        return curr_pos
