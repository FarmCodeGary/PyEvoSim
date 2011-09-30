# Simulation configuration

BOARD_WIDTH = 60  # The width of the board in tiles.
BOARD_HEIGHT = 25 # The height of the board in tiles.

INITIAL_DNA = "DWIAFEHR"
# INITIAL_DNA is the DNA sequence with which all monsters begin.
# Note that certain beginning DNA sequences are doomed to fail, specifically
# any that prioritize Dividing below Wandering or Idling.

INITIAL_HP = 200  # The number of health points the starting monsters get.
INITIAL_COLOR = (127,127,127) # The color of all starting monsters, in RGB format.

MONSTER_DENSITY = 0.05 # Chances of a given space having a monster initially.
FOOD_DENSITY = 1.0    # Chances of a space having food initially (assuming it doesn't have a monster).

MAX_NUM_MONSTERS = BOARD_WIDTH*BOARD_HEIGHT # Maximum number of monsters to start with.
MAX_NUM_FOOD = BOARD_WIDTH*BOARD_HEIGHT     # Maximum amount of food to start with.
# The above two numbers can be used to limit the maximum number of monsters or
# food created at the start of the simulation. If this setting is used, the
# monsters/food created will tend to be toward the left-hand side of the board.

FOOD_HP_INCREASE = 130  # The amount by which food increases a monster's HP.
REST_HP_INCREASE = 15   # The amount by which resting increases a monster's HP.
HEAL_HP_INCREASE = 21   # The amount by which healing increases a monster's HP.
REST_MAX_HP = 200       # The maximum HP beyond which resting will not work.
ATTACK_HP_DECREASE = 50 # The amount by which attacking decreases a monster's HP.
DIVIDE_MIN_HP = 75      # The minimum HP necessary for a monster to divide.
HP_LOSS_PER_TURN = 20   # The amount of HP a monster will lose in a turn.

MUTATION_RATE = 0.2
# The probability of offspring having a mutation (should be between 0.0 and 1.0).

COLOR_CHANGE_OFFSET = 30
# The amount by which a mutated offspring's color will change.
# (It will randomly choose one component of the RGB color representation and
# add or subtract this number to it, ensuring that the resulting number is still
# between 0 and 255.)
