import pygame
from math import sqrt,trunc
from numpy.random import choice
from Graphics import Animation
import json,sys
from Control_variables import Screen,ScreenRect

#Mother class of all tiles. All tiles are the same size and contain the same number of elements. 
"""FIXME: Needs a lot of work, 
-fix render over sight
-rework visibility to remove redundent blits
-clean up unused variables
-Not a single things here that isnt a work in progress"""

#Tile graphic loading
def load_graphics(self):
    def Hexagon():
        Hexdata = Isometric['Hexagon']
        HPath = Hexdata['Path']
        Total = Hexdata['Total']
        Choice = Hexdata['Choice']
        self.images = []
        if Total == 1:
            self.Hexagon_image = pygame.image.load(
                    "{}{}0.png".format(Path,HPath)
                ).convert()
            self.Hexagon_image.set_colorkey((255,0,255))
        else:
            images = []
            for i in range(Total):
                image = pygame.image.load(
                        "{}{}{}.png".format(Path,HPath,i)
                    ).convert()
                image.set_colorkey((255,0,255))
                images.append(image)
            if Choice == False:
                Speed = Hexdata['Speed']
                self.Animation = Animation(images,Speed)
                self.draw = self.animated_draw
                return
            else:
                value = choice(range(4),1,False,Choice)[0]
                self.Hexagon_image = pygame.image.load(
                        "{}{}{}.png".format(Path,HPath,value)
                    ).convert()
        self.draw = self.standard_draw

    def cliffs():
        self.Left_image = pygame.image.load(
                "{}{}0.png".format(Path,Isometric['Left']['Path'])
            ).convert()
        self.Center_image = pygame.image.load(
                "{}{}0.png".format(Path,Isometric['Center']['Path'])
            ).convert()
        self.Right_image = pygame.image.load(
                "{}{}0.png".format(Path,Isometric['Right']['Path'])
            ).convert()

    with open("database.json",'r') as File:
        data = json.load(File)
        data = data['Tile']
        Path = data[self.Type]['Path']
        Isometric = data[self.Type]['Isometric']
        cliffs()
        Hexagon()
        self.set_colorkey()

#Tile dictionary:
def TileClass():
    TileID = {}
    with open('database.json','r') as File:
        data = json.load(File)['Tile']
        for key in data:
            TileID[data[key]['ID']] = getattr(sys.modules[__name__], key)
    File.close()
    return TileID

