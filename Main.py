#import all modules from directory, as well as pygame lib
#full modules
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame
import time
import Engine
import Graphics
import Menus
#objects
from Settings import Settings
from Control_variables import Ctrl_Vars
from HUD import HUD
from World import World
from Enemies import ENEMIES
from Player import Player

#initialize clock function, settings, screen window
clock = pygame.time.Clock()
pygame.font.init()
Settings = Settings()
##SOUND
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)
pygame.mixer.music.set_volume(0.08)

Screen = pygame.display.set_mode((Settings.Screen_width,Settings.Screen_height))
pygame.display.set_caption("Lux Strike")
Icon = pygame.image.load('HUD/Icon.png').convert()
Icon.set_colorkey((255,0,255))
pygame.display.set_icon(Icon)

#initialize control variables
Ctrl_Vars = Ctrl_Vars()

#Start Menu --------------------------------------------------------------------
"""Set Control variables to start with an active start menu operation, initialize all start menu elements"""
Ctrl_Vars.Game_active = False
Ctrl_Vars.Start_Screen = True
Ctrl_Vars.menu_select = True
#---------------------------------------------------------------------------------

#initialization swtich menu:
def world_init(Ctrl_Vars,Screen):
    if Ctrl_Vars.Random:
        world = World(Screen,None)
        Ctrl_Vars.seed = str(world.seed)
        Ctrl_Vars.Random = False
    elif Ctrl_Vars.set_seed:
        Seed = Ctrl_Vars.seed
        world = World(Screen,Seed)
        Ctrl_Vars.set_seed = False
    return world

#main loop: note pause functionality limited.
while True:
    clock.tick(60) #set fram rate (variable in argument per second)
    if not Ctrl_Vars.Game_active:
        if not Ctrl_Vars.load_world:
            #Dynamic Menus, Start, Pause, Victory, Game Over
            if Ctrl_Vars.menu_select:
                active_menu = Menus.menu_select(Screen,Ctrl_Vars)
            Engine.run_menu(Settings,Ctrl_Vars,active_menu) 
        #Create New world --------------------------------------------------------------------------*
            """Loading Screen"""
        elif Ctrl_Vars.load_world:
            time.sleep(0.5)
            Screen.fill((0,0,0))
            pygame.display.flip()
            #Initialization of major game objects
            if not Ctrl_Vars.initialized:
                World = world_init(Ctrl_Vars,Screen)
                Max_parameters = (World.Max_Rows,World.Max_Columns)
                spawn_coord = (World.spawn_row,World.spawn_col)
                Player = Player(Screen,spawn_coord)
                Enemies = ENEMIES(Screen,Max_parameters,World)
                HUD = HUD(Settings,Screen,Ctrl_Vars,World,Player,Enemies)
                Ctrl_Vars.initialized = True
            else:
                Engine.new_world_init(Ctrl_Vars,Screen,World) 
                Engine.re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,HUD)
            Engine.end_loading(Settings,Ctrl_Vars,World,Player,Enemies)
        #-------------------------------------------------------------------------------------------*
    #Main Game loop
    else:
        Ctrl_Vars.merge_timer()
        if Ctrl_Vars.phase_active:
            Engine.animation_check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies)
            if Ctrl_Vars.TURN_PLAYER:
                Engine.Player_animation_phase(Settings,Ctrl_Vars,HUD,World,Player,Enemies)   
            elif Ctrl_Vars.TURN_ENEMY:
                Engine.Enemy_animation_phase(Ctrl_Vars,World,Player,Enemies)
        else: #Ctrl_Vars.phase_active == False
            if Ctrl_Vars.TURN_PLAYER:
                Engine.check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies)
                Engine.Player_turn_end(World,Player,Enemies,Ctrl_Vars)
            else:
                Engine.enemy_turn(Ctrl_Vars,World,Player,Enemies)

        Engine.Camera(Settings,Ctrl_Vars,World,Player,Enemies)
        Graphics.Display(Screen,World,HUD,Player,Enemies)