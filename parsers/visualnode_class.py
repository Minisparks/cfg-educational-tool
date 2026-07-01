import pygame
from pygame.locals import *
import sys

class VisualNode:
    def __init__(self, token, x_position, y_position, is_terminal, is_leaf):
        self._token = token
        self._position = (x_position,y_position)
        self._is_terminal = is_terminal
        self._is_leaf = is_leaf
        self._is_bold = False
        self._is_target = False
    
    def make_bold(self):
        self._is_bold = True

    def get_is_bold(self):
        return self._is_bold

    def make_target(self):
        self._is_target = True

    def get_is_terminal(self):
        return self._is_terminal

    def get_is_leaf(self):
        return self._is_leaf

    def get_token(self):
        return self._token

    def draw(self, surface, target_color_override=None):
        font = pygame.font.SysFont('Corbel', 25, self._is_bold, False)
        color = (1,1,1)
        if self._is_target:
            color = (200,150,0)
            if not target_color_override is None:
                color = target_color_override
            text = font.render(self._token, True, color)
        elif self._is_bold:
            color = (0,200,0)
            text = font.render(self._token, True, color)
        else:
            text = font.render(self._token, True, color)
        
        sizex,sizey = font.size(self._token)
        sizex += 10
        rectx, recty = self._position[0]-(sizex*0.5), self._position[1]-(sizey*0.5)
        pygame.draw.rect(surface, color, pygame.Rect(rectx,recty,sizex,sizey),width=2,border_radius=5)
        surface.blit(text, text.get_rect(center=self._position))