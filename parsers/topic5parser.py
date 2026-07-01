from parsers.parser_classes import Derivation,ParseTree,TreeNode
import copy

# GRAMMAR:

# S -> BODY
# IFEXP -> if COND then BODY | if COND then BODY else BODY
# COND -> 'condition'
# BODY -> IFEXP | 'body'


def derive(input_string):
    # Split up input into list of tokens
    input_tokens = input_string.split()
    input_tokens.append("%")

    # Instantiate first derivation
    root_node = TreeNode("S",False)
    initial_tree = ParseTree(root_node)
    initial_derivation = Derivation(initial_tree)

    # Parse input
    return S(input_tokens, initial_derivation)

def S(input_tokens, derivation):
    # S -> BODY

    tree_copy = copy.deepcopy(derivation.get_last_tree())

    # Add BODY child node and extend derivation
    child = TreeNode("BODY", False)
    tree_copy.get_current().add_child(child)
    derivation.append_derivation(Derivation(tree_copy))

    # Get derivation list
    derivations = BODY(input_tokens, derivation)

    # Check that derivations don't have excessive tokens
    for d in derivations:
        if input_tokens[d.get_cursor()] != "%" and d.get_validity()==True:
            d.set_validity(False)
            d.set_reason("INVALID : doesn't derive entire input")

    return derivations

def BODY(input_tokens, derivation):
    # BODY -> IFEXP | body

    result_derivations = []

    # Compute first production rule derivations:
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = BODY1(input_tokens, tree_copy)

    # Concatenate input derivation with first returned derivation, then add returned derivations to result
    derivation_copy = copy.deepcopy(derivation)
    derivation_copy.append_derivation(derivations[0])
    result_derivations.append(derivation_copy)
    for i in range(1,len(derivations)):
        result_derivations.append(derivations[i])
    
    # Compute second production rule derivations:
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = BODY2(input_tokens, tree_copy)

    # Add returned derivations to result
    for i in range(0,len(derivations)):
        result_derivations.append(derivations[i])

    return result_derivations

def BODY1(input_tokens, tree):
    # BODY -> IFEXP

    result_derivations = []

    # Add IFEXP child node and construct derivation
    child = TreeNode("IFEXP", False)
    tree.get_current().add_child(child)
    derivation = Derivation(tree)

    # Compute IFEXP rule derivations
    derivations = IFEXP(input_tokens, derivation)
    for d in derivations:
        result_derivations.append(d)
    
    return result_derivations

def BODY2(input_tokens,tree):
    # BODY -> body

    # Add body child node and construct derivation
    child = TreeNode("body",True)
    tree.get_current().add_child(child)
    derivation = Derivation(tree)

    # Check if token is body
    if (input_tokens[derivation.get_cursor()] != "body"):
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected 'body'")
        return [derivation]

    # Add copy of tree to derivation with cursor increased by 1
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    tree_copy.increment_cursor()
    derivation.add_tree(tree_copy)

    return [derivation]

def COND(input_tokens,derivation):
    # COND -> condition

    tree_copy = copy.deepcopy(derivation.get_last_tree())

    # Add condition child node and extend derivation
    child = TreeNode("condition",True)
    tree_copy.get_current().add_child(child)
    derivation.append_derivation(Derivation(tree_copy))

    # Check if token is condition
    if (input_tokens[derivation.get_cursor()] != "condition"):
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected 'condition'")
    else:
        # Add copy of tree to derivation with cursor increased by 1
        tree_copy = copy.deepcopy(derivation.get_last_tree())
        tree_copy.increment_cursor()
        derivation.add_tree(tree_copy)
    
    return [derivation]

def IFEXP(input_tokens,derivation):
    # IFEXP -> if COND then BODY | if COND then BODY else BODY

    result_derivations = []

    # Compute first production rule derivations:
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = IFEXP1(input_tokens,tree_copy)

    # Concatenate copy of input with first returned derivation, then append all to result
    derivation_copy = copy.deepcopy(derivation)
    derivation_copy.append_derivation(derivations[0])
    result_derivations.append(derivation_copy)
    for i in range(1,len(derivations)):
        result_derivations.append(derivations[i])

    # Compute second production rule derivations:
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    derivations = IFEXP2(input_tokens,tree_copy)

    # Append to result
    for i in range(0,len(derivations)):
        result_derivations.append(derivations[i])

    return result_derivations

