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
from typing_extensions import *
from numbers import *
import os, sys

# Add needed directories to the path
this_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_directory, "..", "utils"))

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph
from pyrat import Player, Maze, GameState, Action, Graph
from MinHeap import MinHeap 
#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class GreedyEachTurn (Player):

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

        # Metagraph used to link the player and all cheeses
        self.metagraph = []

        # List of routing tables linking the player and all cheeses
        self.routing_tables = {}

        # List of actions to follow 
        self.actions = []
        self.target = 0
       
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
        cheese_pos = game_state.cheese

        # On crée le metagraph reliant les froamges puis on applique 
        # l'algorithme greedy pour récupérer le chemin à suivre
        self.metagraph, self.routing_tables = self.get_metagraph(maze, player_pos, cheese_pos)
        self.target = self.greedy(self.metagraph, player_pos)

        # On enregistre les actions à effectuer aux prochains tours
        self.actions = maze.locations_to_actions(self.find_route(self.routing_tables[player_pos], player_pos, self.target))

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

        player_pos = game_state.player_locations[self.name]
        cheese_pos = game_state.cheese
        
        # Tant qu'il y a des actions a jouer et que le fromage vers lequel on se dirige existe
        # on continue d'avancer
        if len(self.actions) != 0 and self.target in cheese_pos:
            return self.actions.pop(0)
        
        # Sinon on récupère le prochain fromage à récupérer si il en reste
        elif len(cheese_pos) != 0:
            # On update le metagraph pour enlever les fromages ayant disparu et recalculer la distance du joueur à tous les fromages
            self.metagraph, routing_table = self.update_metagraph(self.metagraph, maze, player_pos, cheese_pos)
            # Il n'est pas nécessaire d'enlever les anciennes routing table car elles restent valides
            self.routing_tables[player_pos] = routing_table
            # On trouve le nouveau fromage à chercher
            self.target = self.greedy(self.metagraph, player_pos)
            # On enregistre les actions à effectuer aux prochains tours
            self.actions = maze.locations_to_actions(self.find_route(self.routing_tables[player_pos], player_pos, self.target))
            return self.actions.pop(0)
        
        return Action.NOTHING

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

