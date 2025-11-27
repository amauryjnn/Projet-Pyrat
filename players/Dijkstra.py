#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from networkx import neighbors, Graph 
from typing_extensions import *
from numbers import *
import os, sys

# Add needed directories to the path
this_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_directory, "..", "utils"))

# PyRat imports
from pyrat import Player, Maze, GameState, Action
from MinHeap import MinHeap 
#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Dijkstra (Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # List of actions to follow 
        self.actions = []
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing ( self:       Self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
            This method redefines the method of the parent class.
            It is called once at the beginning of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * None.
        """
        # On récupère la position initiale du joueur ainsi que celle du fromage
        player_pos = game_state.player_locations[self.name]
        cheese_pos = game_state.cheese[0]

        # On récupère la routing_table à l'aide de la method traversal (le dict des distances ne nous intéresse pas)
        _, routing_table = self.traversal(maze, player_pos)
        route = self.find_route(routing_table, player_pos, cheese_pos)

        # On enregistre les actions à effectuer aux prochains tours
        self.actions = maze.locations_to_actions(route)

    #############################################################################################################################################

    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Return a predefined action
        return self.actions.pop(0)

#############################################################################################################################################

    @override
    def postprocessing ( self:       Self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      Dict[str, Any],
                       ) ->          None:

        """
            This method redefines the method of the parent class.
            It is called once at the end of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
                * stats:      Statistics about the game.
            Out:
                * None.
        """

        # Print phase of the game
        print("Postprocessing")

#####################################################################################################################################################
#####################################################################################################################################################

    def traversal( self:   Self,
                    graph:  Graph,
                    source: Integral):
        """
            Implémentation de dijkstra, ne s'arrête pas lorsque le fromage est trouvé pour faciliter les tests.
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
            Out:
                * distances:     The distances from the source to each explored vertex.
                * routing_table: The routing table, that is, the parent of each vertex in the traversal (None for the source).
        """
        # initialize 
        min_heap = MinHeap()
        routing_table = {}
        explored_vertices = {}    # On peut se passer de ce dictionnaire si on ne veut que trouver le chemin
        min_heap.add_or_replace(source, (0, None))

        # algorithm loop
        while len(min_heap.elements) != 0:
            # On récupère le prochain élement de la min_heap et on l'ajoute à nos différents dict.
            current_vertex, (distance, parent) = min_heap.remove()
            explored_vertices[current_vertex] = distance
            routing_table[current_vertex] = parent

            # On itère sur tous les voisins du nouveau point
            neighbors = graph.get_neighbors(current_vertex)
            for neighbor in neighbors:
                if neighbor not in routing_table:
                    distance_next = distance + graph.get_weight(current_vertex,neighbor)
                    min_heap.add_or_replace(neighbor, (distance_next, current_vertex))

        return explored_vertices, routing_table 
    

    def find_route ( self:          Self,
                    routing_table: Dict[Integral, Optional[Integral]],
                    source:        Integral,
                    target:        Integral
                ) ->             List[Integral]:

        """
            This method finds the route from the source to the target using the routing table.
            In:
                * self:          Reference to the current object.
                * routing_table: The routing table.
                * source:        The source vertex.
                * target:        The target vertex.
            Out:
                * route: The route from the source to the target.
        """
        route = [target]
        # On remonte le chemin depuis la cible jusqu'a retomber sur la source
        while route[-1] != source:
            route.append(routing_table[route[-1]])

        # On renvoie la liste inversée pour plus facilement utiliser locations_to_actions par la suite
        return [route[-(i+1)] for i in range(len(route))]
