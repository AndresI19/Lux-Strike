#World Creator engine
import pygame,sys,math
import Tessellation
from WC_HUD import WC_HUD
from Generation import Hexagon

def check_events(Settings,Ctrl_Vars,Map,Elements,HUD):
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
            MouseMotion(event,Settings,Ctrl_Vars,Map,Elements,HUD)
        elif event.type == pygame.KEYDOWN:
            KEYDOWN(Settings,event,Ctrl_Vars,Map,HUD)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                Ctrl_Vars.LSHIFT_DOWN = False

def check_mouse_position(Settings,Ctrl_Vars,Map,Elements,HUD):
    if not Ctrl_Vars.LSHIFT_DOWN:
        x,y = pygame.mouse.get_pos()
        x *= Settings.mouseX_scaling
        y *= Settings.mouseY_scaling
        HUD.Inventory.collision(x,y)
        for col in range(Map.num_cols):
            for row in range(Map.num_rows):
                hover = Map.data(col,row).check_contained(x,y)
                if hover:
                    pencil_draw(Ctrl_Vars,Map,Elements,col,row)

def pencil_draw(Ctrl_Vars,Map,Elements,col,row):
    Type = Ctrl_Vars.WC_Tools.Type
    if Ctrl_Vars.Left_MouseDown:
        if Type == None:
            return
        ID = Ctrl_Vars.WC_Tools.ID
        if Type == 'Tile':
            Map.data(col,row).update_ID(ID)
        else:
            for element in Elements:
                if element.col == col and element.row == row:
                    Elements.remove(element)
            coords = [col,row]
            poss = Map.data(col,row).get_center()
            Screen = Map.data(col,row).Screen
            element = Field_element(Screen,Type,ID,coords,poss)
            Elements.append(element)
    elif Ctrl_Vars.Right_MouseDown:
        if Type == 'Tile':
            Map.data(col,row).update_ID(0)
        else:
            for element in Elements:
                if element.col == col and element.row == row:
                    Elements.remove(element)

def MouseDown(event,Ctrl_Vars):
    """event buttons 1 and 2 refer to mouse bindings"""
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = True
    elif event.button == 3:
        Ctrl_Vars.Right_MouseDown = True

def MouseUp(event,Ctrl_Vars):
    if event.button == 1:
        Ctrl_Vars.Left_MouseDown = False
    elif event.button == 3:
        Ctrl_Vars.Right_MouseDown = False

def MouseMotion(event,Settings,Ctrl_Vars,Map,Elements,HUD):
    #handles relative movement of the mouse
    if Ctrl_Vars.LSHIFT_DOWN and Ctrl_Vars.Left_MouseDown:
        #drag
        dx,dy = event.rel
        if Ctrl_Vars.WC_Tools.move_inv:
            HUD.Inventory.translate(dx,dy)
        else:
            for col in range(Map.num_cols):
                for row in range(Map.num_rows):
                    Map.data(col,row).translate(dx,dy)
            for element in Elements:
                element.translate(dx,dy)

def KEYDOWN(Settings,event,Ctrl_Vars,Map,HUD):
    if event.key == pygame.K_ESCAPE:
        Ctrl_Vars.WC_Tools.Pause = True
        Ctrl_Vars.Game_Menu_Vars.Game_active = False
        Ctrl_Vars.Game_Menu_Vars.menu_select = True
    elif event.key == pygame.K_LSHIFT:
        Ctrl_Vars.LSHIFT_DOWN = True
    elif event.key == pygame.K_F1:
        Ctrl_Vars.WC_Tools.toggle_HUD()
    elif event.key == pygame.K_e:
        HUD.Inventory.toggle()
    elif event.key == pygame.K_f:
        x,y = pygame.mouse.get_pos()
        x *= Settings.mouseX_scaling
        y *= Settings.mouseY_scaling
        for col in range(Map.num_cols):
            for row in range(Map.num_rows):
                hover = Map.data(col,row).check_contained(x,y)
                if hover:
                    ID1 = Ctrl_Vars.WC_Tools.ID
                    ID2 = Map.data(col,row).ID
                    if ID1 != ID2:
                        fill(Map,[col,row],[ID1,ID2])
    else:
        if event.key >= 48 and event.key <= 57: #Type any number between 0 and 9
            x,y = pygame.mouse.get_pos()
            x *= Settings.mouseX_scaling
            y *= Settings.mouseY_scaling
            item = HUD.Inventory.get_collision(x,y)
            index = event.key - 49
            if index == -1:
                index = 9

            if item != False:
                Type,ID = item
                Ctrl_Vars.WC_Tools.set_hotbar(index,Type,ID)
                HUD.hotbar.set_tool(index,Type,ID)
            else:
                Ctrl_Vars.WC_Tools.set_TypeID(index)
                HUD.hotbar.highlight(index)

def initialization(Screen,Ctrl_Vars):
    HUD = WC_HUD(Screen,Ctrl_Vars)
    Map = Map_init(Screen)
    Elements = []
    Cursor = highlight(Screen)
    pygame.mixer.music.load('Music/World Edit.wav')
    pygame.mixer.music.play(-1)
    return (HUD,Map,Elements,Cursor)

