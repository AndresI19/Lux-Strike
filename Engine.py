import sys, pygame, pygame.display
from Graphics import Menu_diplay

"""Main Loop *************************************************************************"""
#Game Engine. (Turn Based Engine) ++++++++++++++++++++++++++++++++++++++++
"""Action Phase"""
#Not that Player input engine gets called brefore this.

def Player_turn_end(World,Player,Enemies,Drops,Ctrl_Vars,HUD):
    if Player.dx != Player.col or Player.dy != Player.row:
        Player_move(Ctrl_Vars,World,Player,Enemies,Drops,HUD)
    Player.update_elevation(World)
    
    check_tall_block(World,Player,Ctrl_Vars)
    check_stairs(World,Player,Ctrl_Vars)
    check_death(Player,Ctrl_Vars)

def enemy_turn(Ctrl_Vars,World,Player,Enemies,HUD):
    col = Player.dx
    row = Player.dy
    for Enemy in Enemies.Group:
        Enemy.update_player_location(col,row)    #update knowledge of player projected location
        if Enemy.aware:
            Enemy.choose_direction(World)
            Enemy_move(Ctrl_Vars,World,Enemy,Player,Enemies,HUD)
        else:
            Enemy.action(Player)
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
def check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera):
    hold_keys(Ctrl_Vars,Player,World)
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
            MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies,Drops,Camera)
        elif event.type == pygame.KEYDOWN:
            KEYDOWN(event,Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera)
        elif event.type == pygame.KEYUP:
            KEYUP(event,Ctrl_Vars,World)

def animation_check_events(Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        #mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event,Ctrl_Vars)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event,Ctrl_Vars)
        if event.type == pygame.MOUSEMOTION:
            MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies,Drops,Camera)
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

def KEYDOWN(event,Settings,Ctrl_Vars,HUD,World,Player,Enemies,Drops,Camera):
    if event.key == pygame.K_ESCAPE:
        Ctrl_Vars.Game_Menu_Vars.Menu_reset()
        Ctrl_Vars.Game_Menu_Vars.Pause = True
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
                laser(World,Ctrl_Vars,Drops,Player,Enemies,[Player.col,Player.row])
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
    #Directional inputs-----------------------------------------
    else:
        if Ctrl_Vars.LSHIFT_DOWN == False:
            move_event(event,Ctrl_Vars,Player,World)
        else:
            face_direction(event,Ctrl_Vars,World,Player)

def move_event(event,Ctrl_Vars,Player,World):
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

def hold_keys(Ctrl_Vars,Player,World):
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
    Scan_line(World,Player,[Player.col,Player.row])

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

def MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies,Drops,Camera):
    #handles relative movement of the mouse
    if Ctrl_Vars.Left_MouseDown:
        #drag
        dx = Settings.drag_sensativity*event.rel[0]
        dy = Settings.drag_sensativity*event.rel[1]
        Camera.Translate_Screen((dx,dy))
        Camera.follow = False

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
    elif len(Ctrl_Vars.seed) >= 18:
        if event.key == 13:
            Ctrl_Vars.Game_Menu_Vars.Menu_reset()
            Ctrl_Vars.Game_Menu_Vars.load_world = True
            Ctrl_Vars.Game_Menu_Vars.menu_select = False
            Ctrl_Vars.Game_Menu_Vars.Custom = True
    if event.key == pygame.K_BACKSPACE:
        Ctrl_Vars.seed = Ctrl_Vars.seed[:-1]
        sound = pygame.mixer.Sound("SFX/Button_press.wav")
        pygame.mixer.Sound.play(sound)

"""Main Loop end *************************************************************************"""

#Movement Checks vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
def Player_move(Ctrl_Vars,World,Player,Enemies,Drops,HUD):
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

def Enemy_move(Ctrl_Vars,World,Enemy,Player,Enemies,HUD):
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
def check_stairs(World,Player,Ctrl_Vars):
    col,row = World.stairs[0],World.stairs[1]
    if Player.col == col and Player.row == row:
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

