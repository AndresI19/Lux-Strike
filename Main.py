#import all modules from directory, as well as pygame lib
#full modules
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
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
from Drops import Drop_envelope
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
pygame.mixer.music.set_volume(Settings.master_volume/100)

##Window
Screen = pygame.Surface((1920,1080))
Window = pygame.display.set_mode((Settings.Screen_width,Settings.Screen_height))
pygame.display.set_caption("Lux Strike")
Icon = pygame.image.load('HUD/Icon.png').convert()
Icon.set_colorkey((255,0,255))
pygame.display.set_icon(Icon)

#Present start up screen --
studio = pygame.image.load('Title/Studio.png')
Screen.blit(studio,(0,0))
Graphics.scale(Window,Screen,Settings)
pygame.display.flip()
#--

#initialize control variables
Ctrl_Vars = Ctrl_Vars()

#initialization swtich menu: Can probobaly move to world module
def world_init(Ctrl_Vars,Screen,Window,Settings):
    if Ctrl_Vars.Game_Menu_Vars.Random:
        world = World(Screen,None,Window,Settings)
        Ctrl_Vars.seed = str(world.seed)
        Ctrl_Vars.Game_Menu_Vars.Random = False
    elif Ctrl_Vars.Game_Menu_Vars.Custom:
        Seed = Ctrl_Vars.seed
        world = World(Screen,Seed,Window,Settings)
        Ctrl_Vars.Game_Menu_Vars.Custom = False
    return world

"""Main loop: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
while True:
    clock.tick(60) #set frame rate (variable in argument per second)
    if not Ctrl_Vars.Game_Menu_Vars.Game_active:
        #Menus and game Loading
        if not Ctrl_Vars.Game_Menu_Vars.load_world:
            if Ctrl_Vars.Game_Menu_Vars.menu_select:
                #Dynamic Menus, Start, Pause, Victory, Game Over
                active_menu = Menus.menu_select(Screen,Window,Ctrl_Vars,Settings)
            Engine.run_menu(Settings,Ctrl_Vars,active_menu)
        #Create New world --------------------------------------------------------------------------*
            """Loading Screen"""
        elif Ctrl_Vars.Game_Menu_Vars.load_world:
            time.sleep(0.5)
            Screen.fill((0,0,0))
            pygame.display.flip()
            #Initialization of major game objects
            if not Ctrl_Vars.initialized:
                World = world_init(Ctrl_Vars,Screen,Window,Settings)
                Max_parameters = (World.Max_Rows,World.Max_Columns)
                spawn_coord = (World.spawn_row,World.spawn_col)
                Player = Player(Screen,spawn_coord)
                Enemies = ENEMIES(Screen,Max_parameters,World)
                HUD = HUD(Settings,Screen,Ctrl_Vars,World,Player,Enemies)
                Drops = Drop_envelope(HUD)
                Ctrl_Vars.initialized = True
            else:
                Engine.new_world_init(Ctrl_Vars,Screen,World,Window,Settings) 
                Engine.re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,Drops,HUD)
            Engine.end_loading(Settings,Ctrl_Vars,World,Player,Enemies,Drops)
        #-------------------------------------------------------------------------------------------*
        """Game loop %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
    else:
        Ctrl_Vars.merge_timer()
        if Ctrl_Vars.phase_active: #animation phase
            Engine.animation_check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops)
            if Ctrl_Vars.TURN_PLAYER:
                Engine.Player_animation_phase(Settings,Ctrl_Vars,HUD,World,Player,Enemies)   
            elif Ctrl_Vars.TURN_ENEMY:
                Engine.Enemy_animation_phase(Ctrl_Vars,World,Player,Enemies)
        else: #Ctrl_Vars.phase_active == False, action phase
            if Ctrl_Vars.TURN_PLAYER:
                Engine.check_drops(Player,Drops)
                Engine.check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops)
                Engine.Player_turn_end(World,Player,Enemies,Drops,Ctrl_Vars)
            else:
                Engine.enemy_turn(Ctrl_Vars,World,Player,Enemies)

        Engine.Camera(Settings,Ctrl_Vars,World,Player,Enemies,Drops)
        Graphics.Display(Screen,World,HUD,Player,Enemies,Drops)
    Graphics.scale(Window,Screen,Settings)