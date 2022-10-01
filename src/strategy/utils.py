from game.game_state import GameState
import game.character_class
import logging

from game.item import Item
from game.position import Position
from strategy.strategy import Strategy

class StartPosEnum():
    top_left = 1
    top_right = 2
    bottom_left = 3
    bottom_right = 4

def enemy_in_attack_range(enemy_pos, our_pos, attack_range):
    if abs(enemy_pos[0] - our_pos[0]) <= attack_range and abs(enemy_pos[1] - our_pos[1]) <= attack_range:
        return True
    return False

def enemy_is_killable(us, enemy, game_state:GameState):
    return game_state.player_state_list[enemy].health < get_damage(us, enemy, game_state)

def get_damage(us, enemy, game_state:GameState):
    if game_state.player_state_list[enemy].item==Item.PROCRUSTEAN_IRON:
        return 4
    return game_state.player_state_list[us].stat_set.damage


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


def go_to_middle(curr_pos, start_pos):
    if start_pos == StartPosEnum.top_left:
        if curr_pos[0] < 4:
            return (curr_pos[0] + 2, curr_pos[1] + 2)
    if start_pos == StartPosEnum.top_right:
        if curr_pos[0] > 6:
            return (curr_pos[0] - 2, curr_pos[1] + 2)
    if start_pos == StartPosEnum.bottom_left:
        if curr_pos[0] < 4:
            return (curr_pos[0] + 2, curr_pos[1] - 2)
    if start_pos == StartPosEnum.bottom_right:
        if curr_pos[0] > 6:
            return (curr_pos[0] - 2, curr_pos[1] - 2)

    return curr_pos

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
