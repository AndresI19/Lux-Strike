import pygame
import pygame.display
import sys
from Graphics import Menu_diplay
from Drops import Money_drop,Key

"""Main Loop *************************************************************************"""
#Game Engine. (Turn Based Engine) ++++++++++++++++++++++++++++++++++++++++
"""Action Phase"""
#Not that Player input engine gets called brefore this.

def Player_turn_end(World,Player,Enemies,Drops,Ctrl_Vars):
    if Player.dx != 0 or Player.dy != 0:
        Player_move(Ctrl_Vars,World,Player,Enemies,Drops)
    update_elevation(Player,World)
    
    check_tall_block(World,Player,Ctrl_Vars)
    check_stairs(World,Player,Ctrl_Vars)
    check_death(Player,Ctrl_Vars)

def enemy_turn(Ctrl_Vars,World,Player,Enemies):
    x = Player.x + Player.dx
    y = Player.y + Player.dy
    for Enemy in Enemies.Group:
        Enemy.update_player_location(x,y)    #update knowledge of player projected location
        if Enemy.aware:
            Enemy.choose_direction()
            Enemy_move(Ctrl_Vars,World,Enemy,Player,Enemies)
        else:
            Enemy.scan_radius(Player,4)
    Enemies.Enemy_Group_Collsion()
    Ctrl_Vars.end_turn()

"""Animation Phase"""
def Player_animation_phase(Settings,Ctrl_Vars,HUD,World,Player,Enemies):
    Player.move_line(World,Ctrl_Vars.phase_frame)
    if not Player.reset_hitstun():
        Player.walk_animation(Ctrl_Vars.phase_frame)
    if Ctrl_Vars.phase_frame + 1 == Ctrl_Vars.phase_Frames:
        Player.glue(World)
    
def Enemy_animation_phase(Ctrl_Vars,World,Player,Enemies):
    Enemies.move_line(World,Ctrl_Vars.phase_frame)
    if Player.hitstun:
        Player.hurt_animation(Ctrl_Vars.phase_frame)
    if Ctrl_Vars.phase_frame + 1 == Ctrl_Vars.phase_Frames:
        Enemies.glue(World)
        Player.reset_hitstun()

#Player input engine vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
def check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops):
    hold_keys(Ctrl_Vars,Player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        #mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event,Ctrl_Vars)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event,Ctrl_Vars)
        #camera controls
        if event.type == pygame.MOUSEMOTION:
            MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies,Drops)
        elif event.type == pygame.KEYDOWN:
            KEYDOWN(event,Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops)
        elif event.type == pygame.KEYUP:
            KEYUP(event,Ctrl_Vars,World)

def animation_check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        #mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event,Ctrl_Vars)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event,Ctrl_Vars)
        if event.type == pygame.MOUSEMOTION:
            MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies,Drops)
        elif event.type == pygame.KEYUP:
            KEYUP(event,Ctrl_Vars,World)    

def KEYUP(event,Ctrl_Vars,World):
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

def KEYDOWN(event,Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops):
    if event.key == pygame.K_ESCAPE:
        Ctrl_Vars.Game_Menu_Vars.Menu_reset()
        Ctrl_Vars.Game_Menu_Vars.Pause = True
    #camera Center
    elif event.key == pygame.K_LSHIFT:
        Center_Screen(Settings,World,Player,Enemies,Drops)
        Ctrl_Vars.camera_follow = True
        Ctrl_Vars.LSHIFT_DOWN = True
    elif event.key == pygame.K_SPACE:
        Ctrl_Vars.box_count += 1
        HUD.Dialog_box.init_box()
    elif event.key == pygame.K_F1:
        #Dev Button
        print("Player Grid Coordinates = X: {}, Y:{}".format(Player.x,Player.y))
        Spot = World.Terrain[Player.y][Player.x].get_Character_Spot()
        print("Player Pixel Cordinates = X: {}, Y:{}".format(Spot[0],Spot[1]))
        HUD.Dialog_box.init_dialog('Tutorial1')
    elif event.key == pygame.K_F2:
        World.Terrain[Player.y][Player.x].Hexagon_image.set_alpha(50)
    #Directional inputs-----------------------------------------
    else:
        if Ctrl_Vars.LSHIFT_DOWN == False:
            move_event(event,Ctrl_Vars,Player)
        else:
            face_direction(event,Ctrl_Vars,World,Player)

