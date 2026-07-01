import pygame
from pygame.locals import *
import sys

class Button:
    def __init__(self, pos, scale, scene_name, sprite_name):
        self._img = self.init_sprite(sprite_name, scale)
        self._rect = self._img.get_rect()

        self._rect.center = pos
        self._pressed = False
        self._scene_name = scene_name

    def init_sprite(self, sprite_name, scale):
        """
        Loads and transforms the button image
        INPUTS:
            sprite_name : filename of the sprite for the image (without .png)
            scale : factor to change the size of the image by in both directions
        """
        path = 'sprites/' + sprite_name + '.png'
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))

    def draw(self, surface):
        """
        Draws button image to surface
        INPUTS:
            surface : surface to draw button to
        """

        surface.blit(self._img, self._rect.topleft)

    def check_if_clicked(self):
        """
        Check if mouse clicked on button
        OUTPUTS:
            boolean for whether button has been pressed
            scene name associated with button if button pressed ('None' if above boolean false)
        """

        if self._rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self._pressed:
            self._pressed = True
            return True,self._scene_name
        return False,'None'