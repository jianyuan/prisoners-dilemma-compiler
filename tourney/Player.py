from collections import namedtuple
# from import_file import import_file
import Game
# from asteval import Interpreter
from collections import defaultdict
from tempfile import NamedTemporaryFile
from import_file import import_file

class Player():
    """Initialize a player"""
    def __init__(self, player_id, source_code):
        self.player_id = player_id
        self.source_code = source_code
        self.interpreter = None
        self.forget()

    def forget(self):
        errors = []
        # tmp_file = NamedTemporaryFile()
        f = open(str(self.player_id) + '.py', 'w')
        try:
            f.write(self.source_code)
            f.close()

            self.interpreter = import_file(str(self.player_id) + '.py')
            # sp = Popen(['pylint', '--errors-only', '--msg-template="{line}: {msg} ({symbol})"', '--disable=E0602', tmp_file.name], stdout=PIPE, stderr=PIPE)
            # out, err = sp.communicate()

            # from pylint import epylint as lint
            # cmd = "%s --msg-template='{line:3d},{column:2d}: {msg} ({symbol})'" % (tmp_file.name,)
            # print cmd
            # (stdout, stderr) = lint.py_run(cmd, True)
            # out = stdout.read()
            # err = stderr.read()

            # if out:
            #     # errors.append(out)
            #     errors.append('\n'.join(out.split('\n')[1:])) # Remove first line of stdout
            # if err:
            #     errors.append(err)
        except Exception as e:
            errors.append(str(e))

        print errors

        # self.interpreter = Interpreter()
        # self.interpreter(self.source_code)

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
            # decision = self.interpreter.symtable['decide'](self.opponent_moves, self.my_moves)
            decision = self.interpreter.decide(self.opponent_moves)
        except Exception as e:
            self.log(str(e))
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