def move_event(event,Ctrl_Vars,Player):
    if event.key == pygame.K_q:
        Player.set_NW()
        Ctrl_Vars.q_down = True
    elif event.key == pygame.K_w:
        Player.set_N()
        Ctrl_Vars.w_down = True
    elif event.key == pygame.K_e:
        Player.set_NE()
        Ctrl_Vars.e_down = True
    elif event.key == pygame.K_d:
        Player.set_SE()
        Ctrl_Vars.d_down = True
    elif event.key == pygame.K_s:
        Player.set_S()
        Ctrl_Vars.s_down = True
    elif event.key == pygame.K_a:
        Player.set_SW()
        Ctrl_Vars.a_down = True

def hold_keys(Ctrl_Vars,Player):
    if Ctrl_Vars.q_down == True:
        Player.set_NW()
    elif Ctrl_Vars.w_down == True:
        Player.set_N()
    elif Ctrl_Vars.e_down == True:
        Player.set_NE()
    elif Ctrl_Vars.d_down == True:
        Player.set_SE()
    elif Ctrl_Vars.s_down == True:
        Player.set_S()
    elif Ctrl_Vars.a_down == True:
        Player.set_SW()

def face_direction(event,Ctrl_Vars,World,Player):
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
    Scan_line(World,Player,[Player.x,Player.y],Player.off_center)

def MouseDown(event,Ctrl_Vars):
    """event buttons 1 and 2 refer to mouse bindings"""
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = True
    elif event.button == 2:
        Ctrl_Vars.Right_MouseDown = True

def MouseUp(event,Ctrl_Vars):
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = False
    elif event.button == 2:
        Ctrl_Vars.Right_MouseDown = False

def MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies,Drops):
    #handles relative movement of the mouse
    if Ctrl_Vars.Left_MouseDown:
        #drag
        dx = Settings.drag_sensativity*event.rel[0]
        dy = Settings.drag_sensativity*event.rel[1]
        Translate_Screen((dx,dy),World,Player,Enemies,Drops)
        Ctrl_Vars.camera_follow = False

#Menu Engine. ------------------------------------------------------------
def menu_management(Settings,Ctrl_Vars,Start_Screen,Pause_Screen,Game_Win,Game_Over,Num_Pad):
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
    run_menu(Settings,Ctrl_Vars,Menu_envelope)

def run_menu(Settings,Ctrl_Vars,Menu_envelope):
    Menu_check_events(Settings,Ctrl_Vars,Menu_envelope.Menus)
    Menu_diplay(Menu_envelope)

#Menu input engine--------------------------------------------------------------------
def Menu_check_events(Settings,Ctrl_Vars,Buttons):
    Ctrl_Vars.mouse_down_update()
    check_hover(Settings,Buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event,Ctrl_Vars)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event,Ctrl_Vars)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if Ctrl_Vars.Start_Screen:
                    sys.exit(0)
            if Ctrl_Vars.Start_Vars.Num_pad:
                num_keys(event,Ctrl_Vars)

def check_hover(Settings,Buttons):
    mouse_position = pygame.mouse.get_pos()
    for i in range(len(Buttons)):
        x = mouse_position[0] * Settings.mouseX_scaling
        y = mouse_position[1] * Settings.mouseY_scaling
        Buttons[i].check_contained(x,y)

def num_keys(event,Ctrl_Vars):
    if len(Ctrl_Vars.seed) <= 18:
        if len(Ctrl_Vars.seed) < 18:
            if event.key == pygame.K_1:
                Ctrl_Vars.seed += "1"
            elif event.key == pygame.K_2:
                Ctrl_Vars.seed += "2"
            elif event.key == pygame.K_3:
                Ctrl_Vars.seed += "3"
            elif event.key == pygame.K_4:
                Ctrl_Vars.seed += "4"
            elif event.key == pygame.K_5:
                Ctrl_Vars.seed += "5"
            elif event.key == pygame.K_6:
                Ctrl_Vars.seed += "6"
            elif event.key == pygame.K_7:
                Ctrl_Vars.seed += "7"
            elif event.key == pygame.K_8:
                Ctrl_Vars.seed += "8"
            elif event.key == pygame.K_9:
                Ctrl_Vars.seed += "9"
            elif event.key == pygame.K_0:
                Ctrl_Vars.seed += "0"
        elif event.key == pygame.K_BACKSPACE:
            Ctrl_Vars.seed = Ctrl_Vars.seed[:-1]
        elif event.key == pygame.K_KP_ENTER:
            if len(Ctrl_Vars.seed) >= 18:
                Ctrl_Vars.seed_menu = False
                Ctrl_Vars.load_world = True
                Ctrl_Vars.set_seed = True
                Ctrl_Vars.Start_Screen = False
        sound = pygame.mixer.Sound("SFX/Button_press.wav")
        pygame.mixer.Sound.play(sound)

