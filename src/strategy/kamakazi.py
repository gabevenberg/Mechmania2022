from game.game_state import GameState
import game.character_class

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy
from strategy.utils import StartPosEnum
import strategy.utils as utils

class Kamakazi(Strategy):

    def __init__(self):
        self.start_pos = -1
        self.start_positions = [(0,0), (9, 0), (0, 9), (9, 9)]

    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.ARCHER

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        curr_pos = (game_state.player_state_list[my_player_index].position.x,  game_state.player_state_list[my_player_index].position.y)

        self.start_pos = utils.get_start_pos(my_player_index)

        # Keep player at spawn if they have more than 5 gold and are located at spawn and dont already have an item.
        if (game_state.player_state_list[my_player_index].gold >= 8
            and (curr_pos[0], curr_pos[1]) in self.start_positions
            and game_state.player_state_list[my_player_index].item==Item.NONE
            ):
            return  game_state.player_state_list[my_player_index].position

        pos_to_move = self.go_to_middle(curr_pos)
        game_state.player_state_list[my_player_index].position.x = pos_to_move[0]
        game_state.player_state_list[my_player_index].position.y = pos_to_move[1]

        return game_state.player_state_list[my_player_index].position

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        target_list = [0,1,2,3]
        target_list.remove(my_player_index)
        our_pos = (game_state.player_state_list[my_player_index].position.x,  game_state.player_state_list[my_player_index].position.y)
        attack_range = game_state.player_state_list[my_player_index].stat_set.range
        goals=((4,4),(4,5),(5,4),(5,5))

        #immediately filters out all targets not in range.
        for enemy in target_list:
            enemy_pos = (game_state.player_state_list[enemy].position.x, game_state.player_state_list[enemy].position.y)
            if not utils.enemy_in_attack_range(our_pos, enemy_pos, attack_range):
                target_list.remove(enemy)
        if len(target_list)==0:
            return my_player_index

        who_killable = utils.who_killable(game_state, target_list, my_player_index)
        if len(who_killable)>0:
            target= max(who_killable, key=lambda x:x['score'])
            return target['index']
        who_on_goal=utils.who_on_goal(game_state, goals, target_list)
        if len(who_on_goal)>0:
            target= max(who_on_goal, key=lambda x:x['score'])
            return target['index']
        return max(target_list, key=lambda x:game_state.player_state_list[x].score)

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        my_pos = (game_state.player_state_list[my_player_index].position.x,game_state.player_state_list[my_player_index].position.y) 
        if my_pos == (0,0) or my_pos == (0,9) or my_pos == (9,0) or my_pos == (9,9):
            if (game_state.player_state_list[my_player_index].gold >= 5):
                return Item.SHIELD
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        goal = ((4,4),(5,4),(4,5),(5,5))
        curr_pos = (game_state.player_state_list[my_player_index].position.x, game_state.player_state_list[my_player_index].position.y)
        if game_state.player_state_list[my_player_index].item == Item.SHIELD:
            if curr_pos not in self.start_positions and curr_pos not in goal:
                 return True

        return False

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
