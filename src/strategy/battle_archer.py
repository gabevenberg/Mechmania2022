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

class BattleArcher(Strategy):

    def __init__(self):
        self.start_pos = -1
        self.start_positions = [(0,0), (9, 0), (0, 9), (9, 9)]

    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.ARCHER

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        curr_pos = (game_state.player_state_list[my_player_index].position.x,  game_state.player_state_list[my_player_index].position.y)

        self.get_start_pos(curr_pos)

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
            if not self.enemy_in_attack_range(our_pos, enemy_pos, attack_range):
                target_list.remove(enemy)
        if len(target_list)==0:
            return my_player_index

        who_killable = self.who_killable(game_state, target_list, my_player_index)
        if len(who_killable)>0:
            target= max(who_killable, key=lambda x:x['score'])
            return target['index']
        who_on_goal=self.who_on_goal(game_state, goals, target_list)
        if len(who_on_goal)>0:
            target= max(who_on_goal, key=lambda x:x['score'])
            return target['index']
        return target_list[0]

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        my_pos = (game_state.player_state_list[my_player_index].position.x,game_state.player_state_list[my_player_index].position.y) 
        if my_pos == (0,0) or my_pos == (0,9) or my_pos == (9,0) or my_pos == (9,9):
            if (game_state.player_state_list[my_player_index].gold >= 8):
                return Item.RALLY_BANNER
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        goal = ((4,4),(5,4),(4,5),(5,5))
        curr_pos = (game_state.player_state_list[my_player_index].position.x, game_state.player_state_list[my_player_index].position.y)
        if game_state.player_state_list[my_player_index].item == Item.SHIELD:
            if curr_pos not in self.start_positions and curr_pos not in goal:
                 return True

        return False
 
    def enemy_in_attack_range(self, enemy_pos, our_pos, attack_range):
        if abs(enemy_pos[0] - our_pos[0]) <= attack_range and abs(enemy_pos[1] - our_pos[1]) <= attack_range:
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

    def who_on_goal(self, game_state, goals, indexes):
        enemies = []
        enemy_info = []
        for i in indexes:
            enemies.append((game_state.player_state_list[i], i))
        for enemy in enemies:
            enemy_pos = (enemy.position[0].x, enemy[0].position.y)
            if enemy_pos in goals:
                enemy_info.append({'position':enemy_pos, 'health':enemy[0].health, 'score':enemy[0].score})
        return enemy_info

    def who_killable(self, game_state, indexes, us):
        enemies = []
        enemy_info = []
        for i in indexes:
            if self.enemy_is_killable(us, i, game_state):
                enemies.append((game_state.player_state_list[i], i))
        for enemy in enemies:
            enemy_info.append({'index':enemy[1], 'health':enemy[0].health, 'score':enemy[0].score})
        return enemy_info
