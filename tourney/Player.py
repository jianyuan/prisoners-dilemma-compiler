from collections import namedtuple
# from import_file import import_file
import Game
from asteval import Interpreter
from collections import defaultdict


class Player():
    """Initialize a player"""
    def __init__(self, player_id, source_code):
        self.player_id = player_id

        self.interpreter = Interpreter()
        self.interpreter(source_code)

        self.forget()

    def forget(self):
        self.iteration_count = 0
        self.opponent_moves = []
        self.opponent_points = 0
        self.my_moves = []
        self.my_points = 0
        self.logs = defaultdict(list)

    def get_move(self):
        decision = None

        try:
            # if 'decide' in self.interpreter.symtable:
            decision = self.interpreter.symtable['decide'](self.opponent_moves, self.my_moves)
        except Exception as e:
            self.log('Crashed')
        finally:
            decision = str(decision).upper()

        if decision not in Game.VALID_MOVES:
            self.log('Invalid move')
            return None

        return decision

    def remember(self, opponent_move, my_move, opponent_points, my_points):
        self.iteration_count += 1
        self.opponent_moves.append(opponent_move)
        self.opponent_points += opponent_points
        self.my_moves.append(my_move)
        self.my_points += my_points

    def log(self, message):
        self.logs[self.iteration_count].append(message)