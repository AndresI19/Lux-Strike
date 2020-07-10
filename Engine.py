import pygame
import pygame.display

#Player input engine vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
def check_events(Settings,Ctrl_Vars,World,Player,Enemies):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event,Ctrl_Vars)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event,Ctrl_Vars)
        #camera controls
        if event.type == pygame.MOUSEMOTION:
            MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Ctrl_Vars.Game_active = False
                Ctrl_Vars.Pause = True
            #camera Center
            elif event.key == pygame.K_LSHIFT:
                Center_Screen(Settings,World,Player,Enemies)
                Ctrl_Vars.camera_follow = True
            #Directional inputs-----------------------------------------
            else:
                if event.key == pygame.K_q:
                    set_NW(World,Player)
                elif event.key == pygame.K_w:
                    set_N(World,Player)
                elif event.key == pygame.K_e:
                    set_NE(World,Player)
                elif event.key == pygame.K_d:
                    set_SE(World,Player)
                elif event.key == pygame.K_s:
                    set_S(World,Player)
                elif event.key == pygame.K_a:
                    set_SW(World,Player)
                Ctrl_Vars.switch_turns()
                
"""event buttons 1 and 2 refer to mouse bindings"""
def MouseDown(event,Ctrl_Vars):
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = True
    elif event.button == 2:
        Ctrl_Vars.Right_MouseDown = True

def MouseUp(event,Ctrl_Vars):
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = False
    elif event.button == 2:
        Ctrl_Vars.Right_MouseDown = False

def MouseMotion(Settings,event,Ctrl_Vars,World,Player,Enemies):
    #handles relative movement of the mouse
    if Ctrl_Vars.Left_MouseDown:
        #drag
        dx = Settings.drag_sensativity*event.rel[0]
        dy = Settings.drag_sensativity*event.rel[1]
        """World.translate(Settings.drag_sensativity*event.rel[0],
            Settings.drag_sensativity*event.rel[1])"""
        Translate_Screen((dx,dy),World,Player,Enemies)
        Ctrl_Vars.camera_follow = False

#-----------------------------------------------------------------------------
def Pause_check_events(Settings,Ctrl_Vars,Buttons):
    Ctrl_Vars.mouse_down_update()
    check_hover(Buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event,Ctrl_Vars)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event,Ctrl_Vars)
        
        elif event.type == pygame.KEYDOWN:
            pass
        
#-----------------------------------------------------------------------------
def Start_check_events(Settings,Ctrl_Vars,Buttons):
    Ctrl_Vars.mouse_down_update()
    check_hover(Buttons)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown(event,Ctrl_Vars)
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseUp(event,Ctrl_Vars)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_TAB:
                Settings.toggle_fullscreen()

def check_hover(Buttons):
    mouse_position = pygame.mouse.get_pos()
    for i in range(len(Buttons)):
        x = mouse_position[0]
        y = mouse_position[1]
        Buttons[i].check_contained(x,y)

#Player input engine ---^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def Player_turn_end(World,Player,Enemies,Ctrl_Vars):
    Player_move(World,Player,Enemies)
    update_elevation(Player,World)
    
    check_foreground(World,Player,Ctrl_Vars)
    check_ground(World,Player,Ctrl_Vars)
    check_death(Player,Ctrl_Vars)

"""ENEMY TURN****************************************************************"""
"""--------------------------------------------------------------------------"""
def enemy_turn(Ctrl_Vars,World,Player,Enemies):
    for Enemy in Enemies.Group:
        enemy_scan(World,Player,Enemy)
        if Enemy.aware:
            Enemy.set_direction()
            Enemy_move(World,Enemy,Player,Enemies)
    Ctrl_Vars.switch_turns()
    Player.reset_hitstun()

def enemy_scan(World,Player,Enemy):
    if Enemy.aware:
        Enemy.set_direction()
    else:
        scan_radius(Player,Enemy,4)
    x = Player.x
    y = Player.y
    Enemy.update_player_location(x,y)

def scan_check(Player,Enemy,rel_coordinates):
    y = Enemy.y + rel_coordinates[1]
    x = Enemy.x + rel_coordinates[0]
    if Player.x == x and Player.y == y:
        Enemy.aware = True

def scan_radius(Player,Enemy,r):
    dy_max = (2*r + 1)
    dy_min = r + 1
    dx = 0
    SR_recursion(Player,Enemy,dy_min,dy_max,dx)