def IFEXP1(input_tokens,tree):
    # IFEXP -> if COND then BODY

    result_derivations = []

    # Add child nodes and construct derivation
    childIF = TreeNode("if",True)
    childCOND = TreeNode("COND",False)
    childTHEN = TreeNode("then",True)
    childBODY = TreeNode("BODY",False)
    tree.get_current().add_children([childIF,childCOND,childTHEN,childBODY])
    derivation = Derivation(tree)

    # Check if token is if
    if (input_tokens[derivation.get_cursor()] != "if"):
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected 'if'")
        return [derivation]

    # Add copy of tree to derivation with cursor increased by 1
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    tree_copy.increment_cursor()
    derivation.add_tree(tree_copy)

    # Compute COND derivations
    derivations = COND(input_tokens,derivation)    

    for d in derivations:
        if (not d.get_validity()):
            # Isn't valid -> add to result as is
            result_derivations.append(d)
        elif (input_tokens[d.get_cursor()] != "then"):
            # Is valid, incorrect token -> add to result as invalid
            d.set_validity(False)
            d.set_reason("INVALID : unexpected 'then'")
            result_derivations.append(d)
        else:
            # Is valid, correct token -> compute BODY derivations and add to result
            tree_copy = copy.deepcopy(d.get_last_tree())
            tree_copy.increment_cursor()
            d.add_tree(tree_copy)

            derivations_2 = BODY(input_tokens,d)

            for d2 in derivations_2:
                result_derivations.append(d2)

    return result_derivations

def IFEXP2(input_tokens,tree):
    # IFEXP -> if COND then BODY else BODY

    result_derivations = []

    # Add child nodes and construct derivation
    childIF = TreeNode("if",True)
    childCOND = TreeNode("COND",False)
    childTHEN = TreeNode("then",True)
    childBODY = TreeNode("BODY",False)
    childELSE = TreeNode("else",True)
    childBODY2 = TreeNode("BODY",False)
    tree.get_current().add_children([childIF,childCOND,childTHEN,childBODY,childELSE,childBODY2])
    derivation = Derivation(tree)

    # Check if token is if
    if (input_tokens[derivation.get_cursor()] != "if"):
        derivation.set_validity(False)
        derivation.set_reason("INVALID : unexpected 'if'")
        return [derivation]

    # Add copy of tree to derivation with cursor increased by 1
    tree_copy = copy.deepcopy(derivation.get_last_tree())
    tree_copy.increment_cursor()
    derivation.add_tree(tree_copy)

    # Compute COND derivations
    derivations = COND(input_tokens,derivation)

    for d in derivations:
        if (not d.get_validity()):
            # Is not valid -> add to result as is
            result_derivations.append(d)
        elif (input_tokens[d.get_cursor()] != "then"):
            # Is valid, incorrect token -> add to result as invalid
            d.set_validity(False)
            d.set_reason("INVALID : unexpected 'then'")
            result_derivations.append(d)
        else:
            # Valid and correct token -> continue to check tokens
            tree_copy = copy.deepcopy(d.get_last_tree())
            tree_copy.increment_cursor()
            d.add_tree(tree_copy)

            derivations_2 = BODY(input_tokens,d)

            for d2 in derivations_2:
                # As above
                if (not d2.get_validity()):
                    result_derivations.append(d2)
                elif (input_tokens[d2.get_cursor()] != "else"):
                    d2.set_validity(False)
                    d2.set_reason("INVALID : unexpected 'else'")
                    result_derivations.append(d2)
                else:
                    tree_copy = copy.deepcopy(d2.get_last_tree())
                    tree_copy.increment_cursor()
                    d2.add_tree(tree_copy)

                    derivations_3 = BODY(input_tokens,d2)

                    for d3 in derivations_3:
                        result_derivations.append(d3)

    return result_derivations