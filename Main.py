#import all modules from directory, as well as pygame lib
#full modules
import pygame
import pygame.font
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
#start menu object that contains all start menu elements.
Start_Screen = Menus.Start_Envelope(Screen,Ctrl_Vars)
Pause_Screen = Menus.Pause_Envelope(Screen,Ctrl_Vars)
Game_Over = Menus.Game_Over_Envelope(Screen,Ctrl_Vars)
Game_Win = Menus.Game_Win_Envelope(Screen,Ctrl_Vars)
Num_Pad = Menus.Num_Pad(Screen,Ctrl_Vars)
#---------------------------------------------------------------------------------

#initialization swtich menu:
def world_init(Ctrl_Vars,Screen):
    if Ctrl_Vars.Random:
        world = World(Screen,None)
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
        #Dynamic Menus, Start, Pause, Victory, Game Over
        if Ctrl_Vars.Start_Screen:
            Engine.Start_check_events(Settings,Ctrl_Vars,Start_Screen.Menus)
            Graphics.Menu_diplay(Start_Screen)
        elif Ctrl_Vars.seed_menu:
            Engine.Start_check_events(Settings,Ctrl_Vars,Num_Pad.Menus)
            Graphics.Menu_diplay(Num_Pad)
        elif Ctrl_Vars.Pause:
            Engine.Pause_check_events(Settings,Ctrl_Vars,Pause_Screen.Menus)
            Graphics.Menu_diplay(Pause_Screen) 
        elif Ctrl_Vars.Game_Win:
            Engine.Pause_check_events(Settings,Ctrl_Vars,Game_Win.Menus)
            Graphics.Menu_diplay(Game_Win)
        elif Ctrl_Vars.Game_Over:
            Engine.Pause_check_events(Settings,Ctrl_Vars,Game_Over.Menus)
            Graphics.Menu_diplay(Game_Over) 
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
                coordinates = (World.spawn_row,World.spawn_col)
                Player = Player(Screen,coordinates,Max_parameters)
                Enemies = ENEMIES(Screen,Max_parameters,World)
                HUD = HUD(Settings,Screen,World,Player.Stats)
                Ctrl_Vars.initialized = True
            else:
                Engine.new_world_init(Ctrl_Vars,Screen,World) 
                Engine.re_init(Settings,Screen,World,Player,Enemies,HUD)
            
            Ctrl_Vars.load_world = False
            Ctrl_Vars.Game_active = True

            Engine.Center_Screen(Settings,World,Player,Enemies)
            Player.update_coordinates(World)
            Enemies.update_coordinates(World)
        #--------------------------------------------------------------------------------------------*
    #Main Game loop
    else:
        Ctrl_Vars.turn_timer()
        if Ctrl_Vars.TURN_PLAYER:
            Engine.check_events(Settings,Ctrl_Vars,World,Player,Enemies)
            Engine.Player_turn_end(World,Player,Enemies,Ctrl_Vars)
            if Ctrl_Vars.turn_frame == 0:
                Player.update_coordinates(World)
        else:
            Engine.enemy_turn(Ctrl_Vars,World,Player,Enemies)
            if Ctrl_Vars.turn_frame == 0:
                Enemies.update_coordinates(World)
        Engine.Camera(Settings,Ctrl_Vars,World,Player,Enemies)
        Graphics.Display(Screen,World,HUD,Player,Enemies)

