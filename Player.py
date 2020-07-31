import pygame
from Tile import Icon_Player

#Parent class for mobile entities, the bases of the player and enemies
class MOB():
    def __init__(self,Screen,spawn_coord):
        self.Screen = Screen

        #Row column information
        self.y = 0
        self.x = 0
        self.off_center = 1

        #relative grid location
        self.D = 'SW'
        self.dy = 0
        self.dx = 0
        self.elevation = 0

        #pixel coordinate information
        self.coordinates = [0,0]
        self.spawn_row = spawn_coord[0]
        self.spawn_col = spawn_coord[1]

        self.track = []
        self.hitstun = False

        self.spawn()
        
    #spawn player in start location
    def spawn(self):
        self.y = self.spawn_col
        self.x = self.spawn_row
        if self.y%2 == 1:
            self.off_center *= -1

###Movement vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    """moving on a hexagon grid is complicated, as the columns go up and contain a list of staggard rows. The way to maneuver this is to
    give the game knowledge of the player location and call every other row staggard. Hence, if the players row value goes up (y) then the off_center value
    is flipped. Moving up or down requires a row change of plus or minus 2. At each possible control a check_move is preformed."""
    def set_NE(self):
        if self.off_center == 1:
            self.set_direction(1,1,'NE')
        elif self.off_center == -1:
            self.set_direction(0,1,'NE')

    def set_N(self):
        self.set_direction(0,2,'N')

    def set_NW(self):
        if self.off_center == 1:
            self.set_direction(0,1,'NW')
        elif self.off_center == -1:
            self.set_direction(-1,1,'NW')

    def set_SW(self):
        if self.off_center == 1:
            self.set_direction(0,-1,'SW')
        elif self.off_center == -1:
            self.set_direction(-1,-1,'SW')

    def set_S(self):
        self.set_direction(0,-2,'S')

    def set_SE(self):
        if self.off_center == 1:
            self.set_direction(1,-1,'SE')
        elif self.off_center == -1:
            self.set_direction(0,-1,'SE')

    def set_direction(self,dx,dy,D):
        self.dx = dx
        self.dy = dy
        self.sprite_direction(D)

    def reset_direction(self):
        self.dx = 0
        self.dy = 0

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
###Standard Functionality vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def update_coordinates(self,World):
        #To be carried out last frame
        self.y += self.dy
        self.x += self.dx
        if abs(self.dy) == 1:
            self.off_center *= -1
        self.reset_direction()

    def glue(self,World):
        self.Icon.update_coo(self.y,self.x)
        self.track = []
        coordinates = World.Terrain[self.y][self.x].get_Character_Spot()
        self.MOB_rect.centerx = coordinates[0]
        self.MOB_rect.bottom = coordinates[1]

    #Image translation
    def translate(self,x,y):
        self.MOB_rect.bottom += y
        self.MOB_rect.centerx += x
        for i in self.track:
            i[0] += x
            i[1] += y

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
        self.Icon = Icon_Player(self.Screen,self.y,self.x)

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