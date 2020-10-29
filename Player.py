import pygame
from Tile import Icon_Player

#Parent class for mobile entities, the bases of the player and enemies
class MOB():
    def __init__(self,Screen,spawn_coord):
        self.Screen = Screen

        #Row column information
        self.col = 0
        self.row = 0
        self.off_center = 1

        #relative grid location
        self.D = 'SW'
        self.dy = 0
        self.dx = 0
        self.elevation = 0

        #pixel coordinate information
        self.coordinates = [0,0]
        self.spawn_col,self.spawn_row = spawn_coord

        self.track = []
        self.hitstun = False

        self.spawn()
    
    #spawn player in start location
    def compare_spawn(self,coords):
        col,row = coords
        allow = True
        if row == self.spawn_row:
            if col == self.spawn_col:
                allow = False
        return allow

    def spawn(self):
        self.col = self.spawn_col
        self.row = self.spawn_row
        if self.row%2 == 0:
            self.off_center *= -1

###Movement vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    """moving on a hexagon grid is complicated, as the columns go up and contain a list of staggard rows. The way to maneuver this is to
    give the game knowledge of the player location and call every other row staggard. Hence, if the players row value goes up (y) then the off_center value
    is flipped. Moving up or down requires a row change of plus or minus 2. At each possible control a check_move is preformed."""
    def set_NE(self,World):
        coords = World.Map.get_NE([self.col,self.row])
        if coords != False:
            col,row = coords
            self.set_direction(col,row,'NE')

    def set_N(self,World):
        #self.set_direction(0,2,'N')
        coords = World.Map.get_N([self.col,self.row])
        if coords != False:
            col,row = coords
            self.set_direction(col,row,'N')

    def set_NW(self,World):
        coords = World.Map.get_NW([self.col,self.row])
        if coords != False:
            col,row = coords
            self.set_direction(col,row,'NW')

    def set_SW(self,World):
        coords = World.Map.get_SW([self.col,self.row])
        if coords != False:
            col,row = coords
            self.set_direction(col,row,'SW')

    def set_S(self,World):
        coords = World.Map.get_S([self.col,self.row])
        if coords != False:
            col,row = coords
            self.set_direction(col,row,'S')

    def set_SE(self,World):
        coords = World.Map.get_SE([self.col,self.row])
        if coords != False:
            col,row = coords
            self.set_direction(col,row,'SE')

    def set_direction(self,col,row,D):
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
                    self.update_coordinates(World)
            else:
                self.update_coordinates(World)

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
    def update_coordinates(self,World):
        #To be carried out last frame
        self.col = self.dx
        self.row = self.dy

    def update_elevation(self,World):
        #self.elevation = World.Terrain[self.y][self.x].elevation
        self.elevation = World.Map.data(self.col,self.row).elevation

    def glue(self,World):
        self.Icon.update_coo(self.col,self.row)
        self.track = []
        #coordinates = World.Terrain[self.y][self.x].get_Character_Spot()
        coordinates = World.Map.data(self.col,self.row).get_Character_Spot()
        self.MOB_rect.centerx,self.MOB_rect.bottom = coordinates

    #Image translation
    def translate(self,x,y):
        self.MOB_rect.bottom += y
        self.MOB_rect.centerx += x
        for i in self.track:
            i[0] += x
            i[1] += y

    def get_coords(self):
        return [self.MOB_rect.centerx,self.MOB_rect.centery]

    def get_position(self):
        return [self.col,self.row]
    #Draw functions and animation loops for world entities
    def Draw(self):
        self.Screen.blit(self.MOB_image, self.MOB_rect)

"""Class for player character.-----------------------------------------------------------------------------"""
class Player(MOB):
    def __init__(self,Screen,spawn_coord):
        MOB.__init__(self,Screen,spawn_coord)
        self.MOB_images = []
        self.MOB_image = pygame.image.load('Player/SW00.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        self.Stats = Stats()
        self.hitstun = False

        self.frame = 0
        self.max_frames = 0
        self.Icon = Icon_Player(self.Screen,self.col,self.row)

        self.damage_SFX = pygame.mixer.Sound("SFX/damage.wav")
        self.last_heart_SXF = pygame.mixer.Sound("SFX/last heart.wav")

    def sprite_direction(self,D):
        self.D = D
        self.MOB_image = self.MOB_image = pygame.image.load(
            'Player/{}00.png'.format(D)
            ).convert()
        self.MOB_image.set_colorkey((255,0,255))

    def hurt_animation(self,frame):
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
    def __init__(self):
        self.Health_Points = 10
        self.Laser_Heat = 0
        self.Money = 0
        self.combo = 0
        self.keys = 0