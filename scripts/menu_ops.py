from logging import PlaceHolder
import numpy as np
import pygame as pyg
from matrix_ops import MOPS
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

mops = MOPS()

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
        
        # menu grid variables
        self.rows = grid_rows
        self.columns = grid_columns
        self.grid_coords = np.zeros((self.rows + 1, self.columns + 1, 2))
        
        self.title = Button(self.scrn, 0, 0, 0, 0, text=self.name, fontSize=25, margin=3, radius=4)
        self.title._hidden = True
        self.title._disabled = True
        
    def update_menu_title(self):
        # make title visible
        if self.title._hidden:
            self.title._hidden = False
        
        # get title position and width
        title_x = self.grid_coords[self.nm_row_span[0], self.nm_col_span[0], 0]
        title_y = self.grid_coords[self.nm_row_span[0], self.nm_col_span[0], 1]

        self.title._x = title_x
        self.title._y = title_y
        # height and width are calculated by finding x and y distances of bounding grid boxes
        self.title._width = self.grid_coords[self.nm_row_span[1], self.nm_col_span[1] + 1, 0] - title_x # plus one allows grabbing of the point to the right in order to match span meaning
        self.title._height = self.grid_coords[self.nm_row_span[1] + 1, self.nm_col_span[1], 1] - title_y

        
    def run(self, menu_shape):
        # update dimensions
        self.dimensions = menu_shape
        
        # update grid coordinates
        grid_box_width = (menu_shape[2]/self.columns)
        grid_box_height = (menu_shape[3]/self.rows)
        # calculate the x and y coordinates. the range goes from the top_left point to the: top_left + width for the x, and top_left + height for the y
        x_coords = list(np.arange(menu_shape[0], menu_shape[0] + menu_shape[2] + 1, grid_box_width))
        y_coords = list(np.arange(menu_shape[1], menu_shape[1] + menu_shape[3] + 1, grid_box_height))
        
        print(x_coords, y_coords, sep = ", ")
        # fill the grid coord matrix
        for row in range(self.grid_coords.shape[0]):
            for col in range(self.grid_coords.shape[1]):
                self.grid_coords[row, col, 0] = x_coords[col]
                self.grid_coords[row, col, 1] = y_coords[row]
                # pyg.draw.circle(self.scrn, (0, 0, 0), (x_coords[col], y_coords[row]), 2)
                
        # round each coordinate float point to an integer
        self.grid_coords = self.grid_coords.astype(int)
        
        # draw menu background
        pyg.draw.rect(self.scrn, self.bg_color, tuple(self.dimensions))
        
        self.update_menu_title()
        

        
        