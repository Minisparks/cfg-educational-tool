from parsers.visualnode_class import VisualNode
from parsers.visualedge_class import VisualEdge
import pygame
from pygame.locals import *
import sys

class Derivation:
    def __init__(self, initial_tree):
        self._trees = []
        self._trees.append(initial_tree)
        self._is_valid = True
        self._reason = None
        self._length = 1
    
    def add_tree(self, tree):
        """
        Appends another tree (step) to the derivation
        INPUTS:
            tree : tree to be added
        """
        self._trees.append(tree)
        self._increment_length()

    def get_last_tree(self):
        return self._trees[self._length-1]

    def get_trees(self):
        return self._trees

    def set_validity(self, is_valid):
        self._is_valid = is_valid

    def get_validity(self):
        return self._is_valid

    def _set_length(self, length):
        self._length = length

    def _increment_length(self):
        self._length += 1

    def _decrement_length(self):
        self._length -= 1

    def get_length(self):
        return self._length

    def get_cursor(self):
        return self.get_last_tree().get_cursor()

    def set_cursor(self, cursor):
        self.get_last_tree().set_cursor(cursor)

    def increment_cursor(self):
        self.get_last_tree().increment_cursor()

    def append_derivation(self, new_derivation):
        """
        Combines another derivation with this derivation
        INPUTS:
            new_derivation : the derivation to add to the current derivation
        """
        for tree in new_derivation.get_trees():
            self.add_tree(tree)
        self.set_cursor(new_derivation.get_cursor())
        self._is_valid = new_derivation.get_validity()
        self._reason = new_derivation.get_reason()

    def set_reason(self, reason):
        self._reason = reason

    def get_reason(self):
        return self._reason


class ParseTree:
    def __init__(self, root_node):
        self._root = root_node
        self._cursor = 0
    
    def get_current(self):
        return self._root.get_current()

    def get_string(self):
        return self._root.get_string()

    def get_cursor(self):
        return self._cursor

    def set_cursor(self, cursor):
        self._cursor = cursor

    def increment_cursor(self):
        self._cursor += 1

    def generate_visual_nodes_and_edges(self):
        """
        Uses the Reingold-Tilford Algorithm to generate a list of nodes and list of edges
        OUTPUTS:
            a list of nodes and edges (each with positions) that represent the ParseTree
        """

        # Pass to calculate x, mod and shift
        self._root.rta_pass1([],[])

        # Pass 2 to calculate final x values
        max_x, min_x, max_y = self._root.rta_pass2(0,0)

        # Calculate necessary adjustments to convert to screen positions
        if max_x == min_x:
            x_scale = 1
            x_shift = 1050
        else:
            x_scale = 1000 / (max_x - min_x)
            x_shift = 550 - (min_x * x_scale)

        if max_y == 0:
            y_scale = 1
            y_shift = 150
        else:
            y_scale = (600 / max_y) * min(1,(max_y/7))
            y_shift = 150

        # Pass 3 to apply adjustments to final x values
        self._root.rta_pass3(x_shift, y_shift, x_scale, y_scale)

        # Generate nodes & edges to display on screen
        nodes,edges = self._root.get_visual_nodes_and_edges()

        # Make accepted tokens bold and set target node
        terminal_number = 0
        leaf_number = 0
        epsilon_counter = 0
        for node in nodes:
            if node.get_token() == 'ε':
                node.make_bold()
                epsilon_counter += 1
                leaf_number += 1
                terminal_number += 1
            elif node.get_is_terminal() == True and terminal_number - epsilon_counter < self.get_cursor():
                node.make_bold()
                terminal_number += 1
                leaf_number += 1
            elif node.get_is_leaf() == True and leaf_number - epsilon_counter == self.get_cursor():
                node.make_target()
                leaf_number += 1
                
        return nodes,edges