class Tile():
    def __init__(self,col,row,cliffs,elevation):
        self.set_ledge_draw_height(cliffs)
        
        #Row Column information
        self.col = col
        self.row = row
        self.elevation = elevation
        self.Type = None
        
        #place holder images
        self.Hexagon_image = pygame.image.load('Tiles/NotFound/H0.png').convert()
        self.Left_image = pygame.image.load('Tiles/NotFound/L0.png').convert()
        self.Center_image = pygame.image.load('Tiles/NotFound/C0.png').convert()
        self.Right_image = pygame.image.load('Tiles/NotFound/R0.png').convert()
        self.set_colorkey()
        #--------------------------------------------------------------

        self.set_HexProperties()
        self.highlighted = False
        self.highlight = highlight()

        #self.Obstacle = None

    #BLIT INSTRUCTIONS
    def standard_draw(self):
        if self.render:
            #filling in elevation gaps with copies
            Screen.blit(self.Hexagon_image, self.Hexagon_rect)
            self.draw_extended_terrain()
            if self.highlighted:
                self.highlight.draw(self.Hexagon_rect)

    def animated_draw(self):
        #self.clock()
        self.Animation.clock()
        if self.render:
            self.draw_extended_terrain()
            self.Animation.draw(self.Hexagon_rect)
            if self.highlighted:
                self.highlight.draw(self.Hexagon_rect)

    #check if the block in the foreground in front of the player is tall and needs to be transparent
    def check_tall_block(self,MOB,Ctrl_Vars):
        dZ = self.elevation - MOB.elevation
        if dZ > 1:
            Ctrl_Vars.foreground_list = [self.col,self.row]
            self.Hexagon_image.set_alpha(120)

    def reset_alpha(self):
        self.Hexagon_image.set_alpha(255)

    def set_HexProperties(self):
        #Hexagon Properties
        self.Hexagon_rect = self.Hexagon_image.get_rect()
        self.height = self.Hexagon_rect.bottom
        self.width = self.Hexagon_rect.right

        self.side_length = self.width/2
        self.outline = 2

        self.height = 73#self.side_length * sqrt(3), this temporary specification prevents scalability of image size ;(
        self.offset = (self.side_length*(3/2))

        #Left Ledge
        self.Left_rect = self.Left_image.get_rect()
        self.Center_rect = self.Center_image.get_rect()
        self.Right_rect = self.Right_image.get_rect()

        #Position
        self.Hexagon_rect_bottom = 0
        self.Hexagon_rect.left = 0

        self.build()
        self.elevate()
        self.check_render()

    def set_ledge_draw_height(self,cliffs):
        self.L_num = cliffs[0]
        self.C_num = cliffs[1]
        self.R_num = cliffs[2]

    #initialize position based on location in matrix
    def build(self):
        self.Hexagon_rect.bottom = ScreenRect.bottom - self.row * ((self.height / 2)-1)
        self.Hexagon_rect.left = self.col * (self.width + self.side_length - 4)
        if self.row%2 == 0:
            self.Hexagon_rect.left += self.offset - 2


        self.Center_rect.top = self.Hexagon_rect.bottom - self.outline
        self.Center_rect.centerx = self.Hexagon_rect.centerx

        self.Left_rect.left = self.Hexagon_rect.left
        self.Left_rect.bottom = self.Center_rect.bottom - self.outline

        self.Right_rect.bottom = self.Center_rect.bottom - self.outline
        self.Right_rect.right = self.Hexagon_rect.right

        self.Character_Spot_Mainx = self.Hexagon_rect.centerx
        self.Character_Spot_Mainy = self.Hexagon_rect.bottom - round(self.Hexagon_rect.height * (3/4))
    
    #returns coordinates of character main location
    def get_Character_Spot(self):
        x = self.Character_Spot_Mainx
        y = self.Character_Spot_Mainy
        return [x,y]

    #presents the illusion of tile height
    def elevate(self):
        if self.elevation > 0:
            self.Hexagon_rect.bottom -= self.Center_rect.height * (self.elevation)
            self.Center_rect.bottom -= self.Center_rect.height * (self.elevation) -1
            self.Left_rect.bottom -= self.Center_rect.height * (self.elevation) -2
            self.Right_rect.bottom -= self.Center_rect.height * (self.elevation) -2 
            self.Character_Spot_Mainy -= self.Center_rect.height

    #move tile across screen, most likely used in a for loop
    def translate(self,x,y):
        self.Hexagon_rect.bottom += y
        self.Hexagon_rect.left += x

        self.Left_rect.bottom += y
        self.Left_rect.left += x

        self.Center_rect.bottom += y
        self.Center_rect.left += x

        self.Right_rect.bottom += y
        self.Right_rect.left += x

        self.Character_Spot_Mainx = self.Hexagon_rect.centerx
        self.Character_Spot_Mainy = self.Hexagon_rect.bottom - round(self.Hexagon_rect.height/4)
        self.check_render()
        
    def draw_extended_terrain(self):
        #clean up this entire thing its gross and redundent
            for i in range(self.L_num):
                Left_rect = self.Left_rect.copy()
                Left_rect.bottom += self.Center_rect.height * i
                Screen.blit(self.Left_image, Left_rect)
            for j in range(self.C_num):
                Center_rect = self.Center_rect.copy()
                Center_rect.bottom += self.Center_rect.height * j
                Screen.blit(self.Center_image, Center_rect)
            for k in range(self.R_num):
                Right_rect = self.Right_rect.copy()
                Right_rect.bottom += self.Center_rect.height * k
                Screen.blit(self.Right_image, Right_rect)

    def check_render(self):
        """FIXME: fix tiles whose ledges should render but hexagon doesnt. Add actual margin
        Happens rarely at the top but enough to notice will become more of a problem the more elevation becomes important"""
        bottom_bound = self.Hexagon_rect.top <= ScreenRect.bottom - 150
        tile_bottom = self.Hexagon_rect.bottom + self.C_num * self.Center_rect.height
        top_bound = tile_bottom >= ScreenRect.top
        
        verticle_bound = bottom_bound and top_bound

        left_bound = self.Hexagon_rect.right >= ScreenRect.left + 203 
        right_bound = self.Hexagon_rect.left <= ScreenRect.right - 240
        horizontal_bound = left_bound and right_bound

        if verticle_bound and horizontal_bound:
            self.render = True
        else:
            self.render = False

    def set_colorkey(self):
        colorkey = (255,0,255)
        self.Center_image.set_colorkey(colorkey)
        self.Left_image.set_colorkey(colorkey)
        self.Right_image.set_colorkey(colorkey)
        self.Hexagon_image.set_colorkey(colorkey)
        self.Hexagon_image.set_alpha(255)

