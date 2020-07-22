import pygame
from math import sqrt,trunc
from numpy.random import choice

#Mother class of all tiles. All tiles are the same size and contain the same number of elements. 
"""FIXME: Needs a lot of work, 
-fix render over sight
-rework visibility to remove redundent blits
-fix water elevation issue
-clean up unused variables
-phase out mother class image calls
-Not a singke things here that isnt a work in progress
"""

class Tile():
    def __init__(self,Screen,col,row,ID,cliffs,elevation):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.set_ledge_draw_height(cliffs)
        
        #Row Column information
        self.col = col
        self.row = row

        #TODO: Rework this entire display on and off system its muddy
        self.Left_display = False
        self.Center_display = False
        self.Right_display = False

        self.ID = ID
        self.elevation = elevation
        
        #place holder images
        self.Hexagon_image = pygame.image.load('Tiles/Grass/H00.png').convert()
        self.Left_image = pygame.image.load('Tiles/Grass/L00.png').convert()
        self.Center_image = pygame.image.load('Tiles/Grass/C00.png').convert()
        self.Right_image = pygame.image.load('Tiles/Grass/R00.png').convert()
        #--------------------------------------------------------------

        self.background = 0
        self.set_HexProperties()
        self.Icon = Icon(Screen,col,row)
        self.highlighted = False
        self.highlight = highlight(Screen)

    #check if the block in the foreground in front of the player is tall and needs to be transparent
    def check_tall_block(self,MOB,Ctrl_Vars):
        dZ = self.elevation - MOB.elevation
        if dZ > 1:
            Ctrl_Vars.foreground_list = [self.col,self.row]
            self.Hexagon_image.set_alpha(120)

    def reset_alpha(self):
        self.background = 0
        self.Hexagon_image.set_alpha(255)

    def set_HexProperties(self):
        #Hexagon Properties
        self.Hexagon_rect = self.Hexagon_image.get_rect()
        self.height = self.Hexagon_rect.bottom
        self.width = self.Hexagon_rect.right

        self.side_length = self.Hexagon_rect.right/2
        self.outline = 1

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

    """EXPIRMENTAL"""
    def set_ledge_draw_height(self,cliffs):
        self.L_num = cliffs[0]
        self.C_num = cliffs[1]
        self.R_num = cliffs[2]

    def draw(self):
        if self.render:
            #filling in elevation gaps with copies
            self.Screen.blit(self.Hexagon_image, self.Hexagon_rect)
            self.draw_extended_terrain()
            if self.highlighted:
                self.highlight.draw(self.Hexagon_rect)

    def draw_extended_terrain(self):
        #clean up this entire thing its gross and redundent
            for i in range(self.L_num):
                Left_rect = self.Left_rect.copy()
                Left_rect.bottom += self.Center_rect.height * i
                self.Screen.blit(self.Left_image, Left_rect)
            for j in range(self.C_num):
                Center_rect = self.Center_rect.copy()
                Center_rect.bottom += self.Center_rect.height * j
                self.Screen.blit(self.Center_image, Center_rect)
            for k in range(self.R_num):
                Right_rect = self.Right_rect.copy()
                Right_rect.bottom += self.Center_rect.height * k
                self.Screen.blit(self.Right_image, Right_rect)

    #initialize position based on location in matrix
    def build(self):
        self.Hexagon_rect.bottom = self.Screen_rect.bottom - self.col * ((self.height / 2)-1)
        self.Hexagon_rect.left = self.row * (self.width + self.side_length - 4)
        if self.col%2 == 0:
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

    #blit list
    def check_render(self):
        """FIXME: fix tiles whose ledges should render but hexagon doesnt. Add actual margin
        Happens rarely at the top but enough to notice will become more of a problem the more elevation becomes important"""
        margin_guess = 120
        bottom_bound = self.Hexagon_rect.top <= self.Screen_rect.bottom - margin_guess
        top_bound = self.Hexagon_rect.bottom >= self.Screen_rect.top
        verticle_bound = bottom_bound and top_bound

        left_bound = self.Hexagon_rect.right >= self.Screen_rect.left + margin_guess
        right_bound = self.Hexagon_rect.left <= self.Screen_rect.right - margin_guess
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
    def __init__(self,Screen,col,row,ID,cliffs,elevation):
        Tile.__init__(self,Screen,col,row,ID,cliffs,elevation)
        #animation image list
        self.Hexagon_images = []
        for i in range(8):
            image = pygame.image.load(
                'Tiles/Water/H0{}.png'.format(i)
                ).convert()
            image.set_colorkey((255,0,255))
            self.Hexagon_images.append(image)

        self.Left_image = pygame.image.load('Tiles/Water/L00.png').convert()
        self.Center_image = pygame.image.load('Tiles/Water/C00.png').convert()
        self.Right_image = pygame.image.load('Tiles/Water/R00.png').convert()
        #magenta is transparent.
        self.Center_image.set_colorkey((255,0,255))
        self.Left_image.set_colorkey((255,0,255))
        self.Right_image.set_colorkey((255,0,255))

        self.frame_count = 0
        self.frames = 104

        self.Icon = Icon_Water(Screen,col,row)

    #special draw instructions for animation
    def draw(self):
        self.clock()
        if self.render:
            self.draw_extended_terrain()
        
    def clock(self):
        if self.frame_count + 1 >= self.frames:
            self.frame_count = 0
        self.Screen.blit(self.Hexagon_images[self.frame_count//13], self.Hexagon_rect)
        if self.highlighted:
            self.highlight.draw(self.Hexagon_rect)
        self.frame_count += 1

class Grass(Tile):
    def __init__(self,Screen,col,row,ID,cliffs,elevation):
        Tile.__init__(self,Screen,col,row,ID,cliffs,elevation)
        #randomize grass environement 
        Choice = choice(range(4),1,False,[.55,.35,.05,.05])
        self.Hexagon_image = pygame.image.load(
            'Tiles/Grass/H0{}.png'.format(Choice[0])
            ).convert()

        self.Left_image = pygame.image.load('Tiles/Grass/L00.png').convert()
        self.Center_image = pygame.image.load('Tiles/Grass/C00.png').convert()
        self.Right_image = pygame.image.load('Tiles/Grass/R00.png').convert()

        self.set_colorkey()
        self.Icon = Icon_Grass(Screen,col,row,elevation)

class Mountain(Tile):
    def __init__(self,Screen,col,row,ID,cliffs,elevation):
        Tile.__init__(self,Screen,col,row,ID,cliffs,elevation)
        self.Hexagon_image = pygame.image.load('Tiles/Mountain/H00.png').convert()
        self.Left_image = pygame.image.load('Tiles/Mountain/L00.png').convert()
        self.Center_image = pygame.image.load('Tiles/Mountain/C00.png').convert()
        self.Right_image = pygame.image.load('Tiles/Mountain/R00.png').convert()
        self.set_colorkey()

        self.Icon = Icon_Brick(Screen,col,row,1)

class Beach(Tile):
    def __init__(self,Screen,col,row,ID,cliffs,elevation):
        Tile.__init__(self,Screen,col,row,ID,cliffs,elevation)
        Choice = choice(range(4),1,False,[.75,.10,.10,.05])
        self.Hexagon_image = pygame.image.load(
            'Tiles/Beach/H0{}.png'.format(Choice[0])
            ).convert()

        self.Left_image = pygame.image.load('Tiles/Beach/L00.png').convert()
        self.Center_image = pygame.image.load('Tiles/Beach/C00.png').convert()
        self.Right_image = pygame.image.load('Tiles/Beach/R00.png').convert()
        self.set_colorkey()

        self.Icon = Icon_Sand(Screen,col,row,1)

class Brick(Tile):
    def __init__(self,Screen,col,row,ID,cliffs,elevation):
        Tile.__init__(self,Screen,col,row,ID,cliffs,elevation)
        self.Hexagon_image = pygame.image.load('Tiles/Brick/H00.png').convert()
        self.Left_image = pygame.image.load('Tiles/Brick/L00.png').convert()
        self.Center_image = pygame.image.load('Tiles/Brick/C00.png').convert()
        self.Right_image = pygame.image.load('Tiles/Brick/R00.png').convert()
        self.set_colorkey()

        self.Icon = Icon_Brick(Screen,col,row,1)

class Stairs(Tile):
    def __init__(self,Screen,col,row,ID,cliffs,elevation):
        Tile.__init__(self,Screen,col,row,ID,cliffs,elevation)
        self.Hexagon_image = pygame.image.load('Tiles/Brick/H01.png').convert()
        self.Left_image = pygame.image.load('Tiles/Brick/L00.png').convert()
        self.Center_image = pygame.image.load('Tiles/Brick/C00.png').convert()
        self.Right_image = pygame.image.load('Tiles/Brick/R00.png').convert()
        self.set_colorkey()

        self.Icon = Icon_Stairs(Screen,col,row,1)

#Class for the mini map icons, one per tile instance
class Icon():
    def __init__(self,Screen,col,row):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.image = pygame.image.load('Tiles/Grass/Mini00.png').convert()
        self.image.set_colorkey((255,0,255))
        self.image_rect = self.image.get_rect()

        self.col = col
        self.row = row
        self.position()

    def position(self):
        width = 15
        height = 13
        offset = 2*width/3

        self.image_rect.bottom = self.Screen_rect.bottom - self.col * (trunc(height/2)) - 32
        self.image_rect.left = self.row * (width + offset/2) + 1550
        if self.col%2 == 0:
            self.image_rect.left += offset

    def draw(self):
        self.Screen.blit(self.image, self.image_rect)

class Icon_Water(Icon):
    def __init__(self,Screen,col,row):
        Icon.__init__(self,Screen,col,row)
        self.image = self.image = pygame.image.load('Tiles/Water/Mini00.png').convert()
        self.image.set_colorkey((255,0,255))

class Icon_Grass(Icon):
    def __init__(self,Screen,col,row,elevation):
        Icon.__init__(self,Screen,col,row)
        self.image = self.image = pygame.image.load(
            'Tiles/Grass/Mini0{}.png'.format(elevation)).convert()
        self.image.set_colorkey((255,0,255))

class Icon_Brick(Icon):
    def __init__(self,Screen,col,row,elevation):
        Icon.__init__(self,Screen,col,row)
        self.image = self.image = pygame.image.load('Tiles/Brick/Mini00.png').convert()
        self.image.set_colorkey((255,0,255))

class Icon_Stairs(Icon):
    def __init__(self,Screen,col,row,elevation):
        Icon.__init__(self,Screen,col,row)
        self.image = self.image = pygame.image.load('Tiles/Brick/Mini01.png').convert()
        self.image.set_colorkey((255,0,255))

class Icon_Player(Icon):
    def __init__(self,Screen,col,row):
        Icon.__init__(self,Screen,col,row)
        self.image = self.image = pygame.image.load('Tiles/Icons/Mini01.png').convert()
        self.image.set_colorkey((255,0,255))
    def update_coo(self,col,row):
        self.col = col
        self.row = row
        self.position()

class Icon_Enemy(Icon):
    def __init__(self,Screen,col,row):
        Icon.__init__(self,Screen,col,row)
        self.image = self.image = pygame.image.load('Tiles/Icons/Mini00.png').convert()
        self.image.set_colorkey((255,0,255))

    def update_coo(self,col,row):
        self.col = col
        self.row = row
        self.position()

class Icon_Sand(Icon):
    def __init__(self,Screen,col,row,elevation):
        Icon.__init__(self,Screen,col,row)
        self.image = pygame.image.load('Tiles/Beach/Mini00.png').convert()
        self.image.set_colorkey((255,0,255))

class highlight():
    def __init__(self,Screen):
        self.Screen = Screen
        self.image = pygame.image.load('HUD/Highlight.png').convert()
        self.image.set_colorkey((255,0,255))
        self.image_rect = self.image.get_rect()
    def update(self,host_rect):
        self.image_rect.bottom = host_rect.bottom
        self.image_rect.centerx = host_rect.centerx
    def draw(self,host_rect):
        self.update(host_rect)
        self.Screen.blit(self.image, self.image_rect)