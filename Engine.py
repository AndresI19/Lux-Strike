import sys, pygame, pygame.display
from Graphics import Menu_diplay,Load_Screen
import Save
from Control_variables import Ctrl_Vars

"""Main Loop *************************************************************************"""
#Game Engine. (Turn Based Engine) ++++++++++++++++++++++++++++++++++++++++
"""Action Phase"""
#Not that Player input engine gets called brefore this.

def Player_turn_end(World,Player,Enemies,Drops,HUD):
    if Player.dx != Player.col or Player.dy != Player.row:
        Player_move(World,Player,Enemies,Drops,HUD)
    Player.update_elevation(World)
    
    check_tall_block(World,Player)
    check_stairs(World,Player)
    check_death(Player)

def enemy_turn(World,Player,Enemies,HUD):
    for Enemy in Enemies.Group:
        Enemy.update_player_location(Player)    #update knowledge of player projected location
        if Enemy.aware:
            Enemy.choose_direction(World)
            Enemy_move(World,Enemy,Player,Enemies,HUD)
        else:
            Enemy.action(Player)
    Enemies.Enemy_Group_Collsion()
    Ctrl_Vars.end_turn()

"""Animation Phase"""
def Player_animation_phase(Settings,HUD,World,Player,Enemies):
    Player.move_line(World,Ctrl_Vars.phase_frame)
    if not Player.reset_hitstun():
        Player.walk_animation(Ctrl_Vars.phase_frame)
    if Ctrl_Vars.phase_frame + 1 == Ctrl_Vars.phase_Frames:
        Player.glue(World)
    
def Enemy_animation_phase(World,Player,Enemies):
    Enemies.move_line(World,Ctrl_Vars.phase_frame)
    if Player.hitstun:
        Player.hurt_animation(Ctrl_Vars.phase_frame)
    if Ctrl_Vars.phase_frame + 1 == Ctrl_Vars.phase_Frames:
        Enemies.glue(World)
        Player.reset_hitstun()

#Player input engine vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
def check_events(Settings,HUD,World,Player,Enemies,Drops,Camera):
    hold_keys(Player,World)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        #mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event)
        #camera controls
        if event.type == pygame.MOUSEMOTION:
            MouseMotion(Settings,event,World,Player,Enemies,Drops,Camera)
        elif event.type == pygame.KEYDOWN:
            KEYDOWN(event,Settings,HUD,World,Player,Enemies,Drops,Camera)
        elif event.type == pygame.KEYUP:
            KEYUP(event,World)

def animation_check_events(Settings,HUD,World,Player,Enemies,Drops,Camera):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        #mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event)
        if event.type == pygame.MOUSEMOTION:
            MouseMotion(Settings,event,World,Player,Enemies,Drops,Camera)
        elif event.type == pygame.KEYUP:
            KEYUP(event,World)    

def KEYUP(event,World):
    if event.key == pygame.K_LSHIFT:
        World.reset_highlight()
        Ctrl_Vars.LSHIFT_DOWN = False
    if event.key == pygame.K_q:
        World.reset_highlight()
        Ctrl_Vars.q_down = False
    elif event.key == pygame.K_w:
        World.reset_highlight()
        Ctrl_Vars.w_down = False
    elif event.key == pygame.K_e:
        World.reset_highlight()
        Ctrl_Vars.e_down = False
    elif event.key == pygame.K_d:
        World.reset_highlight()
        Ctrl_Vars.d_down = False
    elif event.key == pygame.K_s:
        World.reset_highlight()
        Ctrl_Vars.s_down = False
    elif event.key == pygame.K_a:
        World.reset_highlight()
        Ctrl_Vars.a_down = False

