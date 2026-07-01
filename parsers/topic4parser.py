from parsers.parser_classes import Derivation,ParseTree,TreeNode
import copy

# GRAMMAR

# S -> A
# A -> a | B
# B -> Ab

# This grammar is left recursive (indirectly)
# In this case, if the 2nd prod rule is checked for A, it will fall into left recursion
# S -> A -> B -> Ab -> Bb -> Abb -> ...
# Since it won't always fall into recursion, we must implement most of the regular parer and catch when it falls into recursion
# This is done by passing around a parameter to track iterations

def derive(input_string):
    # Split into tokens
    input_tokens = list(input_string)
    input_tokens.append("%")

    # Create the derivation, starting S
    root_node = TreeNode("S", False)
    initial_tree = ParseTree(root_node)
    initial_derivation = Derivation(initial_tree)

    # Parse
    return S(input_tokens, initial_derivation)

def S(input_tokens, derivation):
    # S -> A

    tree_copy = copy.deepcopy(derivation.get_last_tree())
    
    # Add A child node and extend derivation
    childA = TreeNode("A", False)
    tree_copy.get_current().add_child(childA)
    derivation.append_derivation(Derivation(tree_copy))

    # Compute A's prod rules
    derivations = A(input_tokens, derivation, iterations=0)

    for d in derivations:
        if input_tokens[d.get_cursor()] != "%" and d.get_validity()==True:
            d.set_validity(False)
            d.set_reason("INVALID : doesn't derive entire input")

    truncated_derivations = []

    for d in derivations:
        truncated_derivations.append(d)
        if d.get_validity():
            break

    return truncated_derivations

def A(input_tokens, derivation, iterations):
    # A -> a | B

    result_derivations = []

    # COmpute first prod rules derivs
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = A1(input_tokens, tree_copy, iterations)

    # Concatenate copy of input with first deriv, then append all
    derivation_copy = copy.deepcopy(derivation)
    derivation_copy.append_derivation(derivations[0])
    result_derivations.append(derivation_copy)
    for i in range(1,len(derivations)):
        result_derivations.append(derivations[i])

    # COmpute 2nd
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = A2(input_tokens, tree_copy, iterations)

    # Append to results
    for i in range(0,len(derivations)):
        result_derivations.append(derivations[i])

    return result_derivations

def A1(input_tokens, tree, iterations):
    # A -> a

    result_derivations = []

    # Add child node a
    childa = TreeNode("a", True)
    tree.get_current().add_child(childa)
    derivation = Derivation(tree)

    # Check if token is 'a'
    if input_tokens[derivation.get_cursor()] != 'a':
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected 'a'")
        return [derivation]
    
    # Add copy to derivation with incremented cursor
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    tree_copy.increment_cursor()
    derivation.add_tree(tree_copy)

    return [derivation]

def A2(input_tokens, tree, iterations):
    # A -> B

    iterations += 1
    if iterations < 9:
        # As normal...

        # Add child node B
        childB = TreeNode("B", False)
        tree.get_current().add_child(childB)
        derivation = Derivation(tree)

        # Compute B derivations
        derivations = B(input_tokens, derivation, iterations)
        
        return derivations
    else:
        # Break recursion using "..." node
        childSOON = TreeNode("...", False)
        tree.get_current().add_child(childSOON)
        derivation = Derivation(tree)
        derivation.set_validity(False)
        derivation.set_reason("TIMEOUT : fallen into left recursion")
        return [derivation]

def B(input_tokens, derivation, iterations):
    # B -> Ab

    result_derivations = []

    tree_copy = copy.deepcopy(derivation.get_last_tree())

    # Add child nodes A & b
    childA = TreeNode("A", False)
    childb = TreeNode("b", True)
    tree_copy.get_current().add_children([childA,childb])
    derivation.add_tree(tree_copy)

    derivations = A(input_tokens, derivation, iterations)

    for d in derivations:
        if d.get_validity() == False:
            result_derivations.append(d)
        elif input_tokens[d.get_cursor()] != 'b':
            d.set_validity(False)
            d.set_reason("INVALID : unexpected 'b'")
            result_derivations.append(d)
        else:
            tree_copy = copy.deepcopy(d.get_last_tree())
            tree_copy.increment_cursor()
            d.add_tree(tree_copy)

            result_derivations.append(d)

    return result_derivations