def SR_recursion(Player,Enemy,dy_min,dy,dx):
    if dy < dy_min:
        return
    y = -dy + 1
    for i in range(dy):
        if dx == 0:
            scan_check(Player,Enemy,[dx,y])
        else:
            if Enemy.off_center == 1:
                if dy%2 == 1:
                    x2 = -dx
                else:
                    x2 = -(dx)+1
                scan_check(Player,Enemy,[dx,y])
                scan_check(Player,Enemy,[x2,y])
            else:
                if dy%2 == 1:
                    x2 = dx
                else:
                    x2 = dx-1
                scan_check(Player,Enemy,[-dx,y])
                scan_check(Player,Enemy,[x2,y])
        y += 2
    dy -= 1
    if dy%2 ==0:
        dx += 1
    SR_recursion(Player,Enemy,dy_min,dy,dx)

"""*********************************************************************"""
#a check to make sure you dont fall off too high a cliff or jump too high a cliff
def Player_move(World,Player,Enemies):
    x = Player.x + Player.dx
    y = Player.y + Player.dy
    boundry = check_bounds(World,x,y)
    if boundry:
        Player.dx = 0
        Player.dy = 0
        return
    cliff_obsticle = check_cliff(World,Player,y,x)
    if cliff_obsticle:
        Player.dx = 0
        Player.dy = 0
        return
    enemy_obsticle = P_check_occupancy(y,x,Enemies)
    if not enemy_obsticle:
        Player.x += Player.dx
        Player.y += Player.dy
        if abs(Player.dy) == 1:
            Player.off_center *= -1
    Player.dx = 0
    Player.dy = 0

def Enemy_move(World,Enemy,Player,Enemies):
    x = Enemy.x + Enemy.dx
    y = Enemy.y + Enemy.dy
    boundry = check_bounds(World,x,y)
    enemy_obsticle = E_check_occupancy(y,x,Player,Enemies)
    cliff_obsticle = check_cliff(World,Enemy,y,x)
    stop_move = enemy_obsticle or cliff_obsticle or boundry
    if not stop_move:
        Enemy.x += Enemy.dx
        Enemy.y += Enemy.dy
        if abs(Enemy.dy) == 1:
            Enemy.off_center *= -1
    Enemy.dx = 0
    Enemy.dy = 0

def check_bounds(World,x,y):
    BX = x < World.Max_Columns and x > -1
    BY = y < World.Max_Rows and y > -1
    if BX and BY:
        return False
    else:
        return True

def check_cliff(World,MOB,y,x):
    if World.Terrain[y][x].type == 'Water':
        return False
    else:
        current_elevation = World.Terrain[MOB.y][MOB.x].elevation
        projected_elevation = World.Terrain[y][x].elevation
        cliff_height = projected_elevation - current_elevation
        if cliff_height <= 1 and cliff_height >= -2:
            return False
        else:
            return True

def P_check_occupancy(y,x,Enemies):
    for Enemy in Enemies.Group:
        if Enemy.x == x and Enemy.y == y:
            Enemies.Group.remove(Enemy)
            return True
    return False

def E_check_occupancy(y,x,Player,Enemies):
    if Player.x == x and Player.y == y:
        if Player.hitstun == False:
            Player.Stats.Health_Points -= 1
            Player.hitstun = True
        return True
    for Enemy in Enemies.Group:
        if Enemy.x == x and Enemy.y == y:
            return True
    return False