def KEYDOWN(event,Settings,HUD,World,Player,Enemies,Drops,Camera):
    if event.key == pygame.K_ESCAPE:
        Ctrl_Vars.GameNav.Menu_reset()
        Ctrl_Vars.GameNav.Pause = True
    #camera Center
    elif event.key == pygame.K_LSHIFT:
        Camera.set_pan(4)
        Ctrl_Vars.LSHIFT_DOWN = True
    elif event.key == pygame.K_SPACE:
        if Ctrl_Vars.LSHIFT_DOWN == False:
            Ctrl_Vars.page_count += 1
            HUD.Dialog_box.init_page()
        else:
            if Player.Stats.Laser_Heat < 5:
                Player.Stats.Laser_Heat += 1
                if Player.Stats.Laser_Heat == 5:
                    HUD.Dialog_box.load_event('ScortchingHot')
                HUD.Laser_Gauge.init_charge()
                #laser(World,Ctrl_Vars,Drops,Player,Enemies,[Player.col,Player.row])
                line(
                    World.Map,Player.D,[Player.col,Player.row],
                    laser_check,[World,Player,Enemies,Drops]
                )
                HUD.Combo.update()
                Ctrl_Vars.end_phase()

    elif event.key == pygame.K_F1:
        #Dev Button
        print("Player Grid Coordinates = Col:{},Row:{}".format(Player.col,Player.row))
        Spot = World.Map.data(Player.col,Player.row).get_Character_Spot()
        print("Player Pixel Coordinates = X: {}, Y:{}".format(Spot[0],Spot[1]))
        HUD.Dialog_box.load_event('Test')
    elif event.key == pygame.K_F2:
        World.Map.data(Player.col,Player.row).Hexagon_image.set_alpha(50)
        for door in World.Doors:
            door.Open(World)
    elif event.key == pygame.K_F3:
        Save_game(World,Player,Enemies,Drops)
    #Directional inputs-----------------------------------------
    else:
        if Ctrl_Vars.LSHIFT_DOWN == False:
            move_event(event,Player,World)
        else:
            face_direction(event,World,Player)

def move_event(event,Player,World):
    if event.key == pygame.K_q:
        Player.set_NW(World)
        Ctrl_Vars.q_down = True
    elif event.key == pygame.K_w:
        Player.set_N(World)
        Ctrl_Vars.w_down = True
    elif event.key == pygame.K_e:
        Player.set_NE(World)
        Ctrl_Vars.e_down = True
    elif event.key == pygame.K_d:
        Player.set_SE(World)
        Ctrl_Vars.d_down = True
    elif event.key == pygame.K_s:
        Player.set_S(World)
        Ctrl_Vars.s_down = True
    elif event.key == pygame.K_a:
        Player.set_SW(World)
        Ctrl_Vars.a_down = True

def hold_keys(Player,World):
    if Ctrl_Vars.q_down == True:
        Player.set_NW(World)
    elif Ctrl_Vars.w_down == True:
        Player.set_N(World)
    elif Ctrl_Vars.e_down == True:
        Player.set_NE(World)
    elif Ctrl_Vars.d_down == True:
        Player.set_SE(World)
    elif Ctrl_Vars.s_down == True:
        Player.set_S(World)
    elif Ctrl_Vars.a_down == True:
        Player.set_SW(World)

def face_direction(event,World,Player):
    if event.key == pygame.K_q:
        Player.sprite_direction('NW')
    elif event.key == pygame.K_w:
        Player.sprite_direction('N')
    elif event.key == pygame.K_e:
        Player.sprite_direction('NE')
    elif event.key == pygame.K_d:
        Player.sprite_direction('SE')
    elif event.key == pygame.K_s:
        Player.sprite_direction('S')
    elif event.key == pygame.K_a:
        Player.sprite_direction('SW')
    line(
        World.Map,Player.D,[Player.col,Player.row],
        highlight_check,[World,Player]
    )
    #Scan_line(World,Player,[Player.col,Player.row])

def MouseDown(event):
    """event buttons 1 and 2 refer to mouse bindings"""
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = True
    elif event.button == 2:
        Ctrl_Vars.Right_MouseDown = True

def MouseUp(event):
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = False
    elif event.button == 2:
        Ctrl_Vars.Right_MouseDown = False

