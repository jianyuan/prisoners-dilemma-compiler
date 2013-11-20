import Game
from Player import Player
import sys
import traceback

class Matchmaster():
    def __init__(self, player_1, player_2, iterations):
        self.iterations = iterations
        self.player_1 = player_1
        self.player_2 = player_2
        self.points = [0] * 2
        self.moves = []
        self.move_points = []
    
    def start_match(self):
        # Reset player history
        self.player_1.forget()
        self.player_2.forget()

        for iteration_count in range(self.iterations):
            move_1 = self.player_1.get_move()
            move_2 = self.player_2.get_move()

            if Game.is_communication_failed():
                move_1 = Game.opposite_move_from(move_1)
            if Game.is_communication_failed():
                move_2 = Game.opposite_move_from(move_2)

            self.moves.append([move_1, move_2])

            points_1, points_2 = Game.get_points(move_1, move_2)

            self.move_points.append([points_1, points_2])

            self.points[0] += points_1
            self.points[1] += points_2

            self.player_1.remember(opponent_move=move_2, my_move=move_1, opponent_points=points_2, my_points=points_1)
            self.player_2.remember(opponent_move=move_1, my_move=move_2, opponent_points=points_1, my_points=points_2)

    def get_match_data(self):
        return {
            'players': [self.player_1.player_id, self.player_2.player_id],
            'points': self.points,
            'iterations': self.iterations,
            'moves': self.moves,
            'move_points': self.move_points,
            'logs': [self.player_1.logs, self.player_2.logs]
        }
