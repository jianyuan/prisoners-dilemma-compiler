import random

DEFECT = 'D'
COOPERATE = 'C'
OTHER = None

VALID_MOVES = [DEFECT, COOPERATE]

# payoff matrix
results = {
    # (DEFECT, DEFECT): (2, 2),
    # (DEFECT, COOPERATE): (0, 3),
    # (COOPERATE, DEFECT): (3, 0),
    # (COOPERATE, COOPERATE): (1, 1)

    # (DEFECT, DEFECT): (1, 1),
    # (DEFECT, COOPERATE): (5, 0),
    # (COOPERATE, DEFECT): (0, 5),
    # (COOPERATE, COOPERATE): (3, 3)

    # Scoring from: http://lesswrong.com/lw/hmx/prisoners_dilemma_with_visible_source_code/
    (COOPERATE, COOPERATE): (2, 2),
    (COOPERATE, DEFECT): (0, 3),
    (COOPERATE, OTHER): (0, 2),
    (DEFECT, COOPERATE): (3, 0),
    (DEFECT, DEFECT): (1, 1),
    (DEFECT, OTHER): (1, 0),
    (OTHER, COOPERATE): (2, 0),
    (OTHER, DEFECT): (0, 1),
    (OTHER, OTHER): (0, 0)
}

def get_points(move_1, move_2):
    return results[(move_1), (move_2)]

def opposite_move_from(move):
    if move in VALID_MOVES:
        return (DEFECT if move == COOPERATE else COOPERATE)
    else:
        return move

def is_communication_failed():
    # return random.randint(0, 4) == 0
    return False
