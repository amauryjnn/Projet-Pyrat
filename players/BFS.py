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
from networkx import Graph, neighbors
from typing_extensions import *
from numbers import *

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class BFS (Player):

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

        # Actions to follow 
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
        print("Preprocessing")
        player_pos = game_state.player_locations[self.name]
        cheese_pos = game_state.cheese[0]
        distances, routing_table = self.traversal(maze, player_pos, cheese_pos)
        route = self.find_route(routing_table, player_pos, cheese_pos)
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
        # Return an action
        print("Turnn")
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

    
#####################################################################################################################################################
#####################################################################################################################################################

    def traversal ( self:   Self,
                    graph:  Graph,
                    source: Integral,
                    cheese: Integral,
                    ) ->      Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:

        """
            This method performs a BFS traversal of a graph.
            It returns the explored vertices with associated distances.
            It also returns the routing table, that is, the parent of each vertex in the traversal.
            The algorithm stops once it finds the cheese
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
                * cheese: The vertex of the cheese.
            Out:
                * distances:     The distances from the source to each explored vertex.
                * routing_table: The routing table, that is, the parent of each vertex in the traversal (None for the source).
        """
        queuing_structure = [(source, None, 0)]
        explored_vertices = {}
        routing_table = {}
        while len(queuing_structure) != 0:
            (current_vertex, parent_vertex, distance) = queuing_structure.pop(0)

            if current_vertex not in explored_vertices:

                explored_vertices[current_vertex] = distance
                routing_table[current_vertex] = parent_vertex

                if current_vertex == cheese:
                    break

                neighbors = graph.get_neighbors(current_vertex)
                for neighbor in neighbors:
                    if neighbor not in explored_vertices:
                        queuing_structure.append((neighbor, current_vertex, distance + 1))
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
        while route[-1] != source:
            route.append(routing_table[route[-1]])
        return [route[-(i+1)] for i in range(len(route))]