class TreeNode:
    def __init__(self, token, is_terminal):
        self._token = token
        self._children = []
        self._is_terminal = is_terminal

        # Following used for drawing the tree nodes:
        self._x = 0          #x coord used in pass 1, before applying shifts, mods and adjustments
        self._mod = 0        #mod to be applied only to descendants
        self._shift = 0      #shift to be applied to descendants and self
        self._y = 0          #y coord used in pass 1, before applying adjustments
        self._x_final = 0    #x coord after applying shifts, mods (in pass 2) and adjustments (in pass 3)
        self._y_final = 0    #y coord after applying adjustments (pass 3)

    def add_child(self, child):
        """
        Adds another node to the child list
        INPUTS:
            child : node to be added
        """
        self._children.append(child)
    
    def add_children(self, children):
        """
        Adds multiple nodes to child list
        INPUTS:
            children : nodes to be added
        """
        for child in children:
            self._children.append(child)

    def get_children(self):
        return self._children

    def remove_children(self):
        """
        Removes all children from list of childen
        """
        self._children = []

    def get_is_terminal(self):
        return self._is_terminal

    def get_string(self):
        """
        Recursive function to get string of subtrees tokens
        """
        if(len(self._children) == 0):
            return self._token
        else:
            substring = ""
            for child in self._children:
                substring = substring + child.get_string()
            return substring
    
    def get_current(self):
        """
        Gets the leftmost non-terminal leaf in the subtree
        """
        if (self._is_terminal):
            return None
        
        if (len(self._children) == 0):
            return self

        for child in self._children:
            result = child.get_current()
            if (result != None):
                return result
            
        return None

    def get_visual_nodes_and_edges(self):
        """
        Creates list of nodes and edges that represents subtree rooted at this node
        OUTPUTS:
            list of generated nodes and list of edges
        """
        nodes = []
        edges = []
        for child in self._children:
            child_nodes,child_edges = child.get_visual_nodes_and_edges()
            nodes = nodes + child_nodes
            edges = edges + child_edges + [VisualEdge(start=(self._x_final,self._y_final), end=(child.get_x_final(),child.get_y_final()))]
        
        is_leaf = False
        if len(self._children) == 0: is_leaf = True
        nodes = nodes + [VisualNode(token=self._token, x_position=self._x_final, y_position=self._y_final, is_terminal=self._is_terminal,is_leaf=is_leaf)]

        return nodes,edges

    # Following used to implement the Reingold-Tilford Algorithm

    def rta_pass1(self, left_siblings, right_siblings):
        """
        First pass of the RTA to calculate x mod and shift
        INPUTS:
            left_siblings : list of this nodes left siblings
            right_siblings : list of this nodes right siblings
        """

        children = self._children
        num_children = len(children)
        SIBLING_DISTANCE = 1
        SUBTREE_DISTANCE = 1

        if len(left_siblings) == 0:
            if num_children > 0:
                # leftmost, has children

                for i in range(0,num_children):
                    children[i].rta_pass1(left_siblings=children[0:i], right_siblings=children[i+1:num_children])
                
                self._x = self.get_children_midpoint()
                self._mod = 0
            else:
                # leftmost, no children

                self._x = 0
                self._mod = 0
        else:
            if num_children > 0:
                # not leftmost, has children

                for i in range(0,num_children):
                    children[i].rta_pass1(left_siblings=children[0:i], right_siblings=children[i+1:num_children])

                self._x = left_siblings[-1].get_x() + SIBLING_DISTANCE
                self._mod = self._x - self.get_children_midpoint()

                # Check for overlaps and apply relative shifts to siblings

                for i in range(0,len(left_siblings)):
                    right_contour_positions = left_siblings[i].get_right_contour_positions()
                    left_contour_positions = self.get_left_contour_positions()
                    sibling_index = i
                    own_index = len(left_siblings)

                    shift = self.calculate_shift(right_contour_positions, left_contour_positions, sibling_index, own_index, SUBTREE_DISTANCE)

                    all_siblings = left_siblings + [self] + right_siblings
                    j = 0
                    for sibling in all_siblings:
                        relative_shift = (j*shift) / own_index
                        sibling.add_shift(relative_shift)
                        j += 1
            else:
                # not leftmost, no children

                self._x = left_siblings[-1].get_x() + SIBLING_DISTANCE
                self._mod = 0

    def rta_pass2(self, carried_adjustment, level):
        """
        Pass 2 of RTA to calculate final x value
        INPUTS:
            carried_adjustment : total mod and shift of parent nodes
            level : y level of the node (0 at root, increasing with depth)
        OUTPUTS:
            maximum depth of subtree, maximum and minumum x values of subtree
        """

        self._x_final = self._x + self._shift + carried_adjustment
        self._y_final = level
        child_adjustment = self._shift + self._mod + carried_adjustment
        max_x = self._x_final
        min_x = self._x_final
        max_y = self._y_final
        for child in self._children:
            sub_max_x,sub_min_x,sub_max_y = child.rta_pass2(carried_adjustment=child_adjustment, level=level+1)
            if sub_max_x > max_x: max_x = sub_max_x
            if sub_min_x < min_x: min_x = sub_min_x
            if sub_max_y > max_y: max_y = sub_max_y
        return max_x, min_x, max_y

    def rta_pass3(self, x_shift, y_shift, x_scale, y_scale):
        """
        Pass 3 of RTA to apply adjustments
        INPUTS:
            x_shift : amount to translate nodes horizontally
            y_shift : amount to translate nodes vertically
            x_scale : amount to scale nodes by horizontally
            y_scale : amount to scale nodes by vertically
        """

        self._x_final = self._x_final * x_scale
        self._x_final = self._x_final + x_shift
        self._y_final = self._y_final * y_scale
        self._y_final = self._y_final + y_shift
        for child in self._children:
            child.rta_pass3(x_shift, y_shift, x_scale, y_scale)
    
    def calculate_shift(self, right_contour_positions, left_contour_positions, sibling_index, own_index, subtree_distance):
        """
        Calculates shift required from overlap of two nodes' subtrees
        INPUTS:
            right_contour_positions : list of positions of left tree's right contours
            left_contour_positions : list of positions of right tree's left contours
            sibling_index : index in of left siblings in child list of parent
            own_index : index of this node in child list of parent
            subtree_distance : distance required between subtrees
        OUTPUT:
            overlap size of the two subtrees
        """

        depth = min(len(right_contour_positions),len(left_contour_positions))
        max_overlap = 0
        for i in range(1,depth):
            overlap = right_contour_positions[i] + subtree_distance - left_contour_positions[i]
            if overlap > max_overlap:
                max_overlap = overlap
        if max_overlap == 0:
            return 0
        else:
            a = max_overlap
            b = a * own_index
            c = b / (own_index - sibling_index)
            return c

    def get_left_contour_positions(self):
        """
        Gets positions of left contours of subtree routed at current node
        OUTPUT:
            list of positions
        """
        length = len(self._children)
        if length == 0:
            return [self._x + self._shift]
        else:
            contour_positions = self._children[0].get_left_contour_positions()
            contour_positions = [x + self._mod + self._shift for x in contour_positions]
            contour_positions = [self._x + self._shift] + contour_positions
            return contour_positions

    def get_right_contour_positions(self):
        """
        Gets positions of right contours of subtree routed at current node
        OUTPUT:
            list of positions
        """
        length = len(self._children)
        if length == 0:
            return [self._x + self._shift]
        else:
            contour_positions = self._children[-1].get_right_contour_positions()
            contour_positions = [x + self._mod + self._shift for x in contour_positions]
            contour_positions = [self._x + self._shift] + contour_positions
            return contour_positions

    def get_x(self):
        return self._x

    def get_mod(self):
        return self._mod

    def get_shift(self):
        return self._shift

    def get_x_final(self):
        return self._x_final

    def get_y_final(self):
        return self._y_final

    def get_children_midpoint(self):
        """
        Calculates midpoint of child nodes
        OUTPUT:
            midpoint
        """
        if len(self._children) == 0:
            return 0
        elif len(self._children) == 1:
            return self._children[0].get_x() + self._children[0].get_shift()
        else:
            leftmost_child = self._children[0]
            rightmost_child = self._children[-1]
            leftmost_position = leftmost_child.get_x() + leftmost_child.get_shift()
            rightmost_position = rightmost_child.get_x() + rightmost_child.get_shift()
            return ((leftmost_position + rightmost_position) / 2)
    
    def add_shift(self, additional_shift):
        self._shift = self._shift + additional_shift