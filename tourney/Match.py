from collections import namedtuple
import Game

class Match():
    def __init__(self, player_1, player_2, _iterations):
        self.player_1 = player_1
        self.player_2 = player_2
        self._iterations = _iterations
        self.points = [0] * 2
    
    def start(self):
        results = []

        for iteration_count in range(self._iterations):
            move_1 = self.player_1.get_move()
            move_2 = self.player_2.get_move()
            if Game.is_communication_failed(): move_1 = Game.opposite_move_from(move_1)
            if Game.is_communication_failed(): move_2 = Game.opposite_move_from(move_2)

            points_1, points_2 = Game.get_points(move_1, move_2)

            self.points[0] += points_1
            self.points[1] += points_2

            results.append('(' + str(points_1) + ', ' + str(points_2) + ')')

            self.player_1.remember(opponent_move=move_2, my_move=move_1, opponent_points=points_2, my_points=points_1)
            self.player_2.remember(opponent_move=move_1, my_move=move_2, opponent_points=points_1, my_points=points_2)

        # print ', '.join(results)

    def get_result(self):
        return self.points