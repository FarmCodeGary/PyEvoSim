======================
PyEvoSim (Version 0.1)
======================
evolution simulator written in Python and Pygame
------------------------------------------------

ABOUT PYEVOSIM
--------------
PyEvoSim is an "evolution simulator". It simulates the evolution of monsters, with the goal of making evolution observable and fun.


REQUIREMENTS
------------
PyEvoSim requires Python 2.7 and Pygame.

http://www.python.org

http://www.pygame.org


USING THE PROGRAM
-----------------
- To start PyEvoSim, run main.py (in the src folder) in a console window. (Typically the command will be "python main.py".) Alternatively, if using Linux, you can run pyevosim.sh (in the project's root folder).

- To run one step of the simulation, press the SPACEBAR.

- To start/stop the simulation, press ENTER.

- To restart the simulation (and reload the config files) press F2.

- To see info about a monster (including its DNA) left-click on it while the simulation is paused. The information will be printed in the console.

- To "follow" a monster, right-click on it while the simulation is paused. (This will also give the monster a random name.)

- To quit, press ESCAPE or close the pygame window.

- To change the parameters of the simulation (such as the mutation rate) open config.py in a text editor and make desired changes. They will be reflected when the simulation is restarted.


ABOUT THE SIMULATION
--------------------
The first version of PyEvoSim (0.1) has a very rudimentary evolution simulation, in which monsters only evolve better priorities. (Evolution of physiology is not simulated at all.)

The simulation takes place on a grid populated with monsters and food. Initially, all monsters are the same color.

Each monster has a value called HP (health points). Each turn, its HP decreases. When its HP reaches zero, the monster dies, and is replaced on the board by food.

In one step of the simulation, each monster is allowed to perform one action. It chooses its action based on its DNA.

Monster DNA is essentially an ordered list of actions. An example would be [divide,attack,wander,eat,flee,idle,heal,rest], which would be written as the "DNA string" DAWEFIHR.

A monster will always choose the first applicable action on the list. An action is "applicable" if its preconditions are met. For instance, the "attack" action has the precondition that there is at least one adjacent monster.

One action is the "divide" action, in which a monster uses half its HP to create a new monster in an adjacent space. The new monster will have the same DNA, except with a chance of mutation.

When DNA mutates, two adjacent actions on the list are swapped. So, the DNA DWIRFAEH could mutate and become DWRIFAEH (if "idle" and "rest" switch places). Mutated offspring will also have a slightly different color. (Color has no effect on the simulation itself - it's only for aesthetics.)

Many parameters of the simulation can be set via changes to config.py.


FUTURE GOALS
------------
- Improve graphics and user interface

- Make more robust DNA format, including some kind of physiological aspect


