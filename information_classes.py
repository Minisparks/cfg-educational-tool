import pygame
from pygame.locals import *
import sys

def create_text(text, size, color=(1,1,1),is_bold=False, is_underlined=False, is_italics=False):
    if not pygame.get_init():
        pygame.init()
    font = pygame.font.SysFont('Corbel', size, is_bold, is_italics)
    font.set_underline(is_underlined)
    return font.render(text, True, color)

class Topic1:
    title = create_text('Topic One - Introduction to CFGs', size=80, is_bold=True, is_underlined=True)
    rules = [
                create_text('S -> AB', size=30, is_bold=True),
                create_text('', size=30),
                create_text('A -> aA | ε', size=30, is_bold=True),
                create_text('', size=30),
                create_text('B -> bB | ε', size=30, is_bold=True)
            ]
    prompt = create_text('Enter a string that can be derived from the language above:', size=25)
    small_rules = [
                create_text('S -> AB', size=20, is_bold=True),
                create_text('', size=20),
                create_text('A -> aA | ε', size=20, is_bold=True),
                create_text('', size=20),
                create_text('B -> bB | ε', size=20, is_bold=True)
            ]
    pre_derivation_information = [
                create_text("Context Free Grammars (CFGs) are a way of defining a language.", size=25, is_bold=True),
                create_text("", size=25),
                create_text("How To Read:", size=25, is_bold=True),
                create_text("1. Start variable:", size=25),
                create_text("           The non-terminal we start our derivations with.", size=25),
                create_text("           We use the non-terminal 'S' here.", size=25),
                create_text("2. Production rules:", size=25),
                create_text("           The left hand side of the rule is the non-terminal that is replaced.", size=25),
                create_text("           The right hand side shows what the left can be replaced by.", size=25),
                create_text("           Each rule seperated by a '|'.", size=25),
                create_text("3. The empty string", size=25),
                create_text("           'ε' represents the empty string.", size=25),
                create_text("", size=25),
                create_text("To determine if a given word is in the language, we use a parser.", size=25, is_bold=True),
                create_text("We use a 'Recursive Descent Parser'.", size=25, is_bold=True),
                create_text("How It Works:", size=25, is_bold=True),
                create_text("1. Start with the start variable, S.", size=25),
                create_text("2. Replace the leftmost non-terminal with it's first production rule.", size=25),
                create_text("3. Repeat until the leftmost token is a terminal.", size=25),
                create_text("3. If that token matches withi the input, accept that token, if not backtrack", size=25),
                create_text("and try the next rule.", size=25),
                create_text("4. If the parser matches all tokens of the input, the word is accepted.", size=25),
                create_text("", size=25),
                create_text("Now, practice with the CFG on the right...", size=25, is_bold=True),
            ]
    post_derivation_headers = [
                create_text("String Not Accepted!", size=35, is_bold=True, is_underlined=True),
                create_text("String Accepted!", size=35, is_bold=True, is_underlined=True)
            ]
    post_derivation_information_1 = [
                create_text("The string you entered is not part of the defined language.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Use what you learnt from the derivation to understand why it was not accepted,", size=25, is_bold=True),
                create_text("then try again with a string that will be accepted...", size=25, is_bold=True),
            ]
    post_derivation_information_2 = [
                create_text("Well Done!", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("This grammar represents the language:", size=25, is_bold=True),
                create_text("       Strings of zero or more 'a's followed by zero or more 'b's", size=25),
                create_text("", size=25, is_bold=True),
                create_text("This is equivalent to the regular expression:", size=25, is_bold=True),
                create_text("       a*b*", size=25,),
                create_text("", size=25, is_bold=True),
                create_text("So why don't we just use regular expressions?", size=25, is_bold=True),
                create_text("       Complete the next topic to find out...", size=25)
            ]

class Topic2:
    title = create_text('Topic Two - Usefulness of CFGs', size=80, is_bold=True, is_underlined=True)
    rules = [
                create_text('S -> (S) | ε', size=30, is_bold=True),

            ]
    prompt = create_text('Experiment with how CFGs can be used for recursive structures:', size=25)
    small_rules = [
                create_text('S -> (S) | ε', size=20, is_bold=True),

            ]
    pre_derivation_information = [
                create_text("The main benefit of CFGs is that they can express recursive structures.", size=25, is_bold=True),
                create_text("Regular expressions cannot do this.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Recursive Structures:", size=25, is_bold=True),
                create_text("       A recursive structure is one whose definition may include itself.", size=25),
                create_text("", size=25, is_bold=True),
                create_text("An example of a recursive structure can be seen on the right:", size=25, is_bold=True),
                create_text("       'N opening brackets followed by N closing brackets'", size=25),
                create_text("       This is recursive as one set of brackets may contain another", size=25),
                create_text("       set, which may also contain another set, and so on...", size=25),
                create_text("", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Enter some strings on the right to see how the parser reacts", size=25, is_bold=True),
                create_text("to both balanced and imbalanced brackets...", size=25, is_bold=True),
            ]
    post_derivation_headers = [
                create_text("String Has Imbalanced Brackets!", size=35, is_bold=True, is_underlined=True),
                create_text("String Has Balanced Brackets!", size=35, is_bold=True, is_underlined=True),
                create_text("Unexpected Character in String!", size=35, is_bold=True, is_underlined=True)
            ]
    post_derivation_information_1 = [
                create_text("The entered string has an inequal number of opening and closing brackets, so the", size=25, is_bold=True),
                create_text("input was not accepted.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("If you haven't already, enter a string with balanced brackets...", size=25, is_bold=True)
            ]
    post_derivation_information_2 = [
                create_text("The entered string has an equal number of opening and closing brackets, so the input", size=25, is_bold=True),
                create_text("was accepted.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("If you haven't already, enter a string with imbalanced brackets...", size=25, is_bold=True),
            ]
    post_derivation_information_3 = [
                create_text("Try again only using the characters '(' and ')', as specified in the grammar...", size=25, is_bold=True),
    ]

class Topic3:
    title = create_text('Topic Three - Direct Left Recursion', size=80, is_bold=True, is_underlined=True)
    rules = [
                create_text('S -> EXP', size=30, is_bold=True),
                create_text('', size=30),
                create_text('EXP -> EXP + NUM', size=30, is_bold=True),
                create_text('              | EXP - NUM', size=30, is_bold=True),
                create_text('              | NUM', size=30, is_bold=True),
                create_text('', size=30),
                create_text('NUM -> 1|2|3|4|5|6|7|8|9|0', size=30, is_bold=True)
            ]
    prompt = create_text('Enter a string to see how the effect of left recursion:', size=25)
    small_rules = [
                create_text('S -> EXP', size=20, is_bold=True),
                create_text('', size=20),
                create_text('EXP -> EXP + NUM', size=20, is_bold=True),
                create_text('              | EXP - NUM', size=20, is_bold=True),
                create_text('              | NUM', size=20, is_bold=True),
                create_text('', size=20),
                create_text('NUM -> 1|2|3|4|5|6|7|8|9|0', size=20, is_bold=True)
            ]
    pre_derivation_information = [
                create_text("One limitation if CFGs is that they can't deal with 'Left Recursion'.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Direct Left Recursion:", size=25, is_bold=True),
                create_text("       There is a production rule such that:", size=25),
                create_text("       A -> Aa     where 'A' is a non-terminal and 'a' is some sequence.", size=25),
                create_text("", size=25, is_bold=True),
                create_text("Let's continue the derivation to see why this is bad:", size=25, is_bold=True),
                create_text("       A -> Aa -> Aaa -> Aaaa -> ...", size=25),
                create_text("       The parser makes no progress and falls into an infinte loop!", size=25),
                create_text("", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Enter a string on the right to see this in practice with a different", size=25, is_bold=True),
                create_text("grammar...", size=25, is_bold=True)
            ]
    post_derivation_headers = [
                create_text("Fallen Into Left Recursion!", size=35, is_bold=True, is_underlined=True)
            ]
    post_derivation_information_1 = [
                create_text("The issue came from the rule:", size=25, is_bold=True),
                create_text("       EXP -> EXP + NUM", size=25),
                create_text("This rule resulted in the derivation looping as follows:", size=25, is_bold=True),
                create_text("       S -> EXP -> EXP + NUM -> EXP + EXP + NUM -> EXP + EXP + EXP + NUM -> ...", size=25),
                create_text("", size=25, is_bold=True),
                create_text("To remove direct left recursion, we must rewrite our grammar:", size=25, is_bold=True),
                create_text("1. Select the left recursive production rule(s) for one non-terminal:", size=25),
                create_text("       EXP -> EXP + NUM | EXP - NUM | NUM", size=25),
                create_text("2. Make a new non-terminal:", size=25),
                create_text("       EXP'", size=25),
                create_text("3. Ignore each recursive rule and concatenate the new non-terminal on the remaining rules:", size=25),
                create_text("       EXP -> NUM EXP'", size=25),
                create_text("4. Create a set of production rules for the new non-terminal. These rules will be the ignored", size=25),
                create_text("rules from before, without the leftmost non-terminal, concatenated with the new non-terminal.", size=25),
                create_text("The final rule will be ε.", size=25),
                create_text("       EXP' -> + NUM EXP' | - NUM EXP' | ε", size=25),
                create_text("5. Repeat for all other non-terminals with left recursive rules.", size=25),
                create_text("6. The new grammar is:", size=25),
                create_text("       S -> EXP", size=25),
                create_text("       EXP -> NUM EXP'", size=25),
                create_text("       EXP' -> + NUM EXP' | - NUM EXP' | ε", size=25),
                create_text("       NUM -> 1|2|3|4|5|6|7|8|9|0", size=25)
            ]

class Topic4:
    title = create_text('Topic Four - Indirect Left Recursion', size=80, is_bold=True, is_underlined=True)
    rules = [
                create_text('S -> A', size=30, is_bold=True),
                create_text('', size=30),
                create_text('A -> a | B', size=30, is_bold=True),
                create_text('', size=30),
                create_text('B -> Ab', size=30, is_bold=True)
            ]
    prompt = create_text('Enter a string to see the effect of indirect left recursion:', size=25)
    small_rules = [
                create_text('S -> A', size=20, is_bold=True),
                create_text('', size=20),
                create_text('A -> a | B', size=20, is_bold=True),
                create_text('', size=20),
                create_text('B -> Ab', size=20, is_bold=True)
            ]
    pre_derivation_information = [
                create_text("Indirect Left Recursion:", size=25, is_bold=True),
                create_text("       There is a derivation (of >1 steps) such that:", size=25),
                create_text("       A ->* Aa    where 'A' is a non-terminal and 'a' is some sequence.", size=25),
                create_text("", size=25, is_bold=True),
                create_text("This has the same issues as direct left recursion, but can be a", size=25, is_bold=True),
                create_text("lot harder to spot.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("See if you can spot the indirect left recursion on the right, then enter", size=25, is_bold=True),
                create_text("a string which can demonstrate it...", size=25, is_bold=True),
            ]
    post_derivation_headers = [
                create_text("Fallen Into Left Recursion!", size=35, is_bold=True, is_underlined=True),
                create_text("String Accepted!", size=35, is_bold=True, is_underlined=True)
            ]
    post_derivation_information_1 = [
                create_text("The parser has timed-out since it started looping due to left recursion.", size=25, is_bold=True),
                create_text("(Progress may have been made, but due to the left recursive nature, a timeout has been applied)", size=25, is_italics=True),
                create_text("The issue came from the rules:", size=25, is_bold=True),
                create_text("       A -> B", size=25),
                create_text("       and", size=25),
                create_text("       B -> Ab", size=25),
                create_text("These rules resulted in the derivation looping as follows:", size=25, is_bold=True),
                create_text("       A -> B -> Ab -> Bb -> Abb -> ...", size=25),
                create_text("To remove left recursion, we must rewrite our grammar:", size=25, is_bold=True),
                create_text("1. For each non-terminal (X) in order...", size=25),
                create_text("2. Select a rule (X -> x) that starts with a non-terminal (Y) defined above it:", size=25),
                create_text("       B -> Ab is the first occurrence in our grammar", size=25),
                create_text("3. Remove this rule from the grammar.", size=25),
                create_text("4. Let z = x without the leading Y:", size=25),
                create_text("       b", size=25),
                create_text("5. For each rule (Y -> y) of the non-terminal Y, add the rule X -> yz:", size=25),
                create_text("       A -> a | B", size=25),
                create_text("       B -> ab | Bb", size=25),
                create_text("6. Repeat until grammar does not change, then move onto next non-terminal", size=25),
                create_text("7. Remove direct left recursion as before.", size=25),
                create_text("8. The new grammar is:", size=25),
                create_text("       S -> A      A -> a | B      B -> abB'       B' -> bB' | ε", size=25)
            ]
    post_derivation_information_2 = [
                create_text("The input was accepted by the parser.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("See if you can find an input whose validity cannot be determined due to left recursion.", size=25, is_bold=True),
            ]

class Topic5:
    title = create_text('Topic Five - Grammar Ambiguity', size=80, is_bold=True, is_underlined=True)
    rules = [
                create_text('S -> BODY', size=30, is_bold=True),
                create_text('', size=30),
                create_text('BODY -> IFEXP | body', size=30, is_bold=True),
                create_text('', size=30),
                create_text('IFEXP -> if COND then BODY', size=30, is_bold=True),
                create_text('                  | if COND then BODY else BODY', size=30, is_bold=True),
                create_text('', size=30),
                create_text('COND -> condition', size=30, is_bold=True)
            ]
    prompt = create_text('Enter a string which can be derived in two different ways:', size=25)
    small_rules = [
                create_text('S -> BODY', size=20, is_bold=True),
                create_text('', size=20),
                create_text('BODY -> IFEXP | body', size=20, is_bold=True),
                create_text('', size=20),
                create_text('IFEXP -> if COND then BODY', size=20, is_bold=True),
                create_text('                  | if COND then BODY else BODY', size=20, is_bold=True),
                create_text('', size=20),
                create_text('COND -> condition', size=20, is_bold=True)
            ]
    pre_derivation_information = [
                create_text("Ambiguity:", size=25, is_bold=True),
                create_text("       A grammar is ambiguous if it can produce two distinct parse trees for a", size=25),
                create_text("       single input.", size=25),
                create_text("", size=25, is_bold=True),
                create_text("Unlike the previous examples, we must now continue to check for", size=25, is_bold=True),
                create_text("additional valid derivations, even after we have already found one!", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Now, inspect the grammar on the right:", size=25, is_bold=True),
                create_text("       This grammar demonstrates an application of CFGs.", size=25),
                create_text("       CFGs can be used to define programming languages.", size=25),
                create_text("       This grammar is a simplification of an 'if-else' statement from a", size=25),
                create_text("       programming language.", size=25),
                create_text("       The main difference is that this grammar is ambiguous!", size=25),
                create_text("", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("See if you can figure out why this grammar is ambiguous, then enter", size=25, is_bold=True),
                create_text("an input to verify your idea...", size=25, is_bold=True),
            ]
    post_derivation_headers = [
                create_text("String Not Accepted!", size=35, is_bold=True, is_underlined=True),
                create_text("String Accepted - Only 1 Parse Tree!", size=35, is_bold=True, is_underlined=True),
                create_text("String Accepted - Ambiguous!", size=35, is_bold=True, is_underlined=True)
            ]
    post_derivation_information_1 = [
                create_text("The string you entered is not part of the language.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Recap the derivation and previous topics if needed, and see if you can find a valid string...", size=25, is_bold=True)
            ]
    post_derivation_information_2 = [
                create_text("This string is part of the language... but we can do better.", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("Some strings have more than one valid derivation. Study the grammar to see if you ", size=25, is_bold=True),
                create_text("can figure out one of these strings...", size=25, is_bold=True),
                create_text("", size=25),
                create_text("", size=25, is_bold=True),
                create_text("Hint:", size=25, is_bold=True),
                create_text("       Think about which 'if' a given 'else' statement is bound to, and whether you can make it ", size=25),
                create_text("       ambiguous.", size=25),
            ]
    post_derivation_information_3 = [
                create_text("Perfect - the string you entered was ambiguous!", size=25, is_bold=True),
                create_text("", size=25, is_bold=True),
                create_text("If you don't understand why, see this example:", size=25, is_bold=True),
                create_text("       'if condition then if condition then body else body'", size=25),
                create_text("It is not clear which 'if' the 'else' is bound to. There are two options:", size=25, is_bold=True),
                create_text("       'if condition then [if condition then body] else body'", size=25),
                create_text("       or", size=25),
                create_text("       'if condition then [if condition then body else body]", size=25),
                create_text("", size=25, is_bold=True),
                create_text("In practice:", size=25, is_bold=True),
                create_text("       Programming languages often use brackets and/or indentation to distinguish between", size=25),
                create_text("       these two possibilities.", size=25)
            ]