def MouseMotion(Settings,event,World,Player,Enemies,Drops,Camera):
    #handles relative movement of the mouse
    if Ctrl_Vars.Left_MouseDown:
        #drag
        dx,dy = event.rel
        Camera.Translate_Screen((dx,dy))
        Camera.follow = False

#Menu Engine. ------------------------------------------------------------
def menu_management(Settings,Start_Screen,Pause_Screen,Game_Win,Game_Over,Num_Pad):
    if Ctrl_Vars.Start_Screen: 
        Menu_envelope = Start_Screen
    elif Ctrl_Vars.seed_menu:
        Menu_envelope = Num_Pad
    elif Ctrl_Vars.Pause:
        Menu_envelope = Pause_Screen
    elif Ctrl_Vars.Game_Win:
        Menu_envelope = Game_Win
    elif Ctrl_Vars.Game_Over:
        Menu_envelope = Game_Over
    run_menu(Settings,Menu_envelope)

def run_menu(Settings,Menu_envelope):
    Menu_check_events(Settings,Menu_envelope.UI)
    Menu_diplay(Menu_envelope)

#Menu input engine--------------------------------------------------------------------
def Menu_check_events(Settings,Buttons):
    #a different set of event mappings based on being ina menu, mostly to listen to the mouse and hitboxes
    Ctrl_Vars.mouse_down_update()
    check_hover(Settings,Buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if Ctrl_Vars.Start_Screen:
                    sys.exit(0)
            elif event.key == pygame.K_LSHIFT:
                Ctrl_Vars.LSHIFT_DOWN = True
            if Ctrl_Vars.Start_Vars.key == 'Seed':
                num_keys(event)
            elif Ctrl_Vars.Start_Vars.key == 'Load World':
                typing(event,Ctrl_Vars.world_name)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                Ctrl_Vars.LSHIFT_DOWN = False

def check_hover(Settings,Buttons):
    x,y = pygame.mouse.get_pos() #scales mouse movements to resolution
    x *= Settings.mouseX_scaling
    y *= Settings.mouseY_scaling
    for i in range(len(Buttons)):
        Buttons[i].check_contained(x,y)

def num_keys(event):
    if len(Ctrl_Vars.seed) < 18:
        if event.key >= 48 and event.key <= 57: #Type any number between 0 and 9
            Ctrl_Vars.seed += chr(event.key)

    elif len(Ctrl_Vars.seed) >= 18:
        if event.key == 13:
            Ctrl_Vars.Nav_GameTypes("Custom")
            """Ctrl_Vars.GameNav.Menu_reset()
            Ctrl_Vars.GameNav.load_world = True
            Ctrl_Vars.GameNav.menu_select = False
            Ctrl_Vars.GameNav.Custom = True"""
    if event.key == pygame.K_BACKSPACE:
        Ctrl_Vars.seed = Ctrl_Vars.seed[:-1]
        sound = pygame.mixer.Sound("SFX/Button_press.wav")
        pygame.mixer.Sound.play(sound)

def typing(event,string):
    char = chr(event.key)
    if event.key >= 48 and event.key <= 57 or event.key == 32: #Type any number between 0 and 9 or a space
        string += char
    elif event.key >= 97 and event.key <= 122: #Type any number between 0 and 9
        if Ctrl_Vars.LSHIFT_DOWN:
            char = char.capitalize()
        string += char
    if event.key == pygame.K_BACKSPACE:
        string = string[:-1]
        sound = pygame.mixer.Sound("SFX/Button_press.wav")
        pygame.mixer.Sound.play(sound)
    Ctrl_Vars.world_name = string

"""Main Loop end *************************************************************************"""

#Movement Checks vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
def Player_move(World,Player,Enemies,Drops,HUD):
    def thud():
        sound = pygame.mixer.Sound("SFX/hit_wall.wav")
        pygame.mixer.Sound.play(sound)
        Player.reset_direction()
        Ctrl_Vars.set_button_downs()

    col = Player.dx #projected tile
    row = Player.dy
    if World.check_bounds(col,row): #in bounds?
        thud()
        return
    if World.check_doors(Player,col,row):
        Player.reset_direction()
        HUD.Keys.update()
        Ctrl_Vars.set_button_downs()
    if World.check_cliff(Player,col,row): #too high?
        thud()
        return
    if Enemies.check_kill(Ctrl_Vars,Drops,col,row): #hit enemy?
        Player.reset_direction()
        Ctrl_Vars.set_button_downs()
        HUD.Combo.update()
        Ctrl_Vars.end_phase()
        return
    else:
        Player.Queue_movement(World,Ctrl_Vars.phase_Frames) #create a line to animate your movement
        Ctrl_Vars.end_turn() #end turn

def Enemy_move(World,Enemy,Player,Enemies,HUD):
    def collision(col,row):
        if Player.col == col and Player.row == row: #hit player?
            Player.hurt()
            HUD.Combo.update()
            return True
        #TODO: Enemy on enemy collision leaves gaps, might have to do with list ordering
        for Enemy in Enemies.Group:
            if Enemy.col == col and Enemy.row == row:
                return True
        return False

    col = Enemy.dx #projected direction
    row = Enemy.dy
    boundry = World.check_bounds(col,row)
    cliff_obsticle = World.check_cliff(Enemy,col,row)
    enemy_obsticle = collision(col,row)
    stop_move = enemy_obsticle or cliff_obsticle or boundry
    if stop_move: #no need to make a thud noise, you dont care what the enemy noise makes
        Enemy.reset_direction()
    else:
        Enemy.Queue_movement(World,Ctrl_Vars.phase_Frames) #make a line

#Checking/Updating
def check_stairs(World,Player):
    col,row = World.stairs[0],World.stairs[1]
    if Player.col == col and Player.row == row:
        Ctrl_Vars.GameNav.Menu_reset()
        Ctrl_Vars.GameNav.Game_Win = True

def check_drops(Player,Drops):
    Drops.check_pick_up(Player)

def check_death(Player):
    if Player.Stats.Health_Points <= 0:
        Ctrl_Vars.GameNav.Menu_reset()
        Ctrl_Vars.GameNav.Game_Over = True
        sound = pygame.mixer.Sound("SFX/game over.wav")
        pygame.mixer.Sound.play(sound)

def check_tall_block(World,MOB):
    col, row = Ctrl_Vars.foreground_list
    World.Map.data(col,row).reset_alpha()
    World.Map.data(MOB.col,MOB.row-2).check_tall_block(MOB,Ctrl_Vars)

def end_loading(Settings,World,Player,Enemies,Drops,Camera):
    Ctrl_Vars.GameNav.load_world = False
    Ctrl_Vars.GameNav.Game_active = True
    Camera.Center_Screen()
    Player.glue(World)
    Enemies.glue(World)
    pygame.mixer.music.load('Music/Navy Blues.mp3')
    pygame.mixer.music.play(-1)

##While loop: Line functions
def laser_check(args,coords):
    World,MOB,Enemies,Drops = args
    col,row = coords
    if World.Map.data(col,row).elevation <= MOB.elevation:
        World.laser_list.append([col,row])
        if World.Map.data(col,row).elevation == MOB.elevation:
            return Enemies.check_kill(Ctrl_Vars,Drops,col,row)
        return False
    return True

def highlight_check(args,coords):
    World,MOB = args
    col,row = coords
    if World.Map.data(col,row).elevation == MOB.elevation:
        World.Map.data(col,row).highlighted = True
        World.highlighted_list.append([col,row])
        return False
    return True

def line(HG,D,start,f,fargs):
    Next = HG.get_[D](start)
    while Next != False:
        if f(fargs,Next):
            break
        Next = HG.get_[D](Next)

#Naming saved worlds
def Save_game(World,Player,Enemies,Drops):
    name = input("Type name: ")
    Save.Save_world(name,World,Player,Enemies,Drops)