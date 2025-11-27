#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define MinHeaps.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class MinHeap ():

    """
        This class implement a minheap data structure
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        None:

        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """
        # We create an attribute to store the elements
        self.elements = []

    #############################################################################################################################################
    #                                                                  METHODS                                                                  #
    #############################################################################################################################################

    def add_or_replace ( self:      Self,
                           key: Any,
                           value:   Any
                         ) ->         Any:
    
        """
            This method add or replaces an element in the min_heap.
            If the key doesn't already exist it is added.
            If the min_heap already has an element with the same key and a value 
            greater than the new value it is replaced.
            In:
                * self:      Reference to the current object.
                * key:       value reference.
                * value:     value.
            Out:
                * structure: Updated data structure.
        """

        # We check if the key is already in the heap
        index = None
        for i in range(len(self.elements)):
            if self.elements[i][0] == key:
                index = i
                break
        
        # If the key is already in the heap, we remove the previous element if the new value is lower
        add_new_element = True
        if index is not None:
            if value < self.elements[index][1]:
                del self.elements[index]
            else:
                add_new_element = False

        # We add the new element
        if add_new_element:
            self.elements.append((key, value))

    #############################################################################################################################################

    def remove (self: Self) -> Tuple[Any, Any]:
    
        """
            This method removes the element of lowest value from the min_heap.
            In:
                * self:      Reference to the current object.
            Out:
                * element:   Element to get (key, value).
        """
        # We find the element with the smallest value
        min_index = 0
        for i in range(1, len(self.elements)):
            if self.elements[i][1] < self.elements[min_index][1]:
                min_index = i

        # We remove the element with the smallest value
        key, value = self.elements[min_index]
        del self.elements[min_index]

        # We return the key and value of the element removed
        return key, value
    
    def is_empty(self) -> bool:
        """
            This method return wether or not the min_heap is empty.
            In:
            Out:
                * is_empty: bool
        """
        return len(self.elements) == 0
    
#####################################################################################################################################################
#####################################################################################################################################################