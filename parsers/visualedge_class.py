import pygame
from pygame.locals import *
import sys

class VisualEdge:
    def __init__(self,start,end):
        self._start = (start[0],start[1]+15)
        self._end = (end[0],end[1]-15)
    
    def draw(self,surface):
        pygame.draw.line(surface,[1,1,1],self._start,self._end,2)