"""Main Loop end *************************************************************************"""

#Movement Checks vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
def Player_move(Ctrl_Vars,World,Player,Enemies,Drops):
    x = Player.x + Player.dx #projected tile
    y = Player.y + Player.dy
    if World.check_bounds(x,y): #in bounds?
        sound = pygame.mixer.Sound("SFX/hit_wall.wav")
        pygame.mixer.Sound.play(sound)
        Player.reset_direction()
        Ctrl_Vars.set_button_downs()
        return
    if World.check_cliff(Player,y,x): #too high?
        sound = pygame.mixer.Sound("SFX/hit_wall.wav")
        pygame.mixer.Sound.play(sound)
        Player.reset_direction()
        Ctrl_Vars.set_button_downs()
        return
    if P_check_occupancy(y,x,Enemies,Drops,Ctrl_Vars): #hit an enemy?
        Player.reset_direction()
        Ctrl_Vars.set_button_downs()
        Player.Stats.combo += 1
        return
    else:
        Queue_movement(Player,World,Ctrl_Vars.phase_Frames) #create a line to animate your movement
        Ctrl_Vars.end_turn() #end turn

def Enemy_move(Ctrl_Vars,World,Enemy,Player,Enemies):
    x = Enemy.x + Enemy.dx #projected direction
    y = Enemy.y + Enemy.dy
    boundry = World.check_bounds(x,y)
    cliff_obsticle = World.check_cliff(Enemy,y,x)
    enemy_obsticle = E_check_occupancy(y,x,Player,Enemies)
    stop_move = enemy_obsticle or cliff_obsticle or boundry
    if stop_move: #no need to make a thud noise, you dont care what the enemy noise makes
        Enemy.reset_direction()
    else:
        Queue_movement(Enemy,World,Ctrl_Vars.phase_Frames) #make a line

def P_check_occupancy(y,x,Enemies,Drops,Ctrl_Vars):
    for Enemy in Enemies.Group: #Maybe you killed something
        if Enemy.x == x and Enemy.y == y:
            Enemy.SFX_death()
            drop = Money_drop(
                Enemies.Screen,Ctrl_Vars,[Enemy.x,Enemy.y],[Enemy.MOB_rect.centerx,Enemy.MOB_rect.bottom]
            )
            Drops.Group.append(drop)
            Enemies.Group.remove(Enemy)
            Ctrl_Vars.end_phase()
            return True
    return False

def E_check_occupancy(y,x,Player,Enemies):
    if Player.x == x and Player.y == y: #hit player?
        Player.hurt()   
        return True
    #FIXME:enemy on enemy collision: it might be fixed but keep an eye out
    for Enemy in Enemies.Group:
        if (Enemy.x) == x and (Enemy.y) == y:
            return True
    return False

#Camera funtions ....
def Center_Screen(Settings,World,Player,Enemies,Drops):
    xf = 960 
    yf = 440
    xi = Player.MOB_rect.centerx
    yi = Player.MOB_rect.centery
    dx = xf - xi
    dy = yf - yi
    Translate_Screen((dx,dy),World,Player,Enemies,Drops)

def Translate_Screen(coordinates,World,Player,Enemies,Drops):
    dx = coordinates[0]
    dy = coordinates[1]
    World.translate(dx,dy)
    Player.translate(dx,dy)
    Enemies.translate(dx,dy)
    Drops.translate(dx,dy)

def Camera(Settings,Ctrl_Vars,World,Player,Enemies,Drops):
    if Ctrl_Vars.camera_follow:
        Center_Screen(Settings,World,Player,Enemies,Drops)
    if Player.hitstun:
        Camera_shake(4,Ctrl_Vars.phase_frame,World,Player,Enemies,Drops)

def Camera_shake(degree,frame,World,Player,Enemies,Drops):
    if frame%2 == 0:
        x = degree
    elif frame%2 == 1:
        x = -1*degree
    Translate_Screen((x,0),World,Player,Enemies,Drops)

#Checking/Updating
def check_stairs(World,Player,Ctrl_Vars):
    y,x = World.stairs[0],World.stairs[1]
    if Player.x == x and Player.y == y:
        Ctrl_Vars.Game_Menu_Vars.Menu_reset()
        Ctrl_Vars.Game_Menu_Vars.Game_Win = True

def check_drops(Player,Drops):
    Drops.check_pick_up(Player)

def check_death(Player,Ctrl_Vars):
    if Player.Stats.Health_Points <= 0:
        Ctrl_Vars.Game_Menu_Vars.Menu_reset()
        Ctrl_Vars.Game_Menu_Vars.Game_Over = True
        sound = pygame.mixer.Sound("SFX/game over.wav")
        pygame.mixer.Sound.play(sound)

