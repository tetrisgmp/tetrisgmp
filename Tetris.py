
import pygame
import core

hauteur = 500
largeur = 500

rectangle = []

def setup():
    print("setup")
    global rectangle
    core.WINDOW_SIZE = [hauteur, largeur]
    core.fps = 30

def run ():
    print("run")

core.main(setup,run)