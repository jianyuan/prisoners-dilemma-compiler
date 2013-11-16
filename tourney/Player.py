from collections import namedtuple
# from import_file import import_file
import Game
from asteval import Interpreter

MatchContext = namedtuple('MatchContext', 'iteration_count opponent_moves my_moves opponent_points my_points')

class PlayerException(Exception):
    def __init__(self, player_id):
        self.player_id = player_id
    def __str__(self):
        return repr(self.player_id)    

class CrashedError(PlayerException):
    pass
class InvalidActionError(PlayerException):
    pass

class Player():
    """Initialize a player"""
    def __init__(self, player_id, source_code):
        self.player_id = player_id

        self.interpreter = Interpreter()
        self.interpreter(source_code)

        self.forget()

        if 'initialize' in self.interpreter.symtable:
            self.interpreter.symtable['initialize'](self.get_match_context())

    def get_move(self):
        decision = None

        try:
            if 'decide' in self.interpreter.symtable:
                decision = self.interpreter.symtable['decide'](self.get_match_context())
        except Exception:
            raise CrashedError(self.player_id)

        if decision not in Game.VALID_MOVES:
            raise InvalidActionError(self.player_id)

        return decision

    def remember(self, opponent_move, my_move, opponent_points, my_points):
        self.context['iteration_count'] += 1
        self.context['opponent_moves'].append(opponent_move)
        self.context['my_moves'].append(my_move)
        self.context['opponent_points'] += opponent_points
        self.context['my_points'] += my_points

    def forget(self):
        self.context = {
            'iteration_count': 0,
            'opponent_moves': [],
            'my_moves': [],
            'opponent_points': 0,
            'my_points': 0
        }

    def get_match_context(self):
        return MatchContext(**self.context)