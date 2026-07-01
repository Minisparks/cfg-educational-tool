import pygame
from pygame.locals import *
from abc import ABC,abstractmethod
import sys
from button_class import Button
from textinput_class import TextInput
from parsers import topic1parser,topic2parser,topic3parser,topic4parser,topic5parser
from parsers.visualnode_class import VisualNode
from information_classes import Topic1,Topic2,Topic3,Topic4,Topic5



"""
Class to control and swap current scenes
"""
class Manager:
    def __init__(self):
        pygame.init()
        self._surface = pygame.display.set_mode((1600,900))
        self._current_scene = MenuScene(self,self._surface)
        self._running = True


    def run(self):
        """
        Loop, calling current scene's functions
        """

        self._current_scene.on_init()
        while (self._running and self._current_scene is not None):
            for event in pygame.event.get():
                self._current_scene.on_event(event)
            self._current_scene.on_loop()
            self._current_scene.on_render()


    def change_scene(self, scene_name, scene_parameter=None):
        """
        Updates current scene
        INPUTS:
            scene_name : name of scene to change to
            scene_parameter : optional additional parameter to pass into new scene. Default None
        """

        self._current_scene.on_cleanup()
        match scene_name:
            case "menu": self._current_scene = MenuScene(self, self._surface)
            case "topic1": self._current_scene = InputScene(self, self._surface, 1)
            case "topic2": self._current_scene = InputScene(self, self._surface, 2)
            case "topic3": self._current_scene = InputScene(self, self._surface, 3)
            case "topic4": self._current_scene = InputScene(self, self._surface, 4)
            case "topic5": self._current_scene = InputScene(self, self._surface, 5)
            case "derivation1": self._current_scene = DerivationScene(self, self._surface, 1, scene_parameter)
            case "derivation2": self._current_scene = DerivationScene(self, self._surface, 2, scene_parameter)
            case "derivation3": self._current_scene = DerivationScene(self, self._surface, 3, scene_parameter)
            case "derivation4": self._current_scene = DerivationScene(self, self._surface, 4, scene_parameter)
            case "derivation5": self._current_scene = DerivationScene(self, self._surface, 5, scene_parameter)
            case "info1": self._current_scene = InfoScene(self, self._surface, 1, scene_parameter)
            case "info2": self._current_scene = InfoScene(self, self._surface, 2, scene_parameter)
            case "info3": self._current_scene = InfoScene(self, self._surface, 3, scene_parameter)
            case "info4": self._current_scene = InfoScene(self, self._surface, 4, scene_parameter)
            case "info5": self._current_scene = InfoScene(self, self._surface, 5, scene_parameter)
            case "help": self._current_scene = HelpScene(self, self._surface)
            case "None":
                pygame.quit()
                pass
        self._current_scene.on_init()



"""
Abstract base class for all scenes to inherit from
Provides base functionality for on_ functions that all scenes will use
"""
class Scene(ABC):
    def __init__(self, manager, surface):
        self._surface = surface
        self._manager = manager


    @abstractmethod
    def on_init(self):
        pass
    

    @abstractmethod
    def on_event(self):
        pass


    @abstractmethod
    def on_loop(self):
        pass


    def on_render(self):
        """
        Draws background, title background and title
        """

        self._surface.fill((250,252,255))
        pygame.draw.rect(self._surface, (174,216,230), pygame.Rect(0,0,1600,90))
        self._surface.blit(self._title, self._title.get_rect(center=(800,50)))
    

    @abstractmethod
    def on_cleanup(self):
        pass
    

    def _create_text(self, text, size, color=(1,1,1), is_bold=False, is_underlined=False):
        """
        Converts string into on-screen text
        INPUTS:
            text : string to be displayed
            size : size of text on screen
            color : RGB color of the text
            is_bold : whether the text should be bold on screen. Default False
            is_underlined : whether the text should be underlined. Default False
        OUTPUTS:
            surface with rendered text
        """

        font = pygame.font.SysFont('Corbel', size, is_bold, italic=False)
        font.set_underline(is_underlined)
        return font.render(text, True, color)



