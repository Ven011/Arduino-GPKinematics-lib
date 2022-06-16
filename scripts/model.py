"""
This script is meant to be used to handle a model of a rotary robotic arm. It creates an application that
will have features that enable model creation and visialization. Additionally, through the application, the
user will be able to control the model using a keyboard and mouse.
"""

import pygame as pyg
import pygame_widgets as pyg_wid
from pygame_widgets.textbox import TextBox
import numpy as np
from math import *
from matrix_ops import Coordinate_grid
from menu_ops import Menu
    
ang = 0
    
def handle_workspace(ws, center_point ,events, ws2, ws3, ws4):
    global ang
    
    # # run the workspace
    ws.run(None, center_point, events)
    
    ws2.run(ws, [20 * cos(ang), 20 * sin(ang), 20], events)
    
    ws3.run(ws, [20 * cos(ang), 20 * sin(ang), 50], events)
    
    ws4.run(ws, [0, 0, 70], events)
    
    # create a workspace 
    
    ang += 0.01
    
    pyg.draw.line(ws.scrn, (234, 24, 242), (ws.get_point_at_XYZcoord([0, 0, 0])), (ws2.get_point_at_XYZcoord([0, 0, 0])), width=5)
    pyg.draw.line(ws.scrn, (30, 223, 34), (ws2.get_point_at_XYZcoord([0, 0, 0])), (ws3.get_point_at_XYZcoord([0, 0, 0])), width=5)
    pyg.draw.line(ws.scrn, (23, 43, 123), (ws3.get_point_at_XYZcoord([0, 0, 0])), (ws4.get_point_at_XYZcoord([0, 0, 0])), width=5)


if __name__ == "__main__":
    # initialize pygame
    pyg.init()
    # set display title
    pyg.display.set_caption("GPKinematics")
    # set initial window size
    WIDTH, HEIGHT = 800, 600
    # handle display
    screen = pyg.display.set_mode((WIDTH, HEIGHT), flags=pyg.RESIZABLE)
    # setup clock
    clock = pyg.time.Clock()
    # fps
    FPS = 30
    # active keydown repeat
    pyg.key.set_repeat(10)
    
    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DAVYS_GRAY = (81, 80, 82)
    JET = (51, 49, 56)
    TART_ORANGE = (255, 49, 46)
    BLACK_FOGRA = (0, 1, 3)
    ALMOND = (237, 224, 212)
    COFFEE = (127, 85, 57)
    BROWN_SUGAR = (156, 102, 68)
    ORANGE = (247, 127, 0)
    MAX_RED = (214, 40, 40)
    MAX_YELLOW_RED = (252, 191, 73)
    PRUSSIAN_BLUE = (0, 48, 73)
    
    
    # create main grid
    master_menu = Menu(screen, WHITE, grid_columns=40, grid_rows=80,
                       title_col_span=[15, 24], title_row_span=[1, 3], menu_title="GPK",)
    
    # initialize menus
    tool_menu = Menu(screen, ORANGE, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Tools")
    settings_menu = Menu(screen, MAX_RED, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Settings")
    comms_menu = Menu(screen, PRUSSIAN_BLUE, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Comms")
    joint_viz_menu = Menu(screen, MAX_YELLOW_RED, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Joint Viz")
    
    # create workspace
    workspace = Coordinate_grid(screen, pixel_axis_length=400, perceived_axis_length=200, grid_rows=10, grid_columns=10, zoom=True,
                                ws_plane=True, grid_points=True)
    
    joint_ws = Coordinate_grid(screen, pixel_axis_length=80, perceived_axis_length=40, grid_rows=4, grid_columns=4)
    joint_ws2 = Coordinate_grid(screen, pixel_axis_length=80, perceived_axis_length=40, grid_rows=4, grid_columns=4)
    joint_ws3 = Coordinate_grid(screen, pixel_axis_length=80, perceived_axis_length=40, grid_rows=4, grid_columns=4)

    while True:
        clock.tick(FPS)
        
        # get all pygame events
        events = pyg.event.get();
        
        # listen for shutdown events
        for event in events: 
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    pyg.quit()
                    exit()
        
        # get latest display information
        winfo = pyg.display.Info()
        
        # handle menus - Menus get draw in the order they are run here
        master_menu.run([0, 0, winfo.current_w, winfo.current_h])
        
        handle_workspace(workspace, [winfo.current_w//2, winfo.current_h//2, 1], events, joint_ws, joint_ws2, joint_ws3)
        
        tool_menu.run(
            master_menu.menu_grid.get_span(col_span=[0, 6], row_span=[0, 38])
        )
        settings_menu.run(
            master_menu.menu_grid.get_span(col_span=[33, 39], row_span=[0, 38])
        )
        comms_menu.run(
            master_menu.menu_grid.get_span(col_span=[33, 39], row_span=[39, 79])
        )
        joint_viz_menu.run(
            master_menu.menu_grid.get_span(col_span=[0, 6], row_span=[39, 79])
        )
        
        # update widgets. widgets have to be updated before the pygame display
        pyg_wid.update(events)
        # update screen
        pyg.display.update()
                        
    
        
            
        
        
    
    

