from parsers.parser_classes import Derivation,ParseTree,TreeNode
import copy

# GRAMMAR

# S -> EXP
# EXP -> EXP + NUM | EXP - NUM | NUM
# NUM -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0

# This grammar is left recursive
# In this case, it will always fall into left recursion
# S -> EXP -> EXP + NUM -> EXP + NUM + NUM -> ...
# Therefore we don't properly derive the input, just manually create the derivation that will always be output

def derive(input_string):
    # Create the derivation, starting S
    root_node = TreeNode("S", False)
    initial_tree = ParseTree(root_node)
    derivation = Derivation(initial_tree)

    # S -> EXP
    tree_copy = copy.deepcopy(initial_tree)
    childEXP = TreeNode("EXP",False)
    tree_copy.get_current().add_child(childEXP)
    derivation.add_tree(tree_copy)

    # Left recursive part of derivation, stop after 5 repeats to interrupt recursion
    for i in range(0,5):
        tree_copy = copy.deepcopy(derivation.get_last_tree())
        childEXP = TreeNode("EXP", False)
        childPLUS = TreeNode("+", True)
        childNUM = TreeNode("NUM", False)
        tree_copy.get_current().add_children([childEXP,childPLUS,childNUM])
        derivation.add_tree(tree_copy)
    
    # Additional "..." node to demonstrate recursion
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    childSOON = TreeNode("...", False)
    tree_copy.get_current().add_child(childSOON)
    derivation.add_tree(tree_copy)

    derivation.set_validity(False)
    derivation.set_reason("TIMEOUT : fallen into left recursion")

    return [derivation]