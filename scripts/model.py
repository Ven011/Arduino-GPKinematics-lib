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
from matrix_ops import MOPS
from menu_ops import Menu

mops = MOPS()
    
def handle_model_viz(width, height, scrn, events):
    # create the workspace axes and plane
    points = []
    center_point = np.matrix([width//2, height//2, 0])
    pyg.draw.circle(scrn, (255, 23, 241), (center_point[0, 0], center_point[0, 1]), 3)

    z_endpoint = mops.get_z_endpoint(width, height)
    y_endpoint = mops.get_y_endpoint(width, height)
    x_endpoint = mops.get_x_endpoint(width, height)
    
    points.append(center_point)
    points.append(z_endpoint)
    points.append(y_endpoint)
    points.append(x_endpoint)
    mops.project_workspace(points, width, height, scrn)
    
    for event in events:
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_UP:
                mops.theta += 0.01
            if event.key == pyg.K_DOWN:
                mops.theta -= 0.01
            if event.key == pyg.K_LEFT:
                mops.alpha += 0.01
            if event.key == pyg.K_RIGHT:
                mops.alpha -= 0.01
            if event.key == pyg.K_COMMA:
                mops.sigma -= 0.01
            if event.key == pyg.K_PERIOD:
                mops.sigma += 0.01

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
    FPS = 200
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
    
    
    # initialize menus
    tool_menu = Menu(screen, ORANGE, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Tools")
    # grid nesting example
    # tools_innermenu = Menu(screen, (255, 255, 255), 10, 8, menu_title="", title_row_span=[1, 3], title_col_span=[1, 3])
    settings_menu = Menu(screen, MAX_RED, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Settings")
    comms_menu = Menu(screen, PRUSSIAN_BLUE, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Comms")
    joint_viz_menu = Menu(screen, MAX_YELLOW_RED, grid_columns=20, grid_rows=40,
                    title_col_span=[2, 17], title_row_span=[1, 3], menu_title="Joint Viz")

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
                    
        # set background color
        screen.fill(WHITE)
        
        # get latest display information
        winfo = pyg.display.Info()
        
        # handle menus
        handle_model_viz(winfo.current_w, winfo.current_h, screen, events)
        tool_menu.run([0, 0, winfo.current_w//6, winfo.current_h//2])
        settings_menu.run([winfo.current_w - (winfo.current_w//6), 0, winfo.current_w//6, winfo.current_h//2])
        comms_menu.run([winfo.current_w - (winfo.current_w//6), winfo.current_h//2, winfo.current_w//6, winfo.current_h//2])
        joint_viz_menu.run([0, winfo.current_h/2, winfo.current_w/6, winfo.current_h/2])
        
        # tools_innermenu.run(tool_menu.menu_grid.get_span(row_span=[5, 10], col_span=[5, 8])) # simple grid nesting
        
        # update widgets. widgets have to be updated before the pygame display
        pyg_wid.update(events)
        # update screen
        pyg.display.update()
                        
    
        
            
        
        
    
    

