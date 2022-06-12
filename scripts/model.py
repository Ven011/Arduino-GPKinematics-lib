"""
This script is meant to be used to handle a model of a rotary robotic arm. It creates an application that
will have features that enable model creation and visialization. Additionally, through the application, the
user will be able to control the model using a keyboard and mouse.
"""

import pygame as pyg
import numpy as np
from math import *
from matrix_ops import MOPS

mops = MOPS()

def draw_menus_backgrounds(width, height, scrn):
    # toolkit menu
    pyg.draw.rect(scrn, (51, 49, 56), (0, 0, width/6, height/2))
    # joint viz menu
    pyg.draw.rect(scrn, (81, 80, 82), (0, height/2, width/6, height/2))
    # GPK setting menu
    pyg.draw.rect(scrn, (255, 255, 250), (width - (width/6), 0, width/6, height/2))
    # Ardu comms menu
    pyg.draw.rect(scrn, (255, 49, 46), (width - (width/6), height/2, width/6, height/2))
    # model viz menu
    pyg.draw.rect(scrn, (0, 1, 3), (width/6, 0, width - (width/3), height))
    
def handle_model_viz(width, height, scrn, events):
    # create the workspace axes and plane
    points = []
    center_point = np.matrix([width/2, height/2, 0])
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
    
    # active keydown repeat
    pyg.key.set_repeat(10)
    
    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    while True:
        # get all pygame events
        for event in pyg.event.get(): 
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
        draw_menus_backgrounds(winfo.current_w, winfo.current_h, screen)
        handle_model_viz(winfo.current_w, winfo.current_h, screen, pyg.event.get())
        
        # update screen
        pyg.display.update()
                        
    
        
            
        
        
    
    

