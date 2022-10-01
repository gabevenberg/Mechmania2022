from random import Random
from game.game_state import GameState
import game.character_class

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy

class Kamakazi(Strategy):
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.ARCHER

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        return game_state.player_state_list[my_player_index].position

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        list = [0,1,2,3]
        list.remove(my_player_index)
        for enemy in list:
            if abs(game_state.player_state_list[my_player_index].position.x - game_state.player_state_list[enemy].position.x) <4 and abs(game_state.player_state_list[my_player_index].position.y - game_state.player_state_list[enemy].position.y) <4:
                return enemy
                
        return list[Random().randint(0, 2)]

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False