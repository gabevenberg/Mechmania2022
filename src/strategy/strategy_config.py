
from strategy.battle_archer import BattleArcher
from strategy.kamakazi import Kamakazi
from strategy.starter_strategy import StarterStrategy
from strategy.strategy import Strategy
from strategy.dumb_knight import DumbKnight
from strategy.hunting_knight import HuntingKnight
from strategy.kamikazi_wiz import KamakaziWizard
import random import choice
"""Return the strategy that your bot should use.

:param playerIndex: A player index that can be used if necessary.

:returns: A Strategy object.
"""
def get_strategy(player_index: int) -> Strategy:  
  
  return choice([DumbKnight(), Kamakazi()])
