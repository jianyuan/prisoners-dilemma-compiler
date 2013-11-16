# http://www.lifl.fr/IPD/ipd.html.en

from Player import Player
from Gamemaster import Gamemaster
import random

gm = Gamemaster(iterations=random.randint(100, 150))

gm.add_player(1, 'def decide(): return "D"')
gm.add_player(2, 'def decide(): return "C"')

gm.generate_matches()

gm.start_tournament()

d = gm.get_overall_points()
for v in sorted(d, key=d.get, reverse=False):
  print v, d[v]

winner = gm.get_winner()
print 'The winner is ', winner