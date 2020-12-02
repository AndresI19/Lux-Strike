import pygame
from Tile import Icon_Player
from Control_variables import Screen

#Parent class for mobile entities, the bases of the player and enemies
class MOB():
    def __init__(self,spawn_coord):
        #Row column information
        self.col = 0
        self.row = 0

        #info
        self.D = 'SW'
        self.elevation = 0

        #pixel coordinate information
        self.coordinates = [0,0]
        self.spawn_col,self.spawn_row = spawn_coord

        self.track = []
        self.hitstun = False

        self.spawn()
    
    #spawn Mob in start location
    def spawn(self):
        self.col = self.spawn_col
        self.row = self.spawn_row
        self.dx = self.col
        self.dy = self.row

    #makes sure nothing is in this location before spawning
    def compare_spawn(self,coords):
        col,row = coords
        allow = True
        if row == self.spawn_row:
            if col == self.spawn_col:
                allow = False
        return allow

###Movement vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def set_NE(self,World):
        coords = World.Map.get_NE([self.col,self.row])
        if coords != False:
            self.set_direction(coords,'NE')

    def set_N(self,World):
        coords = World.Map.get_N([self.col,self.row])
        if coords != False:
            self.set_direction(coords,'N')

    def set_NW(self,World):
        coords = World.Map.get_NW([self.col,self.row])
        if coords != False:
            self.set_direction(coords,'NW')

    def set_SW(self,World):
        coords = World.Map.get_SW([self.col,self.row])
        if coords != False:
            self.set_direction(coords,'SW')

    def set_S(self,World):
        coords = World.Map.get_S([self.col,self.row])
        if coords != False:
            self.set_direction(coords,'S')

    def set_SE(self,World):
        coords = World.Map.get_SE([self.col,self.row])
        if coords != False:
            self.set_direction(coords,'SE')

    def set_direction(self,coords,D):
        col, row = coords
        self.dx =  col
        self.dy =  row
        self.sprite_direction(D)

    def reset_direction(self):
        self.dx = self.col
        self.dy = self.row

    def move_line(self,World,frame):
        if len(self.track) > 0:
            self.MOB_rect.centerx = self.track[frame][0]
            self.MOB_rect.bottom = self.track[frame][1]
            going_up = self.D == 'N' or self.D == 'NW' or self.D == 'NE'
            if going_up:
                if frame + 1 == len(self.track):
                    self.update_coordinates()
            else:
                self.update_coordinates()

    def Queue_movement(self,World,N):
        x,y = World.Map.data(self.col,self.row).get_Character_Spot()
        Fx,Fy = World.Map.data(self.dx,self.dy).get_Character_Spot()
        DX = Fx-x
        DY = Fy-y
        if DX == 0 and DY == 0:
            return
        elif DX == 0:
            increment = DY/N
            for i in range(N):
                y += increment
                self.track.append([x,y])
        else:
            m = (DY/DX)
            b = y - m * x
            increment = float(DX/N)
            for i in range(N):
                y = x*m + b
                self.track.append([round(x),round(y)])
                x += increment
###Standard Functionality vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def update_coordinates(self):
        #To be carried out last frame
        self.col = self.dx
        self.row = self.dy

    def update_elevation(self,World):
        self.elevation = World.Map.data(self.col,self.row).elevation

    def glue(self,World):
        #pastes character or object to tile main spot
        self.Icon.update_coo(self.col,self.row)
        self.track = []
        coordinates = World.Map.data(self.col,self.row).get_Character_Spot()
        self.MOB_rect.centerx,self.MOB_rect.bottom = coordinates

    def translate(self,x,y):
        #Image translation
        self.MOB_rect.bottom += y
        self.MOB_rect.centerx += x
        for i in self.track:
            i[0] += x
            i[1] += y

    def get_coords(self):
        return [self.MOB_rect.centerx,self.MOB_rect.centery]

    def get_position(self):
        return [self.col,self.row]

    def Draw(self):
        #Draw functions and animation loops for world entities
        Screen.blit(self.MOB_image, self.MOB_rect)

"""Class for player character.-----------------------------------------------------------------------------"""
class Player(MOB):
    def __init__(self,spawn_coord,DATA = None):
        MOB.__init__(self,spawn_coord)
        self.MOB_images = []
        self.MOB_image = pygame.image.load('Player/SW00.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        self.Stats = Stats(DATA)
        self.hitstun = False

        self.frame = 0
        self.max_frames = 0
        self.Icon = Icon_Player(self.col,self.row)

        self.damage_SFX = pygame.mixer.Sound("SFX/damage.wav")
        self.last_heart_SXF = pygame.mixer.Sound("SFX/last heart.wav")

        if DATA != None:
            self.col,self.row,self.elevation = DATA['Player']
            self.dx,self.dy = self.col,self.row
    
    def sprite_direction(self,D):
        #changes sprite according to direction faced
        self.D = D
        self.MOB_image = self.MOB_image = pygame.image.load(
            'Player/{}00.png'.format(D)
            ).convert()
        self.MOB_image.set_colorkey((255,0,255))

    def hurt_animation(self,frame):
        #turns you red
        self.MOB_image = self.MOB_image = pygame.image.load(
            'Player/{}10.png'.format(self.D)
            ).convert()
        self.MOB_image.set_colorkey((255,0,255))

    def walk_animation(self,frame):
        if self.D == 'SW' or self.D == 'SE': #once all animations are finished this can be removed
            x = frame
            if x >= 3:
                x = 0
            self.MOB_image = self.MOB_image = pygame.image.load(
                'Player/{}0{}.png'.format(self.D,x)
                ).convert()
            self.MOB_image.set_colorkey((255,0,255))

    def hurt(self):
        #sets variables to hurt the player, and reduce health
        if self.hitstun == False: #dont hurt twice
            self.Stats.Health_Points -= 1
            self.Stats.combo = 0
            self.hitstun = True
            self.SFX_damage()

    def reset_hitstun(self): #no functionality yet
        if self.hitstun == True:
            self.hitstun = False

##sound
    def SFX_damage(self):
        pygame.mixer.Sound.play(self.damage_SFX)
        if self.Stats.Health_Points == 1:
            pygame.mixer.Sound.play(self.last_heart_SXF)
            pygame.mixer.music.load('Music/Approach.mp3')
            pygame.mixer.music.play(-1)

#class for dynamic game statistics
class Stats():
    def __init__(self,DATA):
        if DATA == None:
            self.Health_Points = 10
            self.Laser_Heat = 0
            self.Money = 0
            self.combo = 0
            self.keys = 0
        else:
            Stats = DATA['Stats']
            self.Health_Points,self.Laser_Heat,self.Money,self.combo,self.keys = Stats