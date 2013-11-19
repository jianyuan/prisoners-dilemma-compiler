import Game
from Player import Player, CrashedError, InvalidActionError
import sys
import traceback

class Matchmaster():
    def __init__(self, player_1, player_2, iterations):
        self.iterations = iterations
        self.player_1 = player_1
        self.player_2 = player_2
        self.points = [0] * 2
        self.crashed = False
        self.crashers = []
        self.moves = []
    
    def start_match(self):
        # Reset player history
        self.player_1.forget()
        self.player_2.forget()

        for iteration_count in range(self.iterations):
            move_1, move_2 = None, None

            try:
                move_1 = self.player_1.get_move()
                move_2 = self.player_2.get_move()
            except CrashedError as e:
                self.points[self.get_player_key_from_player_id(e.player_id)] += Game.POINTS_FOR_CRASHING
                self.crashed = True
                self.crashers.append({'iteration': iteration_count, 'player_id': e.player_id, 'message': e.message})
                continue
            # except InvalidActionError as e:
            #     self.points[self.get_player_key_from_player_id(e.player_id)] += Game.POINTS_FOR_INVALID_ACTION
            #     self.crashed = True
            #     self.crashers.append({'iteration': iteration_count, 'player_id': e.player_id, 'message': 'did not return a correct response'})
            #     continue

            if Game.is_communication_failed():
                move_1 = Game.opposite_move_from(move_1)
            if Game.is_communication_failed():
                move_2 = Game.opposite_move_from(move_2)

            self.moves.append([move_1, move_2])

            points_1, points_2 = Game.get_points(move_1, move_2)

            self.points[0] += points_1
            self.points[1] += points_2

            # print '(' + str(points_1) + ', ' + str(points_2) + ')'

            self.player_1.remember(opponent_move=move_2, my_move=move_1, opponent_points=points_2, my_points=points_1)
            self.player_2.remember(opponent_move=move_1, my_move=move_2, opponent_points=points_1, my_points=points_2)

        # print ', '.join(results)

    def get_points(self):
        return self.points

    def get_moves(self):
        return self.moves

    def get_player_key_from_player_id(self, player_id):
        if self.player_1.player_id == player_id:
            return 0
        else:
            return 1

    def get_match_data(self):
        return {
            'players': [self.player_1.player_id, self.player_2.player_id],
            'points': self.get_points(),
            'iterations': self.iterations,
            'crashed': self.crashed,
            'crashers': self.crashers,
            'moves': self.get_moves(),
        }