class MenuScene(Scene):
    def __init__(self, manager, surface):
        Scene.__init__(self,manager,surface)
    

    def on_init(self):
        """
        Initialise title and buttons for menu scene
        """

        self._title = self._create_text('Context-Free Grammar Derivation Visualiser', size=80, color=(1,1,1), is_bold=True, is_underlined=True)
        self._header = self._create_text('Select a Topic:', size=50, color=(1,1,1), is_underlined=True)
        t1_button = Button((350,400), 1.75, 'topic1', 'topic1button')
        t2_button = Button((800,400), 1.75, 'topic2', 'topic2button')
        t3_button = Button((1250,400), 1.75, 'topic3', 'topic3button')
        t4_button = Button((575,660), 1.75, 'topic4', 'topic4button')
        t5_button = Button((1025,660), 1.75, 'topic5', 'topic5button')
        self._topic_buttons = [t1_button,t2_button,t3_button,t4_button,t5_button]


    def on_event(self, event):
        """
        Handle pygame events
        INPUT:
            event : event to handle
        EVENTS:
            QUIT : application closure
        """

        if event.type == pygame.QUIT:
            self._manager.change_scene("None")


    def on_loop(self):
        """
        Check if menu buttons have been pressed, changing scene if so
        """

        for button in self._topic_buttons:
            pressed,scene_name = button.check_if_clicked()
            if pressed:
                self._manager.change_scene(scene_name)
                break


    def on_render(self):
        """
        Render title and buttons
        """

        super().on_render()

        self._surface.blit(self._header, self._header.get_rect(center=(800,210)))
        for button in self._topic_buttons:
            button.draw(self._surface)
        pygame.display.flip()


    def on_cleanup(self):
        pass



class InputScene(Scene):
    def __init__(self,manager,surface,topic_number):
        Scene.__init__(self,manager,surface)
        self._topic_number = topic_number


    def on_init(self):
        """
        Initialise title, rules, prompt, input and buttons
        """

        # Select corresponding 'container' that contains title, rules etc for topic
        match self._topic_number:
            case 1: info_container = Topic1
            case 2: info_container = Topic2
            case 3: info_container = Topic3
            case 4: info_container = Topic4
            case 5: info_container = Topic5
        
        # Extract information from container 
        self._title = info_container.title
        self._rules = info_container.rules
        self._prompt = info_container.prompt
        self._info = info_container.pre_derivation_information

        self._help_button = Button((1555,45), 5, 'help', 'infobutton')
        self._back_button = Button((45,45), 1.7, 'menu', 'backbutton')
        self._input_box = TextInput((850,780))

        
    def on_event(self,event):
        """
        Handle pygame events
        INPUTS:
            event : event to handle
        EVENTS:
            QUIT : Application closure
            KEYDOWN (Enter) : User presses enter to enter string for derivation
            KEYDOWN (Other) : User presses character key to input string
        """

        if event.type == pygame.QUIT:
            self._manager.change_scene("None")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Change to corresponding derivation scene, passing user input
                scene = "derivation" + str(self._topic_number)
                self._manager.change_scene(scene, scene_parameter=self._input_box.get_text())
            else:
                # Character key handled by input box object
                self._input_box.handle_keydown(event)


    def on_loop(self):
        """
        Check if buttons pressed, changing scene if so
        """

        pressed,scene_name = self._back_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)

        pressed,scene_name = self._help_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)


    def on_render(self):
        """
        Render title, rules, input and buttons
        """

        super().on_render()

        # Reder the info for the topic
        y = 130
        for line in self._info:
            self._surface.blit(line,line.get_rect(topleft=(35,y)))
            y += 30

        # Render middle divider
        pygame.draw.line(self._surface, [1,1,1], (800,120), (800,870), 2)

        # Render production rules with seperation of 30 between lines
        header = self._create_text("Production Rules:", size=40, color=(1,1,1), is_bold=True, is_underlined=True)
        self._surface.blit(header, header.get_rect(topleft=(850,120)))
        y = 180
        for rule in self._rules:
            self._surface.blit(rule,rule.get_rect(topleft=(850,y)))
            y += 30
        
        # Render other elements
        self._surface.blit(self._prompt,self._prompt.get_rect(topleft=(900,755)))
        self._input_box.draw(self._surface)
        self._back_button.draw(self._surface)
        self._help_button.draw(self._surface)

        pygame.display.flip()


    def on_cleanup(self):
        pass



