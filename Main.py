#full modules
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
import sys,pygame,time
import Engine,Graphics,Menus,WC_Engine
#Classes and funtions
from Settings import Settings
from HUD import HUD
from World import World
from Enemies import ENEMIES
from Drops import Drop_envelope
from Player import Player
from Camera import Camera
from Save import Load_map
from Generation import Make_Loading

#Global objects
from Control_variables import Ctrl_Vars,Screen

#initialize clock function, settings, screen window
clock = pygame.time.Clock()
pygame.font.init()
Settings = Settings()

##SOUND
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)
pygame.mixer.music.set_volume(Settings.settings["Master volume"]/100)

##Window
Window = Settings.create_window()
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

#initialization of all game object instances
def world_init():
    def init_entities(DATA):
        global player,enemies,hud,drops,camera
        Max_parameters = [world.num_cols,world.num_rows]
        spawn_coord = [world.spawn_col,world.spawn_row]
        player = Player(spawn_coord,DATA)
        enemies = ENEMIES(Max_parameters,world,player,DATA)
        hud = HUD(Settings,world,player,enemies,DATA)
        drops = Drop_envelope(hud,player.Stats,DATA)
        camera = Camera(world,player,enemies,drops)

    global world
    Make_Loading(Window,Settings)
    #Loading = Graphics.Load_Screen(Window,Settings)
    if Ctrl_Vars.GameNav.Load:
        name = Ctrl_Vars.seed
        DATA = Load_map(name)
        world = World(None,DATA)
        Ctrl_Vars.GameNav.Load = False
    else:
        DATA = None
    if Ctrl_Vars.GameNav.Random:
        world = World(None)
        Ctrl_Vars.seed = str(world.seed)
        Ctrl_Vars.GameNav.Random = False
    elif Ctrl_Vars.GameNav.Custom:
        Seed = Ctrl_Vars.seed
        world = World(Seed)
        Ctrl_Vars.GameNav.Custom = False
    elif Ctrl_Vars.GameNav.restart_world:
        Seed = world.seed
        world.__init__(Seed)
        Ctrl_Vars.GameNav.restart_world = False
    init_entities(DATA)

#loop for standard gameplay
def game_loop():
    Ctrl_Vars.merge_timer()
    if Ctrl_Vars.phase_active: #animation phase
        Engine.animation_check_events(Settings,hud,world,player,enemies,drops,camera)
        if Ctrl_Vars.TURN_PLAYER:
            Engine.Player_animation_phase(Settings,hud,world,player,enemies)   
        elif Ctrl_Vars.TURN_ENEMY:
            Engine.Enemy_animation_phase(world,player,enemies)
    else: #Ctrl_Vars.phase_active == False, action phase
        if Ctrl_Vars.TURN_PLAYER:
            Engine.check_drops(player,drops)
            Engine.check_events(Settings,hud,world,player,enemies,drops,camera)
            Engine.Player_turn_end(world,player,enemies,drops,hud)
        else:
            Engine.enemy_turn(world,player,enemies,hud)

"""Main loop: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
while True:
    clock.tick(60) #set frame rate (variable in argument per second)
    if not Ctrl_Vars.GameNav.Game_active:
        #Menus and game Loading
        if not Ctrl_Vars.GameNav.load_world:
            if Ctrl_Vars.GameNav.menu_select:
                #Dynamic Menus, Start, Pause, Victory, Game Over
                active_menu = Menus.menu_select(Window,Settings)
            Engine.run_menu(Settings,active_menu)
        #Create New world --------------------------------------------------------------------------*
            """Loading Screen"""
        elif Ctrl_Vars.GameNav.load_world:
            time.sleep(0.5)
            Screen.fill((0,0,0))
            pygame.display.flip()
            #Initialization of major game objects
            if not Ctrl_Vars.GameNav.restart_world:
                world = None
            world_init()
            Engine.end_loading(Settings,world,player,enemies,drops,camera)
        #-------------------------------------------------------------------------------------------*
        """Game loop %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
    else:
        if Ctrl_Vars.main: #recognizable game
            game_loop()
            camera.View(Ctrl_Vars)
            Graphics.Display(world,hud,player,enemies,drops)
        elif Ctrl_Vars.world_creator: 
            #World creator ---------------------------------------------------------
            if not Ctrl_Vars.WC_initialized:
                hud,Map,Elements,Cursor = WC_Engine.initialization()
                Ctrl_Vars.WC_initialized = True
            WC_Engine.check_events(Settings,Map,Elements,hud)
            WC_Engine.check_mouse_position(Settings,Map,Elements,hud)
            WC_Engine.Display(Screen,hud,Map,Elements,Cursor)
    #Scale graphics to resolution.
    Graphics.scale(Window,Screen,Settings)