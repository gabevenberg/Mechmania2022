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

class Kamakazi(Strategy):

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
        target_list = [0,1,2,3]
        target_list.remove(my_player_index)
        our_pos = (game_state.player_state_list[my_player_index].position.x,  game_state.player_state_list[my_player_index].position.y)

        #immediately filters out all targets not in range.
        for enemy in target_list:
            enemy_pos = (game_state.player_state_list[enemy].position.x, game_state.player_state_list[enemy].position.y)
            if not self.enemy_in_attack_range(our_pos, enemy_pos):
                target_list.remove(enemy)
        if len(target_list)==0:
            return my_player_index

        lowest_health_enemy = 0
        lowest_knight_enemy = 0
        hunting_scope_enemy = 0
        for enemy in target_list:
            enemy_pos = (game_state.player_state_list[enemy].position.x, game_state.player_state_list[enemy].position.y)
            # if killable enemy is in range, kill it.
            if self.enemy_is_killable(my_player_index, enemy, game_state):
                return enemy
            # get Lowest health enemy in range
            if game_state.player_state_list[enemy].health < game_state.player_state_list[lowest_health_enemy].health and self.enemy_in_attack_range(our_pos, enemy_pos):
                lowest_health_enemy = enemy
            # get Lowest health knight in range
            if game_state.player_state_list[enemy].health < game_state.player_state_list[lowest_knight_enemy].health and game_state.player_state_list[enemy].character_class == game.character_class.CharacterClass.KNIGHT and self.enemy_in_attack_range(our_pos, enemy_pos):
                lowest_knight_enemy = enemy
            # get enemy using hunter scopes
            
            if game_state.player_state_list[enemy].item == Item.HUNTER_SCOPE and self.enemy_in_attack_range(enemy_pos, our_pos):
                hunting_scope_enemy = enemy
            
            # Free point if they are  a wizard/archer and we are a knight. No matter what we one shot and it's free points
            if game_state.player_state_list[enemy].character_class == game.character_class.CharacterClass.ARCHER or game_state.player_state_list[enemy].character_class == game.character_class.CharacterClass.WIZARD and self.enemy_in_attack_range(enemy_pos, our_pos):
                return enemy

            # To determine who to attack, change the index positions of 'final_attack_pos' and the return statement
            
            if hunting_scope_enemy is not None and game_state.player_state_list[lowest_health_enemy].health  >2:
                final_attack_pos = (game_state.player_state_list[hunting_scope_enemy].position.x, game_state.player_state_list[hunting_scope_enemy].position.y)
                if self.enemy_in_attack_range(final_attack_pos, our_pos):
                    return hunting_scope_enemy
            else:
                final_attack_pos = (game_state.player_state_list[lowest_health_enemy].position.x, game_state.player_state_list[lowest_health_enemy].position.y)
                if self.enemy_in_attack_range(final_attack_pos, our_pos):
                    return lowest_health_enemy

           
            # Random enemy in range if specified 
            if abs(game_state.player_state_list[my_player_index].position.x - game_state.player_state_list[enemy].position.x) <4 and abs(game_state.player_state_list[my_player_index].position.y - game_state.player_state_list[enemy].position.y) <4:
                return lowest_health_enemy
            return lowest_health_enemy
                
        return target_list[Random().randint(0, 2)]

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        my_pos = (game_state.player_state_list[my_player_index].position.x,game_state.player_state_list[my_player_index].position.y) 
        if my_pos == (0,0) or my_pos == (0,9) or my_pos == (9,0) or my_pos == (9,9):
            if game_state.player_state_list[my_player_index].gold >= 5:
                return Item.SHIELD
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        list = [0,1,2,3]
        list.remove(my_player_index)
        # my_pos = (game_state.player_state_list[my_player_index].position.x,game_state.player_state_list[my_player_index].position.y) 
        # for enemy in list:
        #     range_pos = (game_state.player_state_list[enemy].position.x, game_state.player_state_list[enemy].position.y)
        #     if self.enemy_in_attack_range(range_pos, my_pos):
        #         return True
        goal = ((4,4),(5,4),(4,5),(5,5))
        curr_pos = (game_state.player_state_list[my_player_index].position.x, game_state.player_state_list[my_player_index].position.y)
        if game_state.player_state_list[my_player_index].item == Item.SHIELD:
            if curr_pos not in self.start_positions and curr_pos not in goal:
                 return True

        return False
 
    def enemy_in_attack_range(self, enemy_pos, our_pos):
        if abs(enemy_pos[0] - our_pos[0]) < 2 and abs(enemy_pos[1] - our_pos[1]) < 2:
            return True
        return False

    def enemy_is_killable(self, us, enemy, game_state:GameState):
        return game_state.player_state_list[enemy].health < self.get_damage(us, enemy, game_state)

    def get_damage(self, us, enemy, game_state:GameState):
        damage=0
        if game_state.player_state_list[us].character_class==game.character_class.CharacterClass.KNIGHT:
            damage=6
        elif game_state.player_state_list[us].character_class==game.character_class.CharacterClass.WIZARD:
            damage=4
        elif game_state.player_state_list[us].character_class==game.character_class.CharacterClass.ARCHER:
            damage=2
        if game_state.player_state_list[enemy].item==Item.PROCRUSTEAN_IRON:
            damage=4
        return damage


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

