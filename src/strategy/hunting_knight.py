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

class HuntingKnight(Strategy):

    def __init__(self):
        self.start_pos = -1
        self.start_positions = [(0,0), (9, 0), (0, 9), (9, 9)]

    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.ARCHER

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        curr_pos = (game_state.player_state_list[my_player_index].position.x,  game_state.player_state_list[my_player_index].position.y)

        self.get_start_pos(curr_pos)

        # Keep player at spawn if they have more than 5 gold and are located at spawn.
        if game_state.player_state_list[my_player_index].gold >= 8 and (curr_pos[0], curr_pos[1]) in self.start_positions:
            return  game_state.player_state_list[my_player_index].position

        pos_to_move = self.go_to_middle(curr_pos)
        game_state.player_state_list[my_player_index].position.x = pos_to_move[0]
        game_state.player_state_list[my_player_index].position.y = pos_to_move[1]

        return game_state.player_state_list[my_player_index].position

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        list = [0,1,2,3]
        list.remove(my_player_index)
        for enemy in list:
            if abs(game_state.player_state_list[my_player_index].position.x - game_state.player_state_list[enemy].position.x) <2 and abs(game_state.player_state_list[my_player_index].position.y - game_state.player_state_list[enemy].position.y) <2:
                return enemy
                
        return list[Random().randint(0, 2)]

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        my_pos = (game_state.player_state_list[my_player_index].position.x,game_state.player_state_list[my_player_index].position.y) 
        if my_pos == (0,0) or my_pos == (0,9) or my_pos == (9,0) or my_pos == (9,9):
            if game_state.player_state_list[my_player_index].gold >= 5:
                return Item.SHIELD
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        my_pos = (game_state.player_state_list[my_player_index].position.x,game_state.player_state_list[my_player_index].position.y) 
        goal = ((4,4),(5,4),(4,5),(5,5))
        curr_pos = (game_state.player_state_list[my_player_index].position.x, game_state.player_state_list[my_player_index].position.y)
        if game_state.player_state_list[my_player_index].item == Item.SHIELD:
            if curr_pos not in self.start_positions and curr_pos not in goal:
                return True
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
                return (curr_pos[0] + 2, curr_pos[1] + 2)

        if self.start_pos == StartPosEnum.top_right:
            if curr_pos[0] > 6:
                return (curr_pos[0] - 2, curr_pos[1] + 2)

        if self.start_pos == StartPosEnum.bottom_left:
            if curr_pos[0] < 4:
                return (curr_pos[0] + 2, curr_pos[1] - 2)

        if self.start_pos == StartPosEnum.bottom_right:
            if curr_pos[0] > 6:
                return (curr_pos[0] - 2, curr_pos[1] - 2)

        return curr_pos