def Map_init(Screen):
    """cols = int(input("Cols: "))
    rows = int(input("Rows: "))"""
    cols = 35
    rows = 35
    Map = Tessellation.Hex_Grid(cols,rows)
    for col in range(Map.num_cols):
        for row in range(Map.num_rows):
            tile = WC_tile(Screen,col,row)
            Map.write(tile,col,row)
    return Map

def Draw_UI(Map,Elements,Cursor):
    highlights = []
    for row in range(Map.num_rows):
        draw_row = Map.num_rows - row - 1
        for col in range(Map.num_cols):
            Map.data(col,draw_row).draw(highlights)
    for element in Elements:
        element.draw()
    for rect in highlights:
        Cursor.draw(rect)

def Display(Screen,HUD,Map,Elements,Cursor):
    Screen.fill((0,0,0))
    Draw_UI(Map,Elements,Cursor)
    HUD.draw()

def return_home(Ctrl_Vars):
    Ctrl_Vars.Game_Menu_Vars.Menu_reset()
    Ctrl_Vars.main = True
    Ctrl_Vars.world_creator = False
    Ctrl_Vars.Game_Menu_Vars.load_world = False
    Ctrl_Vars.Game_Menu_Vars.Game_active = False
    Ctrl_Vars.Game_Menu_Vars.Start_Screen = True
    Ctrl_Vars.Game_Menu_Vars.menu_select = True

def fill(Map,coords,ID):
    """fills parametric outline to create solid map, by creating list of all tiles in a row and filling all
    empty blocks between the min and max"""
    def check(coords):
        #check
        if coords != False:
            col, row = coords
            if Map.data(col,row).ID == ID2:
                Map.data(col,row).update_ID(ID1)
                #return
                recursive_fill(coords)

    def recursive_fill(coords):
        Next = Map.get_N(coords)
        check(Next)
        Next = Map.get_NW(coords)
        check(Next)
        Next = Map.get_SW(coords)
        check(Next)
        Next = Map.get_S(coords)
        check(Next)
        Next = Map.get_SE(coords)
        check(Next)
        Next = Map.get_NE(coords)
        check(Next)

    #fill grid shape
    ID1,ID2 = ID
    recursive_fill(coords)

class WC_tile(Hexagon):
    def __init__(self,Screen,col,row):
        Hexagon.__init__(self,col,row,0,0)
        self.Screen = Screen
        self.image = pygame.image.load("WC_Hex/Tile0.png").convert()
        self.image.set_colorkey((255,0,255))

        self.height = 78
        self.width = 90
        self.side_length = self.width/2
        self.offset = (self.side_length*(3/2))
        self.position()
        self.highlighted = False
        self.Highlight = pygame.image.load("WC_Hex/TileHighlight.png").convert()
        self.Highlight.set_colorkey((255,0,255))

    def update_ID(self,ID):
        self.ID = ID
        self.image = pygame.image.load(
            "WC_Hex/Tile{}.png".format(self.ID)
            ).convert()
        self.image.set_colorkey((255,0,255))

    def translate(self,dx,dy):
        self.left += dx
        self.top += dy
        self.center_y += dy
        self.bottom += dy

    def position(self):
        self.bottom = 1080 - (self.row * (self.height / 2 - 1))
        self.top = self.bottom - self.height
        self.left = self.col * (self.width + self.side_length - 1)
        if self.row%2 == 0:
            self.left += self.offset
            self.off_center = True
        self.center_y = self.bottom - self.height/2

    def get_center(self):
        return [(self.left + self.width//2),self.center_y] 

    def check_contained(self,x,y):
        if y > self.top and y < self.bottom:
            slope = 1/math.sqrt(3)
            if y - self.center_y >= 0:
                slope *= -1

            y_rel = self.center_y - y
            left_bound = self.left + (y_rel)*slope
            right_bound = self.left + self.width - (y_rel)*slope

            if x >= left_bound and x <= right_bound:
                self.highlighted = True
                return True
        self.highlighted = False
        return False
        
    def draw(self,Cursor_list):
        self.Screen.blit(self.image,(self.left,self.top))
        if self.highlighted:
            Cursor_list.append([self.left-2,self.top-2])

class Field_element():
    def __init__(self,Screen,Type,ID,coords=None,position=None):
        self.Screen = Screen
        self.Type = Type
        self.ID = ID
        self.image = pygame.image.load(
            "WC_Hex/{}{}.png".format(Type,ID)
            ).convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.active = False

        if coords != None:
            self.rect.centerx,self.rect.centery = position
            self.col,self.row = coords
            self.active = True

    def translate(self,dx,dy):
        if self.active:
            self.rect.left += dx
            self.rect.top += dy

    def draw(self):
        self.Screen.blit(self.image,self.rect)

class highlight():
    def __init__(self,Screen):
        self.Screen = Screen
        self.Highlight = pygame.image.load("WC_Hex/TileHighlight.png").convert()
        self.Highlight.set_colorkey((255,0,255))
    def draw(self,rect):
        self.Screen.blit(self.Highlight,rect)