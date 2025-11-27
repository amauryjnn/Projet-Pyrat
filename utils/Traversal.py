#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a traversal.
    Instanciated objects can be used to traverse a graph and find a path between two vertices.
    The way the path is found depends on the structure used to store the vertices to visit.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import abc

# PyRat imports
from pyrat import Graph, Maze, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Traversal (abc.ABC):

    """
        This class is abstract and cannot be instantiated.
        It defines a traversal of a graph.
        You should extend it and define the initialize_structure, add_to_structure, and get_from_structure methods.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self: Self,
                 ) ->    Self:

        """
            This function is the constructor of the class.
            In:
                * self: Reference to the current object.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__()

        # Calling traversal will set these attributes
        self.routing_table = None
        self.distances = None
       
    #############################################################################################################################################
    #                                                                  METHODS                                                                  #
    #############################################################################################################################################

    def traversal ( self:   Self,
                    graph:  Graph,
                    source: Integral
                  ) ->      None:

        """
            This method performs a traversal of a graph.
            It computes the distances from the source to all other vertices.
            It also computes the routing table, that is, the parent of each vertex in the traversal.
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
            Out:
                * None.
        """
        # Initialization
        self.source = source

        self.routing_table = {}
        self.distances = {}

        to_visit = self.initialize_structure()
        self.add_to_structure(to_visit, (source, None, 0))

        while len(to_visit) != 0:
            (current_vertex, parent_vertex, distance), to_visit = self.get_from_structure(to_visit)

            if current_vertex not in self.distances:

                self.distances[current_vertex] = distance
                self.routing_table[current_vertex] = parent_vertex

                neighbors = graph.get_neighbors(current_vertex)
                for neighbor in neighbors:
                    if neighbor not in self.distances:
                        self.add_to_structure(to_visit, (neighbor, current_vertex, distance + 1))
        
    #############################################################################################################################################

    def find_route ( self:   Self,
                     target: Integral
                   ) ->      List[Integral]:

        """
            This method finds the route from the source to the target using the routing table.
            In:
                * self:   Reference to the current object.
                * target: The target vertex.
            Out:
                * route: The route from the source to the target.
        """

        # Debug
        assert(self.routing_table is not None) # Should not be called before traversal

        route = [target]
        while route[-1] != self.source:
            route.append(self.routing_table[route[-1]])
        return [route[-(i+1)] for i in range(len(route))]

    #############################################################################################################################################

    @abc.abstractmethod
    def initialize_structure ( self: Self,
                             ) ->    Any:
    
        """
            This method is abstract and must be implemented in the child classes.
            It initializes the data structure needed for the traversal.
            In:
                * self: Reference to the current object.
            Out:
                * structure: Initialized data structure.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")
    
    #############################################################################################################################################

    @abc.abstractmethod
    def add_to_structure ( self:      Self,
                           structure: Any,
                           element:   Any
                         ) ->         Any:
    
        """
            This method is abstract and must be implemented in the child classes.
            It adds an element to the data structure.
            In:
                * self:      Reference to the current object.
                * structure: Data structure to update.
                * element:   Element to add.
            Out:
                * structure: Updated data structure.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

    #############################################################################################################################################

    @abc.abstractmethod
    def get_from_structure ( self:      Self,
                             structure: Any,
                           ) ->         Tuple[Any, Any]:
    
        """
            This method is abstract and must be implemented in the child classes.
            It gets an element from the data structure.
            In:
                * self:      Reference to the current object.
                * structure: Data structure to update.
            Out:
                * element:   Element to get.
                * structure: Updated data structure.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

#####################################################################################################################################################
#####################################################################################################################################################