#directional MOTION vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""moving on a hexagon grid is comlicated, as the columns go up and contain a list of staggard rows. The way to menuever this is to
give the game knowledge of the player location and call every other row staggard. Hence, if the players row value goes up (y) then the off_center value
is flipped. Moving up or down requires a row change of plus or minus 2. At each possible control a check_move is preformed."""
def set_NE(World,MOB):
    if MOB.off_center == 1:
        MOB.set_direction(1,1,'NE')
    elif MOB.off_center == -1:
        MOB.set_direction(0,1,'NE')

def set_N(World,MOB):
    MOB.set_direction(0,2,'N')

def set_NW(World,MOB):
    if MOB.off_center == 1:
        MOB.set_direction(0,1,'NW')
    elif MOB.off_center == -1:
        MOB.set_direction(-1,1,'NW')

def set_SW(World,MOB):
    if MOB.off_center == 1:
        MOB.set_direction(0,-1,'SW')
    elif MOB.off_center == -1:
        MOB.set_direction(-1,-1,'SW')

def set_S(World,MOB):
    MOB.set_direction(0,-2,'S')

def set_SE(World,MOB):
    if MOB.off_center == 1:
        MOB.set_direction(1,-1,'SE')
    elif MOB.off_center == -1:
        MOB.set_direction(0,-1,'SE')

#directional MOTION ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#Camera funtions ....
def Center_Screen(Settings,World,Player,Enemies):
    xf = Settings.Screen_center[0]
    yf = Settings.Screen_center[1]
    xi = Player.MOB_rect.centerx
    yi = Player.MOB_rect.centery
    dx = xf - xi
    dy = yf - yi
    Translate_Screen((dx,dy),World,Player,Enemies)
    #World.translate(dx,dy)

def Translate_Screen(coordinates,World,Player,Enemies):
    dx = coordinates[0]
    dy = coordinates[1]
    World.translate(dx,dy)
    Player.translate(dx,dy)
    Enemies.translate(dx,dy)

def update_elevation(MOB,World):
    MOB.elevation = World.Terrain[MOB.y][MOB.x].elevation

def check_foreground(World,MOB,Ctrl_Vars):
    World.Terrain[Ctrl_Vars.foreground_list[0]][Ctrl_Vars.foreground_list[1]].reset_foreground()
    World.Terrain[MOB.y-2][MOB.x].check_foreground(MOB,Ctrl_Vars)

def Camera(Settings,Ctrl_Vars,World,Player,Enemies):
    if Ctrl_Vars.camera_follow:
        Center_Screen(Settings,World,Player,Enemies)

#Checking/Updating
def check_ground(World,Player,Ctrl_Vars):
    y,x = World.stairs[0],World.stairs[1]
    if Player.x == x and Player.y == y:
        Ctrl_Vars.Game_active = False
        Ctrl_Vars.Game_Win = True

def check_death(Player,Ctrl_Vars):
    if Player.Stats.Health_Points <= 0:
        Ctrl_Vars.Game_active = False
        Ctrl_Vars.Game_Over = True

#other
def line(MOB,World,N):
    Initial = World.Terrain[MOB.x][MOB.y].get_Character_Spot()
    Final = World.Terrain[MOB.x + MOB.dx][MOB.y + MOB.dy].get_Character_Spot()
    Xi = Initial[0]
    Yi = Initial[1]
    Xf = Final[0]
    Yf = Final[1]
    DX = Xf-Xi
    DY = Yf-Yi
    if DX == 0 and DY == 0:
        return
    elif DX == 0:
        increment = DY/N
        y = Yi
        for i in range(N):
            y += increment
            MOB.track.append([Xi,y])
    else:
        MOB.clear_track()
        m = (DY/DX)
        b = Yi - m * Xi
        x = Xi
        increment = float(DX/N)
        for i in range(N):
            y = x*m + b
            MOB.track.append([x,y])
            x += increment
        print("Track {}, Yi {}, Yf {}".format(MOB.track,Yi,Yf))

#instancing
def re_init(Settings,Screen,World,Player,Enemies,HUD):
    #assuming world has been initialized, this will re initialize everything else
    Max_parameters = (World.Max_Rows,World.Max_Columns)
    coordinates = (World.spawn_row,World.spawn_col)
    Player.__init__(Screen,coordinates,Max_parameters)
    Enemies.__init__(Screen,Max_parameters,World)
    HUD.__init__(Settings,Screen,World,Player.Stats)

def new_world_init(Ctrl_Vars,Screen,World):
        if Ctrl_Vars.Random:
            World.__init__(Screen,None)
            Ctrl_Vars.Random = False
        elif Ctrl_Vars.set_seed:
            Seed = Ctrl_Vars.seed
            World.__init__(Screen,Seed)
            Ctrl_Vars.set_seed = False
        elif Ctrl_Vars.restart_world:
            Ctrl_Vars.restart_world = False

#if main ever beomes very crowded this code might be useful
"""def first_world_init(Ctrl_Vars,Screen):
    if Ctrl_Vars.Random:
        world = World(Screen,None)
        Ctrl_Vars.Random = False
    elif Ctrl_Vars.set_seed:
        Seed = Ctrl_Vars.seed
        world = World(Screen,Seed)
        Ctrl_Vars.set_seed = False
        Ctrl_Vars.seed = ""
    return world"""