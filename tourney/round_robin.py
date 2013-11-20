# http://www.lifl.fr/IPD/ipd.html.en

from Player import Player
from Gamemaster import Gamemaster
import random

def round_robin(iterations=None, players=[]):
    # Must have 2 or more players to play round robin!
    if len(players) >= 2:
        if iterations is None:
            iterations = random.randint(100, 150)

        gm = Gamemaster(iterations=iterations)

        for player in players:
            gm.add_player(*player)

        gm.generate_matches()

        gm.start_tournament()

        # d = gm.get_overall_points()
        # for v in sorted(d, key=d.get, reverse=False):
        #     print v, d[v]

        output = {
            'points': gm.get_overall_points(),
            'winner': gm.get_winner(),
            'results': gm.get_match_results()
        }

    else:
        output = {
            'points': {},
            'winner': None,
            'results': []
        }

    return output

if __name__ == '__main__':

    players = [
        [1, 'def decide(context): return context.iterationstest'],
        [2, 'def decide(context): return "C"']
    ]

    print round_robin(iterations=random.randint(100, 150), players=players)