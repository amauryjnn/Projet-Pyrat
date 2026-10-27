# 🐀 PyRat Project

Computer science project of semester 5 (FISE 1A, IMT Atlantique): programming, in Python, a rat that moves through a maze to catch pieces of cheese, using graph theory and classic algorithms.

🏆 **Our competition player finished 5th in the PyRat tournament.**

Built by a team of three: **Amaury JANIN**, **CREPIN** and **SARETE**.

> Project description and sessions: <https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/index.html>

---

## Table of contents

- [The game](#the-game)
- [Repository content](#repository-content)
- [The players](#the-players)
- [The competition player](#the-competition-player)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [Tournament](#tournament)
- [Team organization](#team-organization)
- [Use of generative AI](#use-of-generative-ai)

---

## The game

[PyRat](https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/index.html) is a game for one or several players. The maze is a **graph**: cells are vertices and passages are edges. **Mud** cells are weighted edges: they take several turns to cross. The goal is to collect as much cheese as possible, in as few turns as possible.

The project is split into sessions, each one adding a difficulty:

| Session | Problem | Algorithms |
|---|---|---|
| 1 | Discovery, first random players | Random walks (`Random1` to `Random5`) |
| 2 | Catch **1 piece of cheese** | Breadth-first search (BFS) and depth-first search (DFS) |
| 3 | Catch **1 piece of cheese** with mud | Dijkstra (with a custom min-heap) |
| 4 | Catch **N pieces of cheese** | Traveling salesman problem (TSP) by exhaustive search |
| 5 | Catch N pieces of cheese **faster** | Greedy algorithms and heuristics |
| 6 | **Challenge an opponent** | Strategy against an opponent (game theory) |

## Repository content

```
.
├── players/   The players (one class per file, inheriting from pyrat.Player)
├── utils/     Reusable building blocks: MinHeap, Traversal, BFSTraversal, DFSTraversal
├── games/     Notebooks that run games and visualize and compare the players
├── test/      Unit tests (unittest, written in notebooks)
├── doc/       Documentation of the PyRat library (HTML, generated with pdoc)
└── *.zip      Archives of deliverables 1 and 2 handed in during the semester
```

## The players

All players are in [players/](players/) and inherit from `pyrat.Player` (methods `preprocessing`, `turn`, `postprocessing`).

| Player | Description |
|---|---|
| `Random1` … `Random5` | Increasingly clever random walks: random moves, wall avoidance, preference for unvisited cells, etc. |
| `BFS`, `DFS`, `DFS_recursive` | Single cheese: the path is computed in `preprocessing` by a breadth-first or depth-first search (a recursive DFS version is included). |
| `TraversalPlayer` | Generic player that uses either [BFSTraversal](utils/BFSTraversal.py) or [DFSTraversal](utils/DFSTraversal.py). |
| `Dijkstra` | Single cheese, weighted shortest path (handles mud) using the [MinHeap](utils/MinHeap.py), implemented without `heapq`. |
| `Exhaustive` | N cheeses: builds a **metagraph** (player + cheeses, edges = shortest paths), then solves the TSP by exhaustive search with pruning. Optimal, but factorial running time. |
| `Greedy` | N cheeses: same metagraph, but always visits the nearest cheese. The visiting order is computed only once. |
| `GreedyEachCheese` | Like `Greedy`, but the metagraph is recomputed each time a cheese is reached. |
| `GreedyEachTurn` | Like `GreedyEachCheese`, but the target is re-evaluated as soon as the targeted cheese disappears (for example, eaten by the opponent). |
| `GreedyTest` | Experimental variant: greedy with a few steps of look-ahead. |
| `CompetPlayer` | Our competition player (see below). |
| `TemplatePlayer` | Provided template to write a new player. |

**Complexities** (V vertices and E edges in the maze, N cheeses): a Dijkstra traversal costs O((V+E) log V), rebuilding a path costs O(V), and the greedy choice costs O(N). The exhaustive player explores up to N! visiting orders, hence the need for greedy methods on large games.

**Exhaustive vs. greedy comparison** ([games/compare_exhaustive_greedy.ipynb](games/compare_exhaustive_greedy.ipynb)): the greedy player needs slightly more turns than the exhaustive one, but it is much faster to compute.

## The competition player

[CompetPlayer](players/CompetPlayer.py) is designed for the tournament settings: a 25×20 maze with 41 pieces of cheese, mud, 3 s of preprocessing and 0.1 s per turn. The exhaustive player is unusable there, and only a fast algorithm fits in the time budget.

How it works:

1. **Metagraph**: the rat and all the cheeses are linked by their shortest paths (Dijkstra, stopped as soon as all cheeses are found).
2. **Greedy**: it heads for the nearest cheese and stores the sequence of actions to follow.
3. **Update**: when the target disappears or is reached, vanished cheeses are removed from the metagraph, distances from the current position are recomputed, and a new target is chosen.
4. **Cheese zones** (`get_zones`): a depth-limited BFS groups nearby cheeses into zones and counts the cheeses in each zone. This is computed in `preprocessing` and visualized in [games/visualize_CompetPlayer.ipynb](games/visualize_CompetPlayer.ipynb), but it is not yet used to choose the route. It is the main improvement path (visiting zone by zone instead of cheese by cheese).

## Installation

Requirements: Python ≥ 3.12 (the compiled files present were generated with 3.12) and the **PyRat** library, installed as described in [session 1](https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/session1/index.html) of the course. The PyRat documentation is also available offline in [doc/index.html](doc/index.html).

```bash
git clone https://github.com/amauryjnn/Projet-Pyrat.git
cd Projet-Pyrat
```

Python dependencies used by the code and the notebooks, in addition to PyRat:

```bash
pip install jupyter numpy matplotlib networkx scikit-learn
```

`networkx` and `scikit-learn` are only used for type-related imports in a few players (for example `CompetPlayer`), but they must be installed for those files to import.

## Usage

The notebooks use relative paths, so they must be **launched from the `games/` folder**.

```bash
cd games
jupyter notebook
```

Useful notebooks:

| Notebook | Purpose |
|---|---|
| `tutorial.ipynb`, `sample_game.ipynb` | Getting started with PyRat |
| `visualize_<Player>.ipynb` | Runs and displays a game with the given player |
| `compare_all_randoms.ipynb` | Compares the five random players |
| `compare_exhaustive_greedy.ipynb` | Compares speed and number of turns of the exhaustive and greedy players |
| `match_Greedy_GreedyEachTurn.ipynb` | Head-to-head match between greedy variants |
| `tournament.ipynb` | Provided tournament script (pools, then knockout phase) |

Minimal example, taken from `visualize_CompetPlayer.ipynb`:

```python
import sys, os
sys.path.append(os.path.join("..", "players"))

from pyrat import Game, GameMode
from CompetPlayer import CompetPlayer

game = Game(maze_width=25, maze_height=20, cell_percentage=80, wall_percentage=60,
            mud_percentage=20.0, mud_range=[4, 9], nb_cheese=41,
            preprocessing_time=3.0, turn_time=0.1, random_seed=42,
            game_mode=GameMode.SEQUENTIAL)
game.add_player(CompetPlayer())
stats = game.start()
```

## Tests

Unit tests use `unittest` and are written in notebooks in the [test/](test/) folder. Each notebook is run from `test/` (**Run All**) and ends with `unittest.main(...)`.

| Notebook | Tests |
|---|---|
| `tests_MinHeap.ipynb` | Adding, removing, replacing, and keys of various types |
| `tests_BFS.ipynb`, `tests_DFS.ipynb` | Traversal (`traversal`) and route reconstruction (`find_route`) |
| `tests_Dijkstra.ipynb` | Same, with a hand-made weighted graph with cycles |
| `tests_Exhaustive.ipynb` | `traversal` and `find_route` of the exhaustive player (the TSP itself is not tested) |
| `tests_Greedy.ipynb`, `tests_GreedyEachCheese.ipynb` | `find_route`, `get_metagraph`, `greedy` |
| `tests_GreedyEachTurn.ipynb` | Same, plus the case where a cheese is eaten before being reached |

## Tournament

The PyRat tournament is optional. Games are played on a 25×20 maze (80% open cells, 60% walls, 20% mud of 4 to 9 turns, 41 pieces of cheese), with 3 s of preprocessing and 0.1 s per turn. We entered `CompetPlayer` and finished in **5th place**.

## Team organization

Roles rotate with each deliverable, with one person in charge of the code, one of the documentation, and one of the unit tests:

| Deliverable | Code | Documentation | Tests |
|---|---|---|---|
| Deliverable 1 (one cheese) | CREPIN | JANIN | SARETE |
| Deliverable 2 (several cheeses) | SARETE | CREPIN | JANIN |

The archives [JANIN_CREPIN_SARETE_1.zip](JANIN_CREPIN_SARETE_1.zip) (deliverable 1) and [JANIN_CREPIN_SARETE.zip](JANIN_CREPIN_SARETE.zip) (deliverable 2) contain the submissions as handed in, with their original READMEs.

## Use of generative AI

<!-- TO BE COMPLETED BY THE TEAM: the course requires declaring the AI tools used and the parts concerned. -->

---

*Project carried out for the Computer Science course unit, FISE 1A, IMT Atlantique.*
