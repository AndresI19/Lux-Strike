debug = False
#import all modules from directory, as well as pygame lib
#full modules
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
import sys,pygame,time
import Engine,Graphics,Menus,WC_Engine
#objects
from Settings import Settings
from Control_variables import Ctrl_Vars
from HUD import HUD
from World import World
from Enemies import ENEMIES
from Drops import Drop_envelope
from Player import Player
from Camera import Camera
from Save import Load_map

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
Screen = pygame.Surface((1920,1080))
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

#initialize control variables
Ctrl_Vars = Ctrl_Vars(debug)

#initialization swtich menu: Can probobaly move to world module
def world_init(Ctrl_Vars,Screen):
    def initialize_entities(World):
        Max_parameters = [World.num_cols,World.num_rows]
        spawn_coord = [World.spawn_col,World.spawn_row]
        player = Player(Screen,spawn_coord)
        enemies = ENEMIES(Screen,Max_parameters,World,player)
        hud = HUD(Settings,Screen,Ctrl_Vars,World,player,enemies)
        drops = Drop_envelope(Screen,Ctrl_Vars,hud,player.Stats)
        camera = Camera(World,player,enemies,drops)
        Ctrl_Vars.initialized = True
        return [player,enemies,hud,drops,camera]

    def load_entities(World,Data):
        Max_parameters = [World.num_cols,World.num_rows]
        spawn_coord = [World.spawn_col,World.spawn_row]
        player = Player(Screen,spawn_coord,DATA)
        enemies = ENEMIES(Screen,Max_parameters,World,player,DATA)
        hud = HUD(Settings,Screen,Ctrl_Vars,World,player,enemies,DATA)
        drops = Drop_envelope(Screen,Ctrl_Vars,hud,player.Stats,DATA)
        camera = Camera(World,player,enemies,drops)
        Ctrl_Vars.initialized = True
        return [player,enemies,hud,drops,camera]

    Loading = Graphics.Load_Screen(Window,Screen,Settings)
    if Ctrl_Vars.Game_Menu_Vars.Random:
        world = World(Screen,None,Loading)
        Ctrl_Vars.seed = str(world.seed)
        player,enemies,hud,drops,camera = initialize_entities(world)
        Ctrl_Vars.Game_Menu_Vars.Random = False
    elif Ctrl_Vars.Game_Menu_Vars.Custom:
        Seed = Ctrl_Vars.seed
        world = World(Screen,Seed,Loading)
        player,enemies,hud,drops,camera = initialize_entities(world)
        Ctrl_Vars.Game_Menu_Vars.Custom = False
    elif Ctrl_Vars.Game_Menu_Vars.Load:
        name = input()
        DATA = Load_map(name)
        world = World(Screen,None,Loading,DATA)
        player,enemies,hud,drops,camera = load_entities(world,DATA)
        Ctrl_Vars.Game_Menu_Vars.Load = False
    return (world,player,enemies,hud,drops,camera)

def new_world_init(Ctrl_Vars,Screen,World,Camera,Window,Settings):
    def re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,Drops,HUD,DATA= None):
        #assuming world has been initialized, this will re initialize everything else
        Max_parameters = (World.num_cols,World.num_rows)
        spawn_coord = (World.spawn_row,World.spawn_col)
        if DATA == None:
            Player.__init__(Screen,spawn_coord)
            Enemies.__init__(Screen,Max_parameters,World,Player)
            Drops.__init__(Screen,Ctrl_Vars,HUD,Player.Stats)
        else:
            Player.__init__(Screen,spawn_coord,DATA)
            Enemies.__init__(Screen,Max_parameters,World,Player,DATA)
            Drops.__init__(Screen,Ctrl_Vars,HUD,Player.Stats,DATA)
        HUD.__init__(Settings,Screen,Ctrl_Vars,World,Player,Enemies)


    Loading = Graphics.Load_Screen(Window,Screen,Settings)
    if Ctrl_Vars.Game_Menu_Vars.Random:
        World.__init__(Screen,None,Loading)
        Ctrl_Vars.seed = str(World.seed)
        re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,Drops,HUD)
        Ctrl_Vars.Game_Menu_Vars.Random = False
    elif Ctrl_Vars.Game_Menu_Vars.Custom:
        Seed = Ctrl_Vars.seed
        World.__init__(Screen,Seed,Loading)
        re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,Drops,HUD)
        Ctrl_Vars.Game_Menu_Vars.Custom = False
    elif Ctrl_Vars.Game_Menu_Vars.Load:
        name = input()
        DATA = Load_map(name)
        World.__init__(Screen,None,Loading,DATA)
        re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,Drops,HUD,DATA)
        Ctrl_Vars.Game_Menu_Vars.Load = False
    elif Ctrl_Vars.restart_world:
        Ctrl_Vars.restart_world = False
    Camera.follow = True

def game_loop(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera):
    Ctrl_Vars.merge_timer()
    if Ctrl_Vars.phase_active: #animation phase
        Engine.animation_check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera)
        if Ctrl_Vars.TURN_PLAYER:
            Engine.Player_animation_phase(Settings,Ctrl_Vars,HUD,World,Player,Enemies)   
        elif Ctrl_Vars.TURN_ENEMY:
            Engine.Enemy_animation_phase(Ctrl_Vars,World,Player,Enemies)
    else: #Ctrl_Vars.phase_active == False, action phase
        if Ctrl_Vars.TURN_PLAYER:
            Engine.check_drops(Player,Drops)
            Engine.check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera)
            Engine.Player_turn_end(World,Player,Enemies,Drops,Ctrl_Vars,HUD)
        else:
            Engine.enemy_turn(Ctrl_Vars,World,Player,Enemies,HUD)

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
                World,Player,Enemies,HUD,Drops,Camera = world_init(Ctrl_Vars,Screen)
            else:
                new_world_init(Ctrl_Vars,Screen,World,Camera,Window,Settings)
            Engine.end_loading(Settings,Ctrl_Vars,World,Player,Enemies,Drops,Camera)
        #-------------------------------------------------------------------------------------------*
        """Game loop %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
    else:
        if Ctrl_Vars.main:
            game_loop(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera)
            Camera.View(Ctrl_Vars)
            Graphics.Display(Screen,World,HUD,Player,Enemies,Drops)
        elif Ctrl_Vars.world_creator:
            if not Ctrl_Vars.WC_initialized:
                HUD,Map = WC_Engine.initialization(Screen,Ctrl_Vars)
                Ctrl_Vars.WC_initialized = True
            WC_Engine.check_events(Settings,Ctrl_Vars,Map,HUD)
            WC_Engine.check_mouse_position(Settings,Ctrl_Vars,Map,HUD)
            WC_Engine.Display(Screen,HUD,Map)
    
    Graphics.scale(Window,Screen,Settings)