#tile daughter classes.
class Water(Tile):
    def __init__(self,col,row,cliffs,elevation):
        Tile.__init__(self,col,row,cliffs,elevation)
        self.ID = 0
        self.Type = 'Water'
        load_graphics(self)
        self.Icon = Icon_Tile(col,row,self.Type,elevation)

class Grass(Tile):
    def __init__(self,col,row,cliffs,elevation):
        Tile.__init__(self,col,row,cliffs,elevation)
        self.ID = 1
        self.Type = 'Grass'
        load_graphics(self)
        self.Icon = Icon_Tile(col,row,self.Type,elevation)

class Mountain(Tile):
    def __init__(self,col,row,cliffs,elevation):
        Tile.__init__(self,col,row,cliffs,elevation)
        self.ID = 3
        self.Type = 'Mountain'
        load_graphics(self)
        self.Icon = Icon_Tile(col,row,self.Type,elevation)

class Beach(Tile):
    def __init__(self,col,row,cliffs,elevation):
        Tile.__init__(self,col,row,cliffs,elevation)
        self.ID = 2
        self.Type = 'Beach'
        load_graphics(self)
        self.Icon = Icon_Tile(col,row,self.Type,elevation)

class Brick(Tile):
    def __init__(self,col,row,cliffs,elevation):
        Tile.__init__(self,col,row,cliffs,elevation)
        self.ID = 100
        self.Type = 'Brick'
        load_graphics(self)
        self.Icon = Icon_Tile(col,row,self.Type,elevation)

class Stairs(Tile):
    def __init__(self,col,row,cliffs,elevation):
        Tile.__init__(self,col,row,cliffs,elevation)
        self.ID = 101
        self.Type = 'Stairs'
        load_graphics(self)
        self.Icon = Icon_Tile(col,row,self.Type,elevation)

class Door(Tile):
    def __init__(self,col,row,cliffs,elevation):
        Tile.__init__(self,col,row,cliffs,elevation)
        self.ID = 102
        self.Type = 'Door'
        load_graphics(self)
        self.open = False
        self.Icon = Icon_Tile(col,row,self.Type,elevation)
    
    def Open(self,World):
        if not self.open:
            self.open = True
            self.change_elevation(-2)
            self.update_neighbor(World,2)
            sound = pygame.mixer.Sound("SFX/door open.wav")
            pygame.mixer.Sound.play(sound)
    
    def update_neighbor(self,World,x):
        coords = World.Map.get_NW([self.col,self.row])
        if coords != False:
            World.Map.data(coords[0],coords[1]).R_num += 2
        coords = World.Map.get_NE([self.col,self.row])
        if coords != False:
            World.Map.data(coords[0],coords[1]).L_num += 2

    def change_elevation(self,x):
        self.elevation += x
        self.L_num += x
        self.C_num += x
        self.R_num += x
        self.Hexagon_rect.bottom -= self.Center_rect.height * (x)
        self.Center_rect.bottom -= self.Center_rect.height * (x) -1
        self.Left_rect.bottom -= self.Center_rect.height * (x) -2
        self.Right_rect.bottom -= self.Center_rect.height * (x) -2 
        self.Character_Spot_Mainy -= self.Center_rect.height * x

