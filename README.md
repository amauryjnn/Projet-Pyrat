# 🐀 Projet PyRat

Projet d'informatique du semestre 5 (FISE 1A, IMT Atlantique) : programmer en Python un rat qui évolue dans un labyrinthe pour attraper des morceaux de fromage, en s'appuyant sur la théorie des graphes et des algorithmes classiques.

🏆 **Notre programme de compétition a terminé 5ᵉ du tournoi PyRat.**

Réalisé en trinôme par **Amaury JANIN**, **CREPIN** et **SARETE**.

> Énoncé et séances du projet : <https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/index.html>

---

## Sommaire

- [Le jeu](#le-jeu)
- [Ce que contient le dépôt](#ce-que-contient-le-dépôt)
- [Les joueurs](#les-joueurs)
- [Le joueur de compétition](#le-joueur-de-compétition)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Tournoi](#tournoi)
- [Organisation de l'équipe](#organisation-de-léquipe)
- [Utilisation de l'IA générative](#utilisation-de-lia-générative)

---

## Le jeu

[PyRat](https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/index.html) est un jeu à un ou plusieurs joueurs. Le labyrinthe est un **graphe** : les cases sont les sommets, les passages sont les arêtes. Les cases de **boue** sont des arêtes pondérées : elles demandent plusieurs tours pour être traversées. Le but est de ramasser le plus de fromage possible, et en un minimum de tours.

Le projet est découpé en séances, chacune ajoutant une difficulté :

| Séance | Problème | Algorithmes |
|---|---|---|
| 1 | Découverte, premiers joueurs aléatoires | Marches aléatoires (`Random1` à `Random5`) |
| 2 | Attraper **1 fromage** | Parcours en largeur (BFS) et en profondeur (DFS) |
| 3 | Attraper **1 fromage** avec de la boue | Dijkstra (avec un tas-min maison) |
| 4 | Attraper **N fromages** | Voyageur de commerce (TSP) par recherche exhaustive |
| 5 | Attraper N fromages **plus vite** | Algorithmes gloutons et heuristiques |
| 6 | **Défier un adversaire** | Stratégie contre un adversaire (théorie des jeux) |

## Ce que contient le dépôt

```
.
├── players/   Les joueurs (une classe par fichier, héritant de pyrat.Player)
├── utils/     Briques réutilisables : MinHeap, Traversal, BFSTraversal, DFSTraversal
├── games/     Notebooks qui lancent des parties, visualisent et comparent les joueurs
├── test/      Tests unitaires (unittest, dans des notebooks)
├── doc/       Documentation de la bibliothèque PyRat (HTML, générée avec pdoc)
└── *.zip      Archives des livrables 1 et 2 rendus pendant le semestre
```

## Les joueurs

Tous les joueurs sont dans [players/](players/) et héritent de `pyrat.Player` (méthodes `preprocessing`, `turn`, `postprocessing`).

| Joueur | Description |
|---|---|
| `Random1` … `Random5` | Marches aléatoires de plus en plus malignes : mouvement au hasard, évitement des murs, préférence pour les cases non visitées, etc. |
| `BFS`, `DFS`, `DFS_recursive` | Un seul fromage : le chemin est calculé dans `preprocessing` par un parcours en largeur ou en profondeur (version récursive de DFS incluse). |
| `TraversalPlayer` | Joueur générique qui utilise au choix [BFSTraversal](utils/BFSTraversal.py) ou [DFSTraversal](utils/DFSTraversal.py). |
| `Dijkstra` | Un seul fromage, plus court chemin pondéré (gère la boue) grâce au [MinHeap](utils/MinHeap.py) implémenté sans `heapq`. |
| `Exhaustive` | N fromages : construit un **métagraphe** (joueur + fromages, arêtes = plus courts chemins) puis résout le TSP par recherche exhaustive avec élagage. Optimal mais en temps factoriel. |
| `Greedy` | N fromages : même métagraphe, mais visite toujours le fromage le plus proche. Ordre calculé une seule fois. |
| `GreedyEachCheese` | Comme `Greedy`, mais le métagraphe est recalculé à chaque fromage atteint. |
| `GreedyEachTurn` | Comme `GreedyEachCheese`, mais la cible est réévaluée dès que le fromage visé disparaît (par exemple mangé par l'adversaire). |
| `GreedyTest` | Variante expérimentale : glouton avec anticipation sur quelques pas. |
| `CompetPlayer` | Notre joueur de compétition (voir ci-dessous). |
| `TemplatePlayer` | Modèle fourni pour écrire un nouveau joueur. |

**Complexités** (V sommets, E arêtes du labyrinthe, N fromages) : la traversée de Dijkstra coûte O((V+E) log V), la reconstruction d'un chemin O(V), et le choix glouton O(N). L'exhaustif explore jusqu'à N! ordres de visite, d'où le besoin de méthodes gloutonnes pour les grandes parties.

**Résultat de la comparaison Exhaustif / Glouton** ([games/compare_exhaustive_greedy.ipynb](games/compare_exhaustive_greedy.ipynb)) : le glouton demande un peu plus de tours que l'exhaustif, mais il est beaucoup plus rapide à calculer.

## Le joueur de compétition

[CompetPlayer](players/CompetPlayer.py) est prévu pour les paramètres du tournoi : un labyrinthe 25×20 avec 41 fromages, de la boue, 3 s de prétraitement et 0,1 s par tour. L'exhaustif y est inutilisable, et seul un algorithme rapide tient dans le budget de temps.

Principe :

1. **Métagraphe** : on relie le rat et tous les fromages par leurs plus courts chemins (Dijkstra, arrêté dès que tous les fromages sont trouvés).
2. **Glouton** : on vise le fromage le plus proche et on mémorise la suite d'actions à suivre.
3. **Mise à jour** : quand la cible disparaît ou est atteinte, on retire les fromages disparus du métagraphe, on recalcule les distances depuis la position courante et on choisit une nouvelle cible.
4. **Zones de fromage** (`get_zones`) : un BFS borné regroupe les fromages proches en zones et compte les fromages par zone. Cette partie est calculée en `preprocessing` et visualisée dans [games/visualize_CompetPlayer.ipynb](games/visualize_CompetPlayer.ipynb), mais elle n'est pas encore utilisée pour choisir la route : c'est la piste d'amélioration principale (visiter zone par zone plutôt que fromage par fromage).

## Installation

Prérequis : Python ≥ 3.12 (les fichiers compilés présents ont été générés avec 3.12) et la bibliothèque **PyRat**, installée comme indiqué à la [séance 1](https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/session1/index.html) du cours. La documentation de PyRat est aussi disponible hors-ligne dans [doc/index.html](doc/index.html).

```bash
git clone https://github.com/amauryjnn/Projet-Pyrat.git
cd Projet-Pyrat
```

Dépendances Python utilisées par le code et les notebooks, en plus de PyRat :

```bash
pip install jupyter numpy matplotlib networkx scikit-learn
```

`networkx` et `scikit-learn` ne servent qu'à des imports de type dans quelques joueurs (par exemple `CompetPlayer`), mais ils doivent être présents pour que ces fichiers s'importent.

## Utilisation

Les notebooks utilisent des chemins relatifs : il faut les **lancer depuis le dossier `games/`**.

```bash
cd games
jupyter notebook
```

Notebooks utiles :

| Notebook | Rôle |
|---|---|
| `tutorial.ipynb`, `sample_game.ipynb` | Prise en main de PyRat |
| `visualize_<Joueur>.ipynb` | Lance une partie avec le joueur indiqué et l'affiche |
| `compare_all_randoms.ipynb` | Compare les cinq joueurs aléatoires |
| `compare_exhaustive_greedy.ipynb` | Compare vitesse et nombre de tours des joueurs exhaustif et glouton |
| `match_Greedy_GreedyEachTurn.ipynb` | Match en face à face entre variantes gloutonnes |
| `tournament.ipynb` | Script de tournoi fourni (poules puis phase finale) |

Exemple minimal, tiré de `visualize_CompetPlayer.ipynb` :

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

Les tests unitaires utilisent `unittest` et sont écrits dans des notebooks du dossier [test/](test/). Chaque notebook se lance depuis `test/` (**Run All**) et se termine par `unittest.main(...)`.

| Notebook | Teste |
|---|---|
| `tests_MinHeap.ipynb` | Ajout, retrait, remplacement et clés de types variés |
| `tests_BFS.ipynb`, `tests_DFS.ipynb` | Parcours (`traversal`) et reconstruction de route (`find_route`) |
| `tests_Dijkstra.ipynb` | Idem, avec un graphe pondéré à cycles fait main |
| `tests_Exhaustive.ipynb` | `traversal` et `find_route` du joueur exhaustif (le TSP lui-même n'est pas testé) |
| `tests_Greedy.ipynb`, `tests_GreedyEachCheese.ipynb` | `find_route`, `get_metagraph`, `greedy` |
| `tests_GreedyEachTurn.ipynb` | Idem, plus le cas où un fromage est mangé avant d'être atteint |

## Tournoi

Le tournoi PyRat est facultatif. Les parties se jouent sur un labyrinthe 25×20 (80 % de cases ouvertes, 60 % de murs, 20 % de boue de 4 à 9 tours, 41 fromages), avec 3 s de prétraitement et 0,1 s par tour. Nous avons présenté `CompetPlayer` et terminé à la **5ᵉ place**.

## Organisation de l'équipe

Les rôles tournent à chaque livrable, avec un responsable du code, un de la documentation et un des tests unitaires :

| Livrable | Code | Documentation | Tests |
|---|---|---|---|
| Livrable 1 (un fromage) | CREPIN | JANIN | SARETE |
| Livrable 2 (plusieurs fromages) | SARETE | CREPIN | JANIN |

Les archives [JANIN_CREPIN_SARETE_1.zip](JANIN_CREPIN_SARETE_1.zip) (livrable 1) et [JANIN_CREPIN_SARETE.zip](JANIN_CREPIN_SARETE.zip) (livrable 2) contiennent les rendus tels que remis, avec leurs README d'époque.

## Utilisation de l'IA générative

<!-- À COMPLÉTER PAR L'ÉQUIPE : le cours demande de déclarer les outils d'IA utilisés et les parties concernées. -->

---

*Projet réalisé dans le cadre de l'UE Informatique, FISE 1A, IMT Atlantique.*
