from parsers.parser_classes import Derivation,ParseTree,TreeNode
import copy

# GRAMMAR

# S -> (S) | _

def derive(input_string):
    # Split into tokens
    input_tokens = list(input_string)
    input_tokens.append("%")

    # Instantiate first derivation
    root_node = TreeNode("S", False)
    initial_tree = ParseTree(root_node)
    initial_derivation = Derivation(initial_tree)

    # Parse
    derivations = S(input_tokens, initial_derivation)

    # Length check done here as cannot be done in S due to grammar
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

def S(input_tokens, derivation):
    # S -> (S) | _

    result_derivations = []

    # Compute first rule derivations
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = S1(input_tokens, tree_copy)

    # Concatenate input derivation with first returned derivation, then add returned derivations to result
    derivation_copy = copy.deepcopy(derivation)
    derivation_copy.append_derivation(derivations[0])
    result_derivations.append(derivation_copy)
    for i in range(1,len(derivations)):
        result_derivations.append(derivations[i])

    # Compute second prod. rule deriv.s
    # Since 2nd is empty string, no need for function call
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    childe = TreeNode("ε", True)
    tree_copy.get_current().add_child(childe)
    derivation2 = Derivation(tree_copy)
    result_derivations.append(derivation2)

    return result_derivations

def S1(input_tokens,tree):
    # S -> (S)

    result_derivations = []

    # Add ( S ) child nodes and extend derivation
    childLBR = TreeNode("(", True)
    childS = TreeNode("S", False)
    childRBR = TreeNode(")", True)
    tree.get_current().add_children([childLBR,childS,childRBR])
    derivation = Derivation(tree)

    if input_tokens[derivation.get_cursor()] != "(":
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected '('")
        return [derivation]
    
    # Add copy of derivation with cursor +1
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    tree_copy.increment_cursor()
    derivation.add_tree(tree_copy)

    # Compute S derivations
    derivations = S(input_tokens, derivation)

    for d in derivations:
        if d.get_validity() == False:
            result_derivations.append(d)
        elif input_tokens[d.get_cursor()] != ")":
            d.set_validity(False)
            d.set_reason("INVALID : unexpected ')'")
            result_derivations.append(d)
        else:
            tree_copy = copy.deepcopy(d.get_last_tree())
            tree_copy.increment_cursor()
            d.add_tree(tree_copy)
            result_derivations.append(d)
    
    return result_derivations
