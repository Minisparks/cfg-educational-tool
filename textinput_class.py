import pygame
from pygame.locals import *
import sys

class TextInput:
    def __init__(self,pos):
        self.rect = pygame.Rect(pos, (700,75))
        self.rect.topleft = pos
        self.str = ''

    def get_text(self):
        return self.str

    def draw(self,surface):
        """
        Render the input box to the surface
        INPUTS:
            surface : surface to render the element on to
        """
        pygame.draw.rect(surface,(1,1,1),self.rect,1)
        font = pygame.font.SysFont('Corbel',25,False,False)
        text = font.render(self.str,True,(1,1,1))
        surface.blit(text, text.get_rect(topleft=(self.rect.left+25,self.rect.top+25)))

    def handle_keydown(self, event):
        """
        Updates object status in response to key press events
        INPUTS:
            event : key-down event to handle
        """
        alphas = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,
        pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,
        pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,
        pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,
        pygame.K_x,pygame.K_y,pygame.K_z]
        
        if event.key in alphas:
            value = pygame.key.name(event.key)
            if event.mod and pygame.KMOD_SHIFT:
                value = value.upper()
            self.str = self.str + value
        elif event.key == pygame.K_1:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '!'
            else:
                self.str = self.str + '1'
        elif event.key == pygame.K_2:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '"'
            else:
                self.str = self.str + '2'
        elif event.key == pygame.K_3:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '£'
            else:
                self.str = self.str + '3'
        elif event.key == pygame.K_4:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '$'
            else:
                self.str = self.str + '4'
        elif event.key == pygame.K_5:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '%'
            else:
                self.str = self.str + '5'
        elif event.key == pygame.K_6:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '^'
            else:
                self.str = self.str + '6'
        elif event.key == pygame.K_7:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '&'
            else:
                self.str = self.str + '7'
        elif event.key == pygame.K_8:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '*'
            else:
                self.str = self.str + '8'
        elif event.key == pygame.K_9:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '('
            else:
                self.str = self.str + '9'
        elif event.key == pygame.K_0:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + ')'
            else:
                self.str = self.str + '0'
        elif event.key == pygame.K_BACKSPACE and len(self.str) > 0:
            self.str = self.str[0:len(self.str)-1]
        elif event.key == pygame.K_RETURN:
            # next screen
            pass
        elif event.key == pygame.K_SPACE:
            self.str = self.str + ' '
        elif event.key == pygame.K_HASH:
            self.str = self.str + '#'
        elif event.key == pygame.K_QUOTE:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '@'
            else:
                self.str = self.str + "'"
        elif event.key == pygame.K_COMMA:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '<'
            else:
                self.str = self.str + ','
        elif event.key == pygame.K_MINUS:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '_'
            else:
                self.str = self.str + '-'
        elif event.key == pygame.K_PERIOD:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '>'
            else:
                self.str = self.str + '.'
        elif event.key == pygame.K_SLASH:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '?'
            else:
                self.str = self.str + '/'
        elif event.key == pygame.K_SEMICOLON:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + ':'
            else:
                self.str = self.str + ';'
        elif event.key == pygame.K_EQUALS:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '+'
            else:
                self.str = self.str + '='
        elif event.key == pygame.K_LEFTBRACKET:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '{'
            else:
                self.str = self.str + '['
        elif event.key == pygame.K_RIGHTBRACKET:
            if event.mod and pygame.KMOD_SHIFT:
                self.str = self.str + '}'
            else:
                self.str = self.str + ']'
        elif event.key == pygame.K_BACKQUOTE:
            self.str = self.str + '`'
        