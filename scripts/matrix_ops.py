"""
This script serves to conduct any matrix opetations that need to be done in order to render the workspace
and robotic arm or to retrieve any information about the workspace or arm.
"""

import numpy as np
import pygame as pyg
import pygame.gfxdraw as pyg_gfx
from math import *
from math import pi

class Coordinate_grid():
    def __init__(self, screen, pixel_axis_length = 200, perceived_axis_length = 400, grid_rows = 10, grid_columns = 10):
        self.scrn = screen
    
        # used to project 3D points (x, y, z) to 2D points (x, y)
        self.projection_matrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        
        self.proj_center_p = []
        self.grid = []
    
        self.axis_len = perceived_axis_length    # perceived length of the axes in centimeters
        self.grid_rows = grid_rows
        self.grid_cols = grid_columns 

        self.theta =    0   # x angle of the center point
        self.alpha =    0   # y angle of the center point
        self.sigma =    0   # z axis angle of the center point
        
        # Displacement vectors
        self.V_Z =      np.zeros((3, 1))
        self.V_Y =      np.zeros((3, 1))
        self.V_X =      np.zeros((3, 1))
        
        self.LZ =       pixel_axis_length  # length from z axis endpoint to center point
        self.LY =       pixel_axis_length
        self.LX =       pixel_axis_length
        
        # used to draw axis lines
        self.axis_points = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]] # [center, +z, +y, +x, center, -z, -y, -x]
        self.ws_edge_points = [[0, 0], [0, 0], [0, 0], [0, 0]]                              # [(xy), (x,-y), (-x, -y), (-x, y)]
        
    def run(self, center, events):
        self.proj_center_p = np.matrix(center).reshape((3, 1))
        
        # create illusion of 3D
        self.proj_center_p[1, 0] = self.proj_center_p[1, 0] - (self.proj_center_p[2, 0] * self.theta * 1.27)
        
        # display the coordinate grid
        self.show_grid(show_grid_points=False)
        
        for event in events:
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_UP:
                    self.theta += 0.01
                if event.key == pyg.K_DOWN:
                    self.theta -= 0.01
                if event.key == pyg.K_LEFT:
                    self.alpha += 0.01
                if event.key == pyg.K_RIGHT:
                    self.alpha -= 0.01
                if event.key == pyg.K_COMMA:
                    self.sigma -= 0.01
                if event.key == pyg.K_PERIOD:
                    self.sigma += 0.01
        
    def get_point_at_XYcoord(self, coord):
        # Uses the concept of ratios. If you think the distance from |---| is 10cm but i represent that distance as |-------| which is 100 cm
        # then point (10, 0) to you is point (100, 0) to me. Using this ratio I can know what you mean by 5cm -> 50cm
        
        # get the center point of the coordinate grid
        x = self.grid[(self.grid_rows//2), (self.grid_cols//2), 0]
        y = self.grid[(self.grid_rows//2), (self.grid_cols//2), 1]
        
        # get the point immediately diagnal to the center point in the first quadrant
        x_n = self.grid[(self.grid_rows//2) - 1, (self.grid_cols//2) - 1, 0]
        y_n = self.grid[(self.grid_rows//2) - 1, (self.grid_cols//2) - 1, 1]
        
        # find the y distance from the center y to the diagnal point y
        y_dis = y_n - y
        # same for x
        x_dis = x_n - x
        
        # determine the perceived grid box length
        per_gb_len = self.axis_len / self.grid_cols
        
        # calculate the point
        point = [x + ((x_dis * coord[0]) / per_gb_len), y + ((y_dis * coord[1]) / per_gb_len)]
        
        return point
        
    def connect_axis_points(self, i, j, color):
        pyg.draw.line(self.scrn, color, (self.axis_points[i][0], self.axis_points[i][1]), (self.axis_points[j][0], self.axis_points[j][1])) 
        
    def update_grid_points(self, draw=False):
        x_grid_boxes, y_grid_boxes = self.grid_rows, self.grid_cols
        
        # get variables
        xy_p = [self.ws_edge_points[0][0], self.ws_edge_points[0][1]]     # (x, y) point
        nxy_p = [self.ws_edge_points[3][0], self.ws_edge_points[3][1]]    # (-x, y)
        xny_p = [self.ws_edge_points[1][0], self.ws_edge_points[1][1]]    # (x, -y)
        
        xy_to_nxy_dist_x = abs(xy_p[0] - nxy_p[0])  # distances
        xy_to_nxy_dist_y = abs(xy_p[1] - nxy_p[1])
        
        # calculate the grid gap of each axis
        x_grid_gap = (xy_to_nxy_dist_x / x_grid_boxes)
        y_grid_gap = (xy_to_nxy_dist_y / y_grid_boxes)
        
        xy_to_nxy_slope_x = xy_p[0] - nxy_p[0]
        xy_to_nxy_slope_y = xy_p[1] - nxy_p[1]
        xy_to_xny_slope_x = xy_p[0] - xny_p[0]
        xy_to_xny_slope_y = xy_p[1] - xny_p[1]
        
        # create a list of x coordinates from xy_p to nxy_p
        x_coords = []
        y_coords = []
            # do not try to create a ranging list with gaps if the grid gap is 0.
        if x_grid_gap: 
                # create the appropriate x coordinates list depending on the coordinate point that is on the left relative to the other on the screen
            if xy_to_nxy_slope_x > 0:   # xy_p is to the right relative to nxy_p
                x_coords = list(np.arange(xy_p[0], nxy_p[0] - 1, -x_grid_gap))
            else:                       # they are level or xy_p is to the left
                x_coords = list(np.arange(xy_p[0], nxy_p[0] + 1, x_grid_gap))
        else:
            x_coords = [xy_p[0]]
                
            # do not try to create a ranging list with gaps if the grid gap is 0.
        if y_grid_gap: 
                # create the appropriate x coordinates list depending on the coordinate point that is on the above relative to the other on the screen
            if xy_to_nxy_slope_y > 0:   # xy_p is below relative to nxy_p
                y_coords = list(np.arange(xy_p[1], nxy_p[1] - 1, -y_grid_gap))
            else:                       # they are level or xy_p is above
                y_coords = list(np.arange(xy_p[1], nxy_p[1] + 1, y_grid_gap))
        else:
            y_coords = [xy_p[1]]
            
            # turn each element of the lists to an int 
        x_coords = [int(x) for x in x_coords]
        y_coords = [int(y) for y in y_coords]
        
        # create and fill workspace grid matrix
        self.grid = np.zeros((y_grid_boxes + 1, x_grid_boxes + 1, 2))
        
            # fill the x and y coordinates lists to match the shape of the ws_grid if they are not filled to that shape
        if len(x_coords) < x_grid_boxes + 1:
            for _ in range(x_grid_boxes + 1 - len(x_coords)):
                x_coords.append(x_coords[0])
                
        if len(y_coords) < y_grid_boxes + 1:
            for _ in range(y_grid_boxes + 1 - len(y_coords)):
                y_coords.append(y_coords[0])
        
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                self.grid[row, col, 0] = x_coords[col] - (xy_to_xny_slope_x / x_grid_boxes * row)
                self.grid[row, col, 1] = y_coords[col] - (xy_to_xny_slope_y / y_grid_boxes * row)
                if draw:
                    pyg.draw.circle(self.scrn, (25, 25, 25), (self.grid[row, col]), 1)
        
    def show_grid(self, show_grid_points=False): 
        # create axis endpoints
        points = []
        
        points.append(np.matrix([self.proj_center_p[0, 0], self.proj_center_p[1, 0], self.proj_center_p[2, 0]]))    # center point
        points.append(self.get_z_endpoint())
        points.append(self.get_y_endpoint())
        points.append(self.get_x_endpoint())
         
        i = 0
        for point in points:
            # turn 3D points into 2D points
            projected3D = np.dot(self.projection_matrix, point.reshape((3, 1)))
            
            x = int(projected3D[0][0])
            y = int(projected3D[1][0])
            
            self.axis_points[i] = [x, y]
            self.axis_points[i + 4] = [(self.proj_center_p[0, 0]) - (x - (self.proj_center_p[0, 0])), (self.proj_center_p[1, 0]) - (y - (self.proj_center_p[1, 0]))]
            i += 1
            
        # calculate workspace plane points. Used the concepts of parallel lines and distance
        # x,y point
        self.ws_edge_points[0][0] = self.axis_points[2][0] - (self.axis_points[0][0] - self.axis_points[3][0])    # x
        self.ws_edge_points[0][1] = self.axis_points[2][1] - (self.axis_points[0][1] - self.axis_points[3][1])    # y
        # -x,-y point
        self.ws_edge_points[2][0] = self.axis_points[6][0] - (self.axis_points[0][0] - self.axis_points[7][0])
        self.ws_edge_points[2][1] = self.axis_points[6][1] - (self.axis_points[0][1] - self.axis_points[7][1])
        # x,-y
        self.ws_edge_points[1][0] = self.axis_points[3][0] + (self.axis_points[0][0] - self.axis_points[2][0])
        self.ws_edge_points[1][1] = self.axis_points[3][1] + (self.axis_points[0][1] - self.axis_points[2][1])
        # -x,y
        self.ws_edge_points[3][0] = self.axis_points[7][0] + (self.axis_points[0][0] - self.axis_points[6][0])
        self.ws_edge_points[3][1] = self.axis_points[7][1] + (self.axis_points[0][1] - self.axis_points[6][1])
           
        # draw axes lines 
        self.connect_axis_points(0, 1, (0, 0, 255)) # draws z axis
        self.connect_axis_points(0, 2, (0, 255, 0)) #       y
        self.connect_axis_points(0, 3, (255, 0, 0)) #       x
        self.connect_axis_points(0, 5, (0, 0, 255)) # draws neg z axis
        self.connect_axis_points(0, 6, (0, 255, 0)) #           y
        self.connect_axis_points(0, 7, (255, 0, 0)) #           x
        
        # draw origin point
        pyg.draw.circle(self.scrn, (255, 23, 241), ([self.proj_center_p[0, 0], self.proj_center_p[1, 0]]), 4)
        
        # draw points to indicate the first octant of the workspace
        pyg.draw.circle(self.scrn, (0, 0, 0), tuple(self.axis_points[1]), 3)
        pyg.draw.circle(self.scrn, (0, 0, 0), tuple(self.axis_points[2]), 3)
        pyg.draw.circle(self.scrn, (0, 0, 0), tuple(self.axis_points[3]), 3)
        
        # draw workspace plane
        pyg_gfx.filled_polygon(self.scrn, [(x, y) for x, y in self.ws_edge_points], (0, 0, 0, 50))
        
        # update the grid points
        if show_grid_points:
            self.update_grid_points(show_grid_points)
        else:
            self.update_grid_points()
    
    def get_z_endpoint(self):
        self.calc_DVs()
        # return the x, y, z coordinate of the Z endpoint
        return np.matrix([self.V_Z[0, 0] + self.proj_center_p[0, 0], self.V_Z[1, 0] + self.proj_center_p[1, 0], self.V_Z[2, 0]])
    
    def get_y_endpoint(self):
        self.calc_DVs()
        # return the x, y, z coordinate of the Y endpoint
        return np.matrix([self.V_Y[0, 0] + self.proj_center_p[0, 0], self.V_Y[1, 0] + self.proj_center_p[1, 0], self.V_Y[2, 0]])
    
    def get_x_endpoint(self):
        self.calc_DVs()
        # return the x, y, z coordinate of the X endpoint
        return np.matrix([self.V_X[0, 0] + self.proj_center_p[0, 0], self.V_X[1, 0] + self.proj_center_p[1, 0], self.V_X[2, 0]])

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
    
# class Robot_joint():
#     def __init__(self, joint_pos = [0, 0, 0], rotation_angle = ["XY", [-pi/2, pi/2]], link_length = 0):
#         # initialize joint variables
#         self.pos = joint_pos
#         self.rot_plane = rotation_angle[0]
#         self.rot_angle = rotation_angle[1]
#         self.link_len = link_length
        
#     def show(self, workspace_grid):
#         # place robot joint point on the workspace at the specified joint position
        
    
# class Robot():
#     def __init__(self):
#         self.joint = []
    
#     def create_joint(self):
        
    
#     def place(self):
#         pass
        

    
    
        
        
        
            
            
            
            