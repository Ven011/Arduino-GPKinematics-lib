"""
This script serves to conduct any matrix opetations that need to be done in order to render the workspace
and robotic arm or to retrieve any information about the workspace or arm.
"""

import numpy as np
import pygame as pyg
import pygame.gfxdraw as pyg_gfx
from math import *
from math import pi

class MOPS():
    def __init__(self):
        self.angle = 0
    
        # used to project 3D points (x, y, z) to 2D points (x, y)
        self.projection_matrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        
        self.prev_theta =   1
        self.prev_alpha =   1
        self.prev_sigma =   1
        self.theta =        0   # x angle of the center point
        self.alpha =        0   # y angle of the center point
        self.sigma =        0   # z axis angle of the center point
        
        # Displacement vectors
        self.V_Z =      np.zeros((3, 1))   
        self.V_Y =      np.zeros((3, 1))   
        self.V_X =      np.zeros((3, 1))   
        
        self.LZ =       200  # length from z axis endpoint to center point
        self.LY =       200
        self.LX =       200
        
        # used to draw axis lines
        self.projected_points = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.ws_points = [[0, 0], [0, 0], [0, 0], [0, 0]]
        
    def refresh_workspace(self):
        """
        Decides whether to recalculate the workspace axes and plane points
        """
        if self.prev_theta == self.theta and self.prev_sigma == self.sigma and self.prev_alpha == self.alpha:
            return False
        else:
            return True
        
    def connect_points(self, i, j, points, scrn, color):
        pyg.draw.line(scrn, color, (points[i][0], points[i][1]), (points[j][0], points[j][1]))
        
    def project_workspace(self, points, width, height, scrn):  
        i = 0
        for point in points:
            # turn 3D points into 2D points
            projected3D = np.dot(self.projection_matrix, point.reshape((3, 1)))
            
            x = int(projected3D[0][0])
            y = int(projected3D[1][0])
            
            self.projected_points[i] = [x, y]
            self.projected_points[i + 4] = [(width/2) - (x - (width/2)), (height/2) - (y - (height/2))]
            i += 1
            
                # calculate workspace plane points. Used the concepts of parallel lines and distance
        # x,y point
        self.ws_points[0][0] = self.projected_points[2][0] - (self.projected_points[0][0] - self.projected_points[3][0])
        self.ws_points[0][1] = self.projected_points[2][1] - (self.projected_points[0][1] - self.projected_points[3][1])
        # -x,y point
        self.ws_points[2][0] = self.projected_points[6][0] - (self.projected_points[0][0] - self.projected_points[7][0])
        self.ws_points[2][1] = self.projected_points[6][1] - (self.projected_points[0][1] - self.projected_points[7][1])
        # -x,-y
        self.ws_points[1][0] = self.projected_points[3][0] + (self.projected_points[0][0] - self.projected_points[2][0])
        self.ws_points[1][1] = self.projected_points[3][1] + (self.projected_points[0][1] - self.projected_points[2][1])
        # x,-y
        self.ws_points[3][0] = self.projected_points[7][0] + (self.projected_points[0][0] - self.projected_points[6][0])
        self.ws_points[3][1] = self.projected_points[7][1] + (self.projected_points[0][1] - self.projected_points[6][1])
        
        self.prev_theta = self.theta
        self.prev_alpha = self.alpha
        self.prev_sigma = self.sigma
           
        # draw axes lines 
        self.connect_points(0, 1, self.projected_points, scrn, (0, 0, 255)) # draws z axis
        self.connect_points(0, 2, self.projected_points, scrn, (0, 255, 0)) #       y
        self.connect_points(0, 3, self.projected_points, scrn, (255, 0, 0)) #       x
        self.connect_points(0, 5, self.projected_points, scrn, (0, 0, 255)) # draws neg z axis
        self.connect_points(0, 6, self.projected_points, scrn, (0, 255, 0)) #           y
        self.connect_points(0, 7, self.projected_points, scrn, (255, 0, 0)) #           x
        
        # draw workspace plane
        pyg_gfx.filled_polygon(scrn, [(x, y) for x, y in self.ws_points], (0, 0, 0, 50))
    
    def get_z_endpoint(self, width, height):
        self.calc_DVs()
        # return the x, y, z coordinate of the Z endpoint
        return np.matrix([self.V_Z[0, 0] + width/2, self.V_Z[1, 0] + height/2, self.V_Z[2, 0]])
    
    def get_y_endpoint(self, width, height):
        self.calc_DVs()
        # return the x, y, z coordinate of the Y endpoint
        return np.matrix([self.V_Y[0, 0] + width/2, self.V_Y[1, 0] + height/2, self.V_Y[2, 0]])
    
    def get_x_endpoint(self, width, height):
        self.calc_DVs()
        # return the x, y, z coordinate of the X endpoint
        return np.matrix([self.V_X[0, 0] + width/2, self.V_X[1, 0] + height/2, self.V_X[2, 0]])

    def calc_DVs(self):
        # calculate the displacement vector for the Z axis endpoint
        self.V_Z[0, 0] = self.LZ * sin(self.alpha)
        self.V_Z[1, 0] = self.LZ * -sin(self.theta)
        self.V_Z[2, 0] = self.LZ * cos(self.alpha) * cos(self.theta)
        
        # calculate the displacement vector for the Y axis endpoint
        self.V_Y[0, 0] = self.LY * -sin(self.sigma)
        self.V_Y[1, 0] = self.LY * cos(self.sigma) * cos(self.theta)
        self.V_Y[2, 0] = self.LY * sin(self.theta) 
        
        # calculate the displacement vector for the X axis endpoint
        self.V_X[0, 0] = self.LX * cos(self.alpha) * cos(self.sigma)
        self.V_X[1, 0] = self.LX * sin(self.sigma)
        self.V_X[2, 0] = self.LX * -sin(self.alpha)
        