#####################################################################################################################################################
#####################################################################################################################################################
    
    def get_metagraph( self: Self,
                      graph: Graph,
                      source: Integral,
                      cheeses: List[Integral]):
        """
            Calcul le metagraph entre la source et tous les fromages du circuit,
            renvoie le metagraph et une liste de routing_table
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
                * cheeses: List of all cheeses to find
            Out:
                * metagraph:     The metagraph.
                * routing_tables: The routing tables, that is, the parent of each vertex in the traversal (None for the source).
        """
        metaGraph = Graph()
        routing_tables = {}

        # Liste de tous les vertices du metagraph
        vertices = [source] + cheeses

        # On rajoute toutes les vertices au metagraph
        for vertex in vertices: 
            metaGraph.add_vertex(vertex)

        # Pour chaque vertice on applique l'algorithme dijkstra pour la relier à toutes les autres vertices non déja explorés.
        # En effet, comme le chemin de A vers B est le même que de B vers A il suffit de le compter qu'une fois et de
        # l'ajouter dans les deux sens
        for i in range(len(vertices)):
            distances, routing_table = self.traversal(graph, vertices[i], vertices[i+1:])
            routing_tables[vertices[i]] = routing_table
            for j in range(1, len(vertices)-i):
                metaGraph.add_edge(vertices[i], vertices[i+j], distances[vertices[i+j]])
                metaGraph.add_edge(vertices[i+j], vertices[i], distances[vertices[i+j]])

        return metaGraph, routing_tables           
    
    def update_metagraph(self: Self,
                        metaGraph: Graph,
                        graph: Graph,
                        source: Integral,
                        cheeses: List[Integral]):
        """
            Cette fonction met à jour le metagraph:
                - Enlève les fromages ayant été récupérés
                - Met à jour la position de la source
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
                * cheeses: List of all cheeses to find
            Out:
                * metagraph:     The metagraph.
                * routing_tables: The routing tables, that is, the parent of each vertex in the traversal (None for the source).
        """
        # On enlève les fromages n'existant plus
        for vertex in metaGraph.vertices:
            if vertex not in cheeses:
                metaGraph.remove_vertex(vertex)

        # On récupère la position de la source vis à vis des autres fromages et on met à jour le metagraph
        distances, routing_table = self.traversal(graph, source, cheeses)
        metaGraph.add_vertex(source)

        for i in range(len(cheeses)):
            metaGraph.add_edge(source, cheeses[i], distances[cheeses[i]])
            metaGraph.add_edge(cheeses[i], source, distances[cheeses[i]])
        
        return metaGraph, routing_table


    def greedy( self: Self,
                graph: Graph, 
                source: Integral):
        """
            Implémentation de l'algorithme greedy, renvoie le plus proche voisin de la source.
            Si celle-ci n'a plus de voisin, elle est elle même renvoyée.
            In :
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
        """
        neighbors = [(graph.get_weight(source, vtx), vtx) for vtx in graph.get_neighbors(source)]
        neighbors.sort()
        if len(neighbors) != 0:
            return neighbors[0][1]
        return source
    

    def traversal( self:   Self,
                    graph:  Graph,
                    source: Integral,
                    cheeses: List[Integral]):
        """
            Implémentation de dijkstra, s'arrête lorsque tous les fromages passés dans cheeses sont trouvés (source to all cheeses).
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
                * cheeses: List of all cheeses to find
            Out:
                * distances:     The distances from the source to each explored vertex.
                * routing_table: The routing table, that is, the parent of each vertex in the traversal (None for the source).
        """
        # If no cheeses to find return empty dict
        if len(cheeses) == 0:
            return {}, {}
        
        # initialize 
        min_heap = MinHeap()
        routing_table = {}
        distances = {}
        min_heap.add_or_replace(source, (0, None))
        nmb_cheese = 0

        # algorithm loop
        while not min_heap.is_empty():
            # On récupère le prochain élement de la min_heap et on l'ajoute à nos différents dict.
            current_vertex, (distance, parent) = min_heap.remove()
            distances[current_vertex] = distance
            routing_table[current_vertex] = parent
            
            # Si on est arrivé a un des fromages on incrémente le compteur de fromages trouvés
            if current_vertex in cheeses:
                nmb_cheese += 1
                # Si tous les fromages sont trouvés on arrête l'algorithme
                if nmb_cheese == len(cheeses):
                    break

            # On itère sur tous les voisins du nouveau point
            neighbors = graph.get_neighbors(current_vertex)
            for neighbor in neighbors:
                if neighbor not in routing_table:
                    distance_next = distance + graph.get_weight(current_vertex,neighbor)
                    min_heap.add_or_replace(neighbor, (distance_next, current_vertex))

        return distances, routing_table 
    

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
        route.reverse()
        return route
    

    def find_routes(self:           Self,
                    routing_tables: Dict[Integral, Dict[Integral, Optional[Integral]]],
                    points:         List[Integral]):
        """
            Return a route from a list of routing_tables and an order set of points to follow
            In:
                * self:          Reference to the current object.
                * routing_tables:The routing tables associated to the differents points.
                * points:        The ordered list of points to reach.
            Out:
                * route: The route from the source to the target.
        """
        route = [points[0]]
        for i in range(len(points)-1):
            # Comme les routing table ne sont calculés que dans un sens (de A vers B ou l'inverse mais pas les deux)
            # il faut trouver laquel des deux routing table utiliser. On applique ensuite l'algorithme find_route.
            if points[i+1] in routing_tables[points[i]]:
                sub_route = self.find_route(routing_tables[points[i]], points[i], points[i+1])
            else:
                sub_route = self.find_route(routing_tables[points[i+1]], points[i+1], points[i])
                sub_route.reverse()
            route += sub_route[1:]
        
        return route

