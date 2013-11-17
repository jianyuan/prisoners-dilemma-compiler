import random
DEFECT = 'D'
COOPERATE = 'C'

VALID_MOVES = [DEFECT, COOPERATE]

POINTS_FOR_CRASHING = 1000
POINTS_FOR_INVALID_ACTION = 1000

# payoff matrix
results = {
    (DEFECT, DEFECT): (2, 2),
    (DEFECT, COOPERATE): (0, 3),
    (COOPERATE, DEFECT): (3, 0),
    (COOPERATE, COOPERATE): (1, 1)
    # (DEFECT, DEFECT): (1, 1),
    # (DEFECT, COOPERATE): (5, 0),
    # (COOPERATE, DEFECT): (0, 5),
    # (COOPERATE, COOPERATE): (3, 3)
}

def get_points(move_1, move_2):
    return results[(move_1), (move_2)]

def opposite_move_from(move):
    return (DEFECT if move == COOPERATE else COOPERATE)

def is_communication_failed():
    # return random.randint(0, 4) == 0
    return False