class Grid():
    def __init__(self, grid_rows, grid_columns):
        # grid attributes
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        
        # grid variables
        self._rows = grid_rows
        self._columns = grid_columns
        
    def get_map(self):
        """
        Calculates and returns a grid net/map of using the desired grid attributes

        Returns:
            np.array: (rows + 1, columns + 1, 2) shaped grid map with x and y points of each grid intersection point
        """
        
        # create grid map template
        grid_coordinates = np.zeros((self._rows + 1, self._columns + 1, 2))
        
        # calculate grid box width and height - will be used to determine grid "net" coordinates
        grid_box_width = (self._width / self._columns)
        grid_box_height = (self._height / self._rows)
        
        # get grid net x and y coordinates
        x_coords = list(np.arange(self._x, (self._x + self._width + 1), grid_box_width))    # (+1) ensures we are including the x + width point as a possible coordinate point
        y_coords = list(np.arange(self._y, (self._y + self._height + 1), grid_box_height))
        
        # fill the grid coordinate matrix with the points
        for row in range(grid_coordinates.shape[0]):
            for col in range(grid_coordinates.shape[1]):
                grid_coordinates[row, col, 0] = x_coords[col]
                grid_coordinates[row, col, 1] = y_coords[row]
                
        # round each coordinate float point to an integer
        grid_coordinates = grid_coordinates.astype(int)
        
        return grid_coordinates
    
    def get_span(self, row_span = [0, 0], col_span = [0, 0]):
        """
        Returns the x, y coordinate, width, and height of the entered grid span

        Args:
            row_span (list, optional): first and last row of the span. Defaults to [0, 0].
            col_span (list, optional): first and last column of the span. Defaults to [0, 0].

        Returns:
            list: the span's top left (x, y), width and height
        """
        
        # calculate the current map
        map = self.get_map()
        
        # grab the x and y coordinates of the top left point of the spans
        topLeftx = map[row_span[0], col_span[0], 0]
        topLefty = map[row_span[0], col_span[0], 1]
        
        # calculate the width and height of the spans. 
        width = map[row_span[1], col_span[1] + 1, 0] - topLeftx
        height = map[row_span[1] + 1, col_span[1], 1] - topLefty
        
        return [topLeftx, topLefty, width, height]
        
    
    def update_attributes(self, grid_dimensions):
        """
        Updates grid attributes

        Args:
            grid_dimensions (list): [topleft_X, topleft_Y, width, height]
        """
        self._x, self._y, self._width, self._height = grid_dimensions
    
    

    
    
        
        
        
            
            
            
            