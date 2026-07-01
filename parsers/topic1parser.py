from parsers.parser_classes import Derivation,ParseTree,TreeNode
import copy

# GRAMMAR:

# S -> AB
# A -> aA | _
# B -> bB | _

def derive(input_string):
    # SPlit into tokens
    input_tokens = list(input_string)
    input_tokens.append("%")

    # Instantiate first derivation
    root_node = TreeNode("S", False)
    initial_tree = ParseTree(root_node)
    initial_derivation = Derivation(initial_tree)

    # Parse input
    return S(input_tokens, initial_derivation)

def S(input_tokens, derivation):
    # S -> AB

    result_derivations = []

    tree_copy = copy.deepcopy(derivation.get_last_tree())

    # Add A & B child nodes and extend derivation
    childA = TreeNode("A",False)
    childB = TreeNode("B",False)
    tree_copy.get_current().add_children([childA,childB])
    derivation.append_derivation(Derivation(tree_copy))

    # Compute derivations for A production rules
    derivations = A(input_tokens, derivation)

    for d in derivations:
        if d.get_validity() == False:
            result_derivations.append(d)
        else:
            # Add copy of tree to derivation -> removed as will always end with epsilon and adding a copy causes confusion
            #tree_copy = copy.deepcopy(d.get_last_tree())
            #d.add_tree(tree_copy)

            # Compute derivations for B production rules
            derivations_2 = B(input_tokens,d)

            for d2 in derivations_2:
                if d2.get_validity() == False:
                    result_derivations.append(d2)
                else:
                    # After checking AB, make sure there are no excessive tokens
                    if (input_tokens[d2.get_cursor()] != "%"):
                        d2.set_validity(False)
                        d2.set_reason("INVALID - doesn't derive entire input")
                    result_derivations.append(d2)

    truncated_derivations = []

    for d in result_derivations:
        truncated_derivations.append(d)
        if d.get_validity():
            break
    
    return truncated_derivations
                    
def A(input_tokens, derivation):
    # A -> aA | _

    result_derivations = []

    # Compute first prod. rule derivations
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = A1(input_tokens, tree_copy)

    # Concatenate copy of input with first deriv. then append all
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

def A1(input_tokens, tree):
    # A -> aA

    result_derivations = []

    # Add children nodes a & A and construct derivation
    childa = TreeNode("a",True)
    childA = TreeNode("A",False)
    tree.get_current().add_children([childa,childA])
    derivation = Derivation(tree)

    # Check if token is a
    if (input_tokens[derivation.get_cursor()] != "a"):
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected 'a'")
        return [derivation]
    
    # Add copy of tree to derivation with cursor +1
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    tree_copy.increment_cursor()
    derivation.add_tree(tree_copy)

    # Compute A derivations
    derivations = A(input_tokens, derivation)

    for d in derivations:
        result_derivations.append(d)

    return result_derivations

def B(input_tokens, derivation):
    # B -> bB | _

    result_derivations = []

    # Compute first prod. rule derivations
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = B1(input_tokens, tree_copy)

    # Concatenate copy of input with first deriv. then append all
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

def B1(input_tokens, tree):
    # B -> bB

    result_derivations = []

    # Add children nodes b & B and construct derivation
    childb = TreeNode("b",True)
    childB = TreeNode("B",False)
    tree.get_current().add_children([childb,childB])
    derivation = Derivation(tree)

    # Check if token is b
    if (input_tokens[derivation.get_cursor()] != "b"):
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected 'b'")
        return [derivation]
    
    # Add copy of tree to derivation with cursor +1
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    tree_copy.increment_cursor()
    derivation.add_tree(tree_copy)

    # Compute B derivations
    derivations = B(input_tokens, derivation)

    for d in derivations:
        result_derivations.append(d)

    return result_derivations