from Matchmaster import Matchmaster
import itertools
import os
import os.path
import sys
import traceback
from collections import defaultdict
from Player import InvalidActionError, Player

class Gamemaster():
    def __init__(self, iterations):
        self.players = {}
        self.player_ids = []
        self.matches = []
        self.overall_points = defaultdict(int)
        self.iterations = iterations
        self.match_results = []

    def add_player(self, player_id, source_code):
        self.players[player_id] = Player(player_id=player_id, source_code=source_code)
        self.player_ids.append(int(player_id))

    def generate_matches(self):
        combinations = itertools.combinations(self.player_ids, 2)
        for pair in combinations:
            self.matches.append(pair)
        self.matches = self.matches * 1

    def start_tournament(self):
        for match in self.matches:
            # print '----- Match between ', match, ' begins -----'
            matchmaster = self.start_match(match)

            points = matchmaster.get_result()
            # print points
            outcome = zip(match, points)
            # print outcome
            for player_id, pts in outcome:
                self.overall_points[player_id] += pts
            # print 'The Score was ', outcome
            # print '----- Match between ', match, ' ended -----'

            self.match_results.append(matchmaster.get_match_data())

    def start_match(self, match):
        matchmaster = Matchmaster(player_1=self.players[match[0]],
                                  player_2=self.players[match[1]],
                                  iterations=self.iterations)
        # try:
        matchmaster.start_match()
        # except InvalidActionError as e:
        #     self.overall_points[e.player_id] += 1000
        #     print e.player_id, 'returned an invalid action!'
        # except Exception as e:
        #     self.handle_match_error(match)

        return matchmaster

    # def handle_match_error(self, match):
    #     tb = sys.exc_info()[2]
    #     stack = traceback.extract_tb(tb)
    #     crasher = None
    #     for s in stack:
    #         print s
    #         if s[2] == 'decide':
    #             crasher = s
    #     if crasher:
    #         crasher = os.path.splitext(os.path.basename(crasher[0]))[0]
    #         print crasher, ' Crashed!'
    #         player_id = int(crasher)
    #         self.overall_points[player_id] += 1000
    #     else:
    #         print "Match crashed, but unable to determine crasher"

    def get_overall_points(self):
        return self.overall_points

    def get_winner(self):
        return min(self.overall_points, key=lambda k: self.overall_points[k])

    def get_match_results(self):
        return self.match_results