#Class for the mini map icons, one per tile instance
class Icon():    
    def __init__(self,col,row):
        self.col = col
        self.row = row
        self.init_image()
        self.position()

    def init_image(self):
        self.image = pygame.image.load('Tiles/Icons/Mini.png').convert()
        self.image.set_colorkey((255,0,255))
        self.image_rect = self.image.get_rect()

    def position(self):
        width = 15
        height = 13
        offset = 2*width/3

        self.image_rect.bottom = ScreenRect.bottom - self.row * (trunc(height/2)) - 32
        self.image_rect.left = self.col * (width + offset/2) + 1550
        if self.row%2 == 0:
            self.image_rect.left += offset

    def gradiantUP(self):
        cap = [
            self.color[i]*1.25// 10 for i in range(3)
        ]
        for i in range(3):
            self.color[i] -= (25 * self.elevation)
            if self.color[i] < cap[i]:
                self.color[i] = cap[i]

    def gradiantDOWN(self):
        start = [
            self.color[i]*1.25// 10 for i in range(3)
        ] 
        for i in range(3):
            start[i] += (25 * self.elevation)
            if start[i] > self.color[i]:
                start[i] = self.color[i]
        self.color = start

    def draw(self):
        Screen.blit(self.image, self.image_rect)

class Icon_Tile(Icon):
    def __init__(self,col,row,Type,elevation):
        self.Type = Type
        self.elevation = elevation

        with open('database.json','r') as File:
            data = json.load(File)['Tile']
            self.color = data[self.Type]['Icon']
        File.close()

        Icon.__init__(self,col,row)

    def init_image(self):
        self.init_color = self.gradiantUP
        self.init_color()
        shape = pygame.image.load('Tiles/Icons/Mini.png').convert()
        self.image_rect = shape.get_rect()
        shape.set_colorkey((255,255,255))
        canvas = pygame.Surface(
            (self.image_rect.width,self.image_rect.height)
        )
        canvas.fill(self.color)
        canvas.blit(shape,(0,0))
        canvas.set_colorkey((255,0,255))
        self.image = canvas 

class Icon_Player(Icon):
    def __init__(self,col,row):
        Icon.__init__(self,col,row)
        self.image = self.image = pygame.image.load('Tiles/Icons/Mini01.png').convert()
        self.image.set_colorkey((255,0,255))
    def update_coo(self,col,row):
        self.col = col
        self.row = row
        self.position()

class Icon_Enemy(Icon):
    def __init__(self,col,row):
        Icon.__init__(self,col,row)
        self.image = self.image = pygame.image.load('Tiles/Icons/Mini00.png').convert()
        self.image.set_colorkey((255,0,255))

    def update_coo(self,col,row):
        self.col = col
        self.row = row
        self.position()

#Obstacles
class Obstacles():
    def __init__(self,Tile):
        self.image = pygame.image.load("Tiles/Obstacles/Tree00.png").convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        x,y = Tile.get_Character_Spot()
        self.rect.centerx = x
        self.rect.bottom = y + 20

    def draw(self):
        Screen.blit(self.image,self.rect)

#Misc
class highlight():
    def __init__(self):
        self.image = pygame.image.load('HUD/Highlight.png').convert()
        self.image.set_colorkey((255,0,255))
        self.image_rect = self.image.get_rect()
    def update(self,host_rect):
        self.image_rect.bottom = host_rect.bottom
        self.image_rect.centerx = host_rect.centerx
    def draw(self,host_rect):
        self.update(host_rect)
        Screen.blit(self.image, self.image_rect)