def update_elevation(MOB,World):
    MOB.elevation = World.Terrain[MOB.y][MOB.x].elevation

def check_tall_block(World,MOB,Ctrl_Vars):
    World.Terrain[Ctrl_Vars.foreground_list[0]][Ctrl_Vars.foreground_list[1]].reset_alpha()
    World.Terrain[MOB.y-2][MOB.x].check_tall_block(MOB,Ctrl_Vars)
#other
def Queue_movement(MOB,World,N):
    Initial = World.Terrain[MOB.y][MOB.x].get_Character_Spot()
    Final = World.Terrain[MOB.y + MOB.dy][MOB.x + MOB.dx].get_Character_Spot()
    x = Initial[0]
    y = Initial[1]
    DX = Final[0]-Initial[0]
    DY = Final[1]-Initial[1]
    if DX == 0 and DY == 0:
        return
    elif DX == 0:
        increment = DY/N
        for i in range(N):
            y += increment
            MOB.track.append([x,y])
    else:
        m = (DY/DX)
        b = y - m * x
        increment = float(DX/N)
        for i in range(N):
            y = x*m + b
            MOB.track.append([round(x),round(y)])
            x += increment

def Scan_line(World,MOB,Start,stagger):
    Next = select_line_path(MOB,Start,stagger)
    off_center = Next[1]
    Next = Next[0]
    if check_line(World,Start,Next):    #Else end
        Scan_line(World,MOB,Next,off_center)

def select_line_path(MOB,Start,stagger):
    Next_x = Start[0]
    Next_y = Start[1]
    off_center = stagger
    if MOB.D == 'S':
        Next_y -= 2
    elif MOB.D == 'N':
        Next_y += 2
    off_center *= -1
    if MOB.D == 'NE':
        Next_y += 1
        if off_center == -1:
            Next_x += 1
    elif MOB.D == 'NW':
        Next_y += 1
        if off_center == 1:
            Next_x -= 1
    elif MOB.D == 'SW':
        Next_y -= 1
        if off_center == 1:
            Next_x -= 1
    elif MOB.D == 'SE':
        Next_y -= 1
        if off_center == -1:
            Next_x += 1
    return [(Next_x,Next_y),off_center]

def check_line(World,Start,Next):
    Start_x = Start[0]
    Start_y = Start[1]
    Next_x = Next[0]
    Next_y = Next[1]
    row_bound = Next_y >= 0 and Next_y < World.Max_Rows
    col_bound = Next_x >= 0 and Next_x < World.Max_Columns
    if row_bound and col_bound:
        DZ = World.Terrain[Next_y][Next_x].elevation - World.Terrain[Start_y][Start_x].elevation
        if DZ == 0:
            World.Terrain[Next_y][Next_x].highlighted = True
            World.highlighted_list.append([Next_y,Next_x])
            return True
        else:
            return False

##initialization
def re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,Drops,HUD):
    #assuming world has been initialized, this will re initialize everything else
    Max_parameters = (World.Max_Rows,World.Max_Columns)
    spawn_coord = (World.spawn_row,World.spawn_col)
    Player.__init__(Screen,spawn_coord)
    Enemies.__init__(Screen,Max_parameters,World)
    HUD.__init__(Settings,Screen,Ctrl_Vars,World,Player,Enemies)
    Drops.__init__(HUD)

def new_world_init(Ctrl_Vars,Screen,World,Window,Settings):
    if Ctrl_Vars.Game_Menu_Vars.Random:
        World.__init__(Screen,None,Window,Settings)
        Ctrl_Vars.seed = str(World.seed)
        Ctrl_Vars.Game_Menu_Vars.Random = False
    elif Ctrl_Vars.Game_Menu_Vars.Custom:
        Seed = Ctrl_Vars.seed
        World.__init__(Screen,Seed,Window,Settings)
        Ctrl_Vars.Game_Menu_Vars.Custom = False
    elif Ctrl_Vars.restart_world:
        Ctrl_Vars.restart_world = False
    Ctrl_Vars.camera_follow = True

def end_loading(Settings,Ctrl_Vars,World,Player,Enemies,Drops):
    Ctrl_Vars.Game_Menu_Vars.load_world = False
    Ctrl_Vars.Game_Menu_Vars.Game_active = True
    Center_Screen(Settings,World,Player,Enemies,Drops)
    Player.glue(World)
    Enemies.glue(World)
    pygame.mixer.music.load('Music/Navy Blues.mp3')
    pygame.mixer.music.play(-1)
