from logging import PlaceHolder
import numpy as np
import pygame as pyg
from matrix_ops import Grid
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

class Menu():
    def __init__(self, scrn, background_color, grid_rows = 0, grid_columns = 0, menu_title = "", title_row_span = [0, 0], title_col_span = [0, 0]):
        self.is_first = True
        
        # menu variables
        self.scrn = scrn
        self.name = menu_title
        
        self.dimensions = []
        self.bg_color = background_color
        
        self.nm_row_span = title_row_span
        self.nm_col_span = title_col_span
        
        # menu grid object and variables
        self.menu_grid = Grid(grid_rows, grid_columns)
        
        self.title = Button(self.scrn, 0, 0, 0, 0, text=self.name, fontSize=25, margin=3, radius=4, inactiveColour = (255, 255, 255))
        self.title._hidden = True
        self.title._disabled = True
   
    def run(self, menu_shape):
        # update the menu grid with the latest menu dimensions
        self.menu_grid.update_attributes(menu_shape)
        
        # draw menu background
        pyg.draw.rect(self.scrn, self.bg_color, tuple(menu_shape))
        
        # update the menu title position
        # make title visible if title is not visible
        if self.title._hidden:
            self.title._hidden = False
        self.title._x, self.title._y, self.title._width, self.title._height = self.menu_grid.get_span(self.nm_row_span, self.nm_col_span)

    
    
        
        