class DerivationScene(Scene):
    def __init__(self, manager, surface, topic_number, input_string):
        Scene.__init__(self,manager,surface)
        self._input_string = input_string
        self._topic_number = topic_number
        self._trees = []
        self._derivations = []
        self._tree_number = 0
        self._number_of_valid_derivations = 0


    def on_init(self):
        """
        Initialise title, rules and buttons
        Also derive input
        """

        # Select corresponding parser and 'container'
        match self._topic_number:
            case 1: 
                parser = topic1parser
                info_container = Topic1
            case 2: 
                parser = topic2parser
                info_container = Topic2
            case 3: 
                parser = topic3parser
                info_container = Topic3
            case 4: 
                parser = topic4parser
                info_container = Topic4
            case 5: 
                parser = topic5parser
                info_container = Topic5

        # Extract information from container
        self._title = info_container.title
        self._rules = info_container.small_rules

        self._control_info = [
                    self._create_text("Left Arrow Key:     Previous Step", size=20, color=(1,1,1), is_bold=True),
                    self._create_text("Right Arrow Key:     Next Step", size=20, color=(1,1,1), is_bold=True)
                ]
        self._help_button = Button((1555,45), 5, 'help', 'infobutton')
        self._back_button = Button((45,45), 1.7, 'topic'+str(self._topic_number), 'backbutton')
        self._finish_button = None

        # Derive input and generate list of trees (as nodes and edges):
        self._derivations = parser.derive(self._input_string)

        for derivation in self._derivations:

            # For each tree, convert it into [nodes,edges,comment] 
            trees = derivation.get_trees()
            for tree in trees:
                nodes,edges = tree.generate_visual_nodes_and_edges()
                comment = ''
                self._trees.append([nodes,edges,comment])

            # Repeat final tree of derivation with added comment
            nodes,edges = derivation.get_last_tree().generate_visual_nodes_and_edges()
            if derivation.get_validity() == False:
                comment = derivation.get_reason()
            else:
                comment = "VALID : correct derivation"
                self._number_of_valid_derivations += 1
            self._trees.append([nodes,edges,comment])

            # Repeat final tree with '<< BACKTRACKING <<' comment
            nodes,edges = derivation.get_last_tree().generate_visual_nodes_and_edges()
            comment = "<< BACKTRACKING <<"
            self._trees.append([nodes,edges,comment])

        # Remove last backtracking comment and tree
        self._trees.pop()
        
        # Add empty tree at end with final comment
        nodes = []
        edges = []
        comment = 'COMPLETE'
        self._trees.append([nodes,edges,comment])

        # Determine route the InfoScene will take
        if self._topic_number in [1,4,5]:
            # Route determined by whether valid derivation count is 0 or 1 (for topics 1,4)
            self._route = self._number_of_valid_derivations + 1
        elif self._topic_number == 2:
            # Route determined by whether tokens are correct and based on number of valid derivations

            input_tokens = list(self._input_string)
            error=False
            for token in input_tokens:
                if token != "(" and token != ")":
                    error=True
            
            if error:
                # Route for invalid token
                self._route = 3
            else:
                # Otherwise route 1 or 2 based on number of valid derivations
                self._route = self._number_of_valid_derivations + 1
        elif self._topic_number == 5:
            # Route based on no. valid derivations (capped at 3)
            self._route = self._number_of_valid_derivations + 1
            if self._route > 3:
                self._route = 3
        else:
            # Route always 1
            self._route = 1


    def on_event(self, event):
        """
        Handle pygame events
        INPUT:
            event : event to handle
        EVENTS:
            QUIT : application closure
            KEYDOWN (LEFT/RIGHT) : user goes back and forth through derivation
        """

        if event.type == pygame.QUIT:
            self._manager.change_scene("None")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._tree_number = min(self._tree_number + 1, len(self._trees) - 1)
            elif event.key == pygame.K_LEFT:
                self._tree_number = max (self._tree_number - 1, 0)
    

    def on_loop(self):
        """
        Check if buttons have been pressed, changing scene if so
        """

        pressed,scene_name = self._back_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)

        if self._finish_button is not None:
            pressed,scene_name = self._finish_button.check_if_clicked()
            if pressed:
                self._manager.change_scene(scene_name, self._route)
        
        pressed,scene_name = self._help_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)


    def on_render(self):
        """
        Render title, rules, buttons and tree
        """

        super().on_render()

        # Render production rules on left side
        rules_heading = self._create_text('Production Rules:', size=20, color=(1,1,1), is_bold=True, is_underlined=True)
        self._surface.blit(rules_heading, rules_heading.get_rect(topleft=(35,130)))
        y = 170
        for rule in self._rules:
            self._surface.blit(rule,rule.get_rect(topleft=(50,y)))
            y += 17
        pygame.draw.line(self._surface, [1,1,1], (500,100), (500,785), 2)

        # Render controls
        controls_heading = self._create_text('Controls:', size=20, color=(1,1,1), is_bold=True, is_underlined=True)
        self._surface.blit(controls_heading, controls_heading.get_rect(topleft=(35,y+51)))
        y += 75
        for line in self._control_info:
            self._surface.blit(line,line.get_rect(topleft=(50,y)))
            y += 25

        count = 0 #Used to count how many non-ε terminals are in the tree for use in rendering input string in segments

        # Render tree
        nodes,edges,comment = self._trees[self._tree_number]

        for node in nodes:

            # If the tree is showing an invalid derivation, draw nodes with a red 'target' node instead of default
            if comment.find("INVALID") != -1:
                node.draw(self._surface, target_color_override=(200,0,0))
            else:
                node.draw(self._surface)

            # Increment count if non-ε, accepted terminal node
            if node.get_token() != 'ε' and node.get_is_terminal() and node.get_is_bold():
                count += 1

        for edge in edges:
            edge.draw(self._surface)

        comment_text = self._create_text(comment, size=25, color=(1,1,1), is_bold=True)
        self._surface.blit(comment_text, comment_text.get_rect(center=(1050,825)))
        pygame.draw.line(self._surface, [1,1,1], (500,785), (1600,785), 2)

        # Render input string
        # Tokenise user input
        if self._topic_number in [1,2,4]: 
            derived_string = list(self._input_string)
            spacer = ''
        else: 
            derived_string = self._input_string.split()
            spacer = ' '
        
        # Seperate accepted tokens, current token and unprocessed tokens
        accepted_tokens = ''
        for i in range(0,count):
            accepted_tokens = accepted_tokens +spacer+ str(derived_string[i])

        if count<len(derived_string): current_token = str(derived_string[count])
        else: current_token = ''

        unprocessed_tokens = ''
        for i in range(count+1,len(derived_string)):
            unprocessed_tokens = unprocessed_tokens +spacer+ str(derived_string[i])

        # Render as string below tree
        string_to_print = "Accepted: [" + accepted_tokens + "]       Current: [" + current_token + "]       Unprocessed: [" + unprocessed_tokens + "]"
        if comment.find("COMPLETE") != -1: string_to_print = ''
        string_to_print = self._create_text(string_to_print, size=18, color=(1,1,1), is_bold=True)
        self._surface.blit(string_to_print, string_to_print.get_rect(center=(1050,875)))

        # Render buttons
        self._back_button.draw(self._surface)
        self._help_button.draw(self._surface)

        # Only render finish button when derivation complete
        if comment.find("COMPLETE") != -1:
            self._finish_button = Button((250,850), 1, 'info'+str(self._topic_number), 'nextbutton')
            self._finish_button.draw(self._surface)
        else:
            self._finish_button = None

        pygame.display.flip()


    def on_cleanup(self):
        pass



