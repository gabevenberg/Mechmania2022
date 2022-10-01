from game.game_state import GameState
import game.character_class
import logging

from game.item import Item
from game.position import Position
from strategy.strategy import Strategy
import math

class StartPosEnum():
    top_left = 1
    top_right = 2
    bottom_left = 3
    bottom_right = 4

def target_in_attack_range(target_pos, attacker_pos, attack_range):
    if abs(target_pos[0] - attacker_pos[0]) <= attack_range and abs(target_pos[1] - attacker_pos[1]) <= attack_range:
        return True
    return False

def enemy_is_killable(us, enemy, game_state:GameState):
    return game_state.player_state_list[enemy].health < get_damage(us, enemy, game_state)

def get_damage(attacker, target, game_state:GameState):
    if game_state.player_state_list[target].item==Item.PROCRUSTEAN_IRON:
        return 4
    return game_state.player_state_list[attacker].stat_set.damage


def get_start_pos(player_index):
    start_pos = StartPosEnum.top_left
    if player_index == 0:
        start_pos = StartPosEnum.top_left
    elif player_index == 1:
        start_pos = StartPosEnum.top_right
    elif player_index == 3:
        start_pos = StartPosEnum.bottom_left
    elif player_index == 2:
        start_pos = StartPosEnum.bottom_right
    # logging.info(f'{player_index=}, {start_pos=}')
    return start_pos

def who_on_goal(game_state, goals, indexes):
    enemies = []
    enemy_info = []
    for i in indexes:
        enemies.append((game_state.player_state_list[i], i))
    for enemy in enemies:
        enemy_pos = (enemy[0].position.x, enemy[0].position.y)
        if enemy_pos in goals:
            enemy_info.append({'position':enemy_pos, 'health':enemy[0].health, 'score':enemy[0].score, 'index':enemy[1]})
    return enemy_info

def who_killable(game_state, indexes, us):
    enemies = []
    enemy_info = []
    for i in indexes:
        if enemy_is_killable(us, i, game_state):
            enemies.append((game_state.player_state_list[i], i))
    for enemy in enemies:
        enemy_info.append({'index':enemy[1], 'health':enemy[0].health, 'score':enemy[0].score})
    return enemy_info

def can_attack_us_after_move(game_state:GameState, us, enemy)->bool:
    our_pos = (game_state.player_state_list[us].position.x,  game_state.player_state_list[us].position.y)
    enemy_pos = (game_state.player_state_list[enemy].position.x, game_state.player_state_list[enemy].position.y)
    enemy_range=game_state.player_state_list[enemy].stat_set.range
    enemy_movement=game_state.player_state_list[enemy].stat_set.speed
    #composing the area covered by a manhattan movement with the area covered by chebychev distance is communitave, it turns out.
    magic_number=manhattan_distance(our_pos, enemy_pos)+chebyshev_distance(our_pos, enemy_pos)
    return magic_number<=enemy_range+enemy_movement

def manhattan_distance(p1, p2) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def chebyshev_distance(p1, p2) -> int:
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