def check_tall_block(World,MOB,Ctrl_Vars):
    """World.Terrain[Ctrl_Vars.foreground_list[0]][Ctrl_Vars.foreground_list[1]].reset_alpha()
    World.Terrain[MOB.y-2][MOB.x].check_tall_block(MOB,Ctrl_Vars)"""
    col, row = Ctrl_Vars.foreground_list
    World.Map.data(col,row).reset_alpha()
    World.Map.data(MOB.col,MOB.row-2).check_tall_block(MOB,Ctrl_Vars)

##initialization
def re_init(Settings,Screen,Ctrl_Vars,World,Player,Enemies,Drops,HUD):
    #assuming world has been initialized, this will re initialize everything else
    Max_parameters = (World.num_cols,World.num_rows)
    spawn_coord = (World.spawn_row,World.spawn_col)
    Player.__init__(Screen,spawn_coord)
    Enemies.__init__(Screen,Max_parameters,World,Player)
    HUD.__init__(Settings,Screen,Ctrl_Vars,World,Player,Enemies)
    Drops.__init__(Screen,Ctrl_Vars,HUD,Player.Stats)

def new_world_init(Ctrl_Vars,Screen,World,Camera):
    if Ctrl_Vars.Game_Menu_Vars.Random:
        World.__init__(Screen,None)
        Ctrl_Vars.seed = str(World.seed)
        Ctrl_Vars.Game_Menu_Vars.Random = False
    elif Ctrl_Vars.Game_Menu_Vars.Custom:
        Seed = Ctrl_Vars.seed
        World.__init__(Screen,Seed)
        Ctrl_Vars.Game_Menu_Vars.Custom = False
    elif Ctrl_Vars.restart_world:
        Ctrl_Vars.restart_world = False
    Camera.follow = True

def end_loading(Settings,Ctrl_Vars,World,Player,Enemies,Drops,Camera):
    Ctrl_Vars.Game_Menu_Vars.load_world = False
    Ctrl_Vars.Game_Menu_Vars.Game_active = True
    Camera.Center_Screen()
    Player.glue(World)
    Enemies.glue(World)
    pygame.mixer.music.load('Music/Navy Blues.mp3')
    pygame.mixer.music.play(-1)

##Recursive Line functions
def Scan_line(World,MOB,Start):
    def Path():
        if MOB.D == 'N':
            Next = World.Map.get_N(Start)
        elif MOB.D == 'NE':
            Next = World.Map.get_NE(Start)
        elif MOB.D == 'SE':
            Next = World.Map.get_SE(Start)
        elif MOB.D == 'S':
            Next = World.Map.get_S(Start)
        elif MOB.D == 'SW':
            Next = World.Map.get_SW(Start)
        elif MOB.D == 'NW':
            Next = World.Map.get_NW(Start)
        return Next

    def Act(Next):
        col,row = Next
        if World.Map.data(col,row).elevation == MOB.elevation:
            World.Map.data(col,row).highlighted = True
            World.highlighted_list.append([col,row])
            return True
        return False

    Next = Path()
    if Next != False:
        if Act(Next):    #Else end
            Scan_line(World,MOB,Next)

def laser(World,Ctrl_Vars,Drops,MOB,Enemies,Start):
    def Path():
        if MOB.D == 'N':
            Next = World.Map.get_N(Start)
        elif MOB.D == 'NE':
            Next = World.Map.get_NE(Start)
        elif MOB.D == 'SE':
            Next = World.Map.get_SE(Start)
        elif MOB.D == 'S':
            Next = World.Map.get_S(Start)
        elif MOB.D == 'SW':
            Next = World.Map.get_SW(Start)
        elif MOB.D == 'NW':
            Next = World.Map.get_NW(Start)
        return Next

    def Act(Next):
        col,row = Next
        if World.Map.data(col,row).elevation <= MOB.elevation:
            World.laser_list.append([col,row])
            if World.Map.data(col,row).elevation == MOB.elevation:
                return not Enemies.check_kill(Ctrl_Vars,Drops,col,row)
        return False

    Next = Path()
    if Act(Next) != False:    #Else end
        laser(World,Ctrl_Vars,Drops,MOB,Enemies,Next)