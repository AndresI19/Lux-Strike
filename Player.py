import pygame

#Parent class for mobile entities, the bases of the player and enemies
class MOB():
    def __init__(self,Screen,coordinates,Max_Parameters):
        self.Screen = Screen

        #Row column information
        self.y = 0
        self.x = 0
        self.off_center = 1

        #relative grid location
        self.dy = 0
        self.dx = 0
        self.D = '' #no functionality yet
        self.elevation = 0

        self.coordinates = [0,0]
        self.spawn_row = coordinates[0]
        self.spawn_col = coordinates[1]

        self.Max_Rows = Max_Parameters[0]
        self.Max_Columns = Max_Parameters[1]

        self.spawn()

    #external variable assignment
    def set_direction(self,dx,dy,D):
        self.dx = dx
        self.dy = dy
        self.D = D

    def reset_direction(self):
        self.dx = 0
        self.dy = 0

    #spawn player in start location
    def spawn(self):
        self.y = self.spawn_col
        self.x = self.spawn_row
        if self.y%2 == 1:
            self.off_center *= -1

    #Draw functions and animation loops for world entities
    def Draw(self):
        #self.update_coordinates(World)
        self.Screen.blit(self.MOB_image, self.MOB_rect)

#TODO: move this into an animation function
    def update_coordinates(self,World):
        coordinates = World.Terrain[self.y][self.x].get_Character_Spot()
        self.MOB_rect.centerx = coordinates[0]
        self.MOB_rect.bottom = coordinates[1]

    def translate(self,x,y):
        self.MOB_rect.bottom += y
        self.MOB_rect.centerx += x

"""Class for player character.-----------------------------------------------------------------------------"""
class Player(MOB):
    def __init__(self,Screen,coordinates,Max_Parameters):
        MOB.__init__(self,Screen,coordinates,Max_Parameters)
        self.MOB_images = []
        self.MOB_image = pygame.image.load('Player/Player.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        self.Stats = Stats()
        self.hitstun = False

        self.frame = 0
        self.max_frames = 0

    def reset_hitstun(self): #no functionality yet
        if self.hitstun == True:
            self.hitstun = False

    def animation_clock(self):
        if self.frame + 1 >= self.max_frames:
            self.frame = 0

    def animate(self):
        self.MOB_image = self.MOB_images[self.frame//self.frame_rate]
        self.Screen.blit(self.MOB_image, self.MOB_rect)

    def set_frame_rate(self):
        self.frame_rate = self.max_frames//len(self.MOB_images)

#class for dynamic game statistics 
class Stats():
    def __init__(self):
        self.Health_Points = 10
        self.Laser_Heat = 0
        self.Money = 0