class InfoScene(Scene):
    def __init__(self, manager, surface, topic_number, route):
        Scene.__init__(self, manager, surface)
        self._topic_number = topic_number
        self._route = route


    def on_init(self):
        """
        Initialise information attributes and buttons based on route and topic
        """
        
        match self._topic_number:
            case 1: info_container = Topic1
            case 2: info_container = Topic2
            case 3: info_container = Topic3
            case 4: info_container = Topic4
            case 5: info_container = Topic5
        
        # Extract information from container
        self._title = info_container.title
        self._header = info_container.post_derivation_headers[self._route -1]
        match self._route:
            case 1: self._info = info_container.post_derivation_information_1
            case 2: self._info = info_container.post_derivation_information_2
            case 3: self._info = info_container.post_derivation_information_3
        self._rules = info_container.small_rules

        self._repeat_button = Button((1375,550), 1.7, "topic"+str(self._topic_number), "repeatbutton")
        self._menu_button = Button((1375,750), 1.7, "menu", "finishbutton")
        self._help_button = Button((1555,45), 5, 'help', 'infobutton')


    def on_event(self, event):
         if event.type == pygame.QUIT:
            self._manager.change_scene("None")


    def on_loop(self):
        """
        Check if buttons pressed, changing scene if so
        """

        pressed,scene_name = self._menu_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)

        pressed,scene_name = self._repeat_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)

        pressed,scene_name = self._help_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)


    def on_render(self):
        """
        Render buttons and info elements
        """

        super().on_render()

        # Render info box
        pygame.draw.rect(self._surface, (1,1,1), pygame.Rect(50,140,1100,710), 2)

        # Render sub_header
        self._surface.blit(self._header, self._header.get_rect(center=(575,175)))

        # Render info
        y = 220
        for line in self._info:
            self._surface.blit(line,line.get_rect(topleft=(150,y)))
            y += 27

        # Render production rules on right side
        rules_heading = self._create_text('Production Rules:', size=20, color=(1,1,1), is_bold=True, is_underlined=True)
        self._surface.blit(rules_heading, rules_heading.get_rect(topleft=(1225,140)))
        y = 175
        for rule in self._rules:
            self._surface.blit(rule,rule.get_rect(topleft=(1225,y)))
            y += 25

        # Render buttons
        self._menu_button.draw(self._surface)
        self._repeat_button.draw(self._surface)
        self._help_button.draw(self._surface)

        pygame.display.flip()


    def on_cleanup(self):
        pass



class HelpScene(Scene):
    def __init__(self, manager, surface):
        Scene.__init__(self, manager, surface)

    
    def on_init(self):
        """
        Initialise text box with key definitions, and buttons
        """

        self._title = self._create_text("Key Definitions", size=80, is_bold=True, is_underlined=True)
        self._info = [
            self._create_text("Non-Terminal:", size=30, is_bold=True, is_underlined=True),
            self._create_text("         A symbol which is replaced in a derivation according to it's production rules.", size=30),
            self._create_text("", size=30),
            self._create_text("Terminal:", size=30, is_bold=True, is_underlined=True),
            self._create_text("         A symbol which is NOT replaced and appears in the language.", size=30),
            self._create_text("", size=30),
            self._create_text("Start Variable:", size=30, is_bold=True, is_underlined=True),
            self._create_text("         The non-terminal you start with in a derivation.", size=30),
            self._create_text("", size=30),
            self._create_text("Production Rule (->):", size=30, is_bold=True, is_underlined=True),
            self._create_text("         Defines how the non-terminal can be replaced during derivation.", size=30),
            self._create_text("", size=30),
            self._create_text("Derivation (->*):", size=30, is_bold=True, is_underlined=True),
            self._create_text("         A series of applied production rules from one sequence to another.", size=30)
        ]
        self._menu_button = Button((45,45), 1.7, "menu", "backbutton")


    def on_event(self, event):
         if event.type == pygame.QUIT:
            self._manager.change_scene("None")


    def on_loop(self):
        """
        Check if buttons pressed, chaning scene if so
        """

        pressed,scene_name = self._menu_button.check_if_clicked()
        if pressed:
            self._manager.change_scene(scene_name)


    def on_render(self):
        """
        Render buttons and text box
        """

        super().on_render()

        # Render title
        self._surface.blit(self._title, self._title.get_rect(center=(800,50)))

        # Render info box
        pygame.draw.rect(self._surface, (1,1,1), pygame.Rect(150,140,1300,710), 2)

        # Render info
        y = 200
        for line in self._info:
            self._surface.blit(line,line.get_rect(topleft=(300,y)))
            y += 40

        # Render buttons
        self._menu_button.draw(self._surface)

        pygame.display.flip()


    def on_cleanup(self):
        pass