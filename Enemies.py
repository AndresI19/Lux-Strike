import pygame
from Player import MOB
from RNG import seed_random_bound_int
from Tile import Icon_Enemy
import random

#holder class for grouops of enemies, all functiosn are just instructions on how to operate on the list of enemies
class ENEMIES():
    def __init__(self,Screen,Max_Parameters,World):
        self.Group = []
        self.max_enemies = 15
        self.Screen = Screen
        self.Max_Parameters = Max_Parameters
        self.spawn_random(World.seed)

    def spawn_random(self,seed):
        #finds random spawning locations. TODO: change this into a while loop to prevent spawning on top of eachother
        for i in range(self.max_enemies):
            Mx = (0,self.Max_Parameters[0]-1)
            My = (0,self.Max_Parameters[1]-1)
            x = seed_random_bound_int(seed,Mx,i)
            y = seed_random_bound_int(seed,My,i+1)
            Enemy = enemy(self.Screen,(y,x))
            self.Group.append(Enemy)

    def update_player_location(self,x,y):
        for i in range(len(self.Group)):
            self.Group[i].update_player_location(x,y)

    def update_Icon(self):
        for i in range(len(self.Group)):
            self.Group[i].Icon.update_coo(self.x,self.y)

    def Enemy_Group_Collsion(self):
        for i in range(len(self.Group)):
            for j in range(i + 1, len(self.Group)):
                self.compare(self.Group[i], self.Group[j])

    def compare(self,Subject,Object):
        SX = Subject.x + Subject.dx
        SY = Subject.y + Subject.dy
        OX = Object.x + Object.dx
        OY = Object.y + Object.dy
        if SX == OX and SY == OY:
            Object.reset_direction()
            Object.track = []

###Movement vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def choose_direction(self):
        for i in range(len(self.Group)):
            self.Group[i].choose_direction()

    def move_line(self,World,frame):
        for i in range(len(self.Group)):
            self.Group[i].move_line(World,frame)
        
    def glue(self,World):
        for i in range(len(self.Group)):
            self.Group[i].glue(World)     
###Standard Functionality vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def update_coordinates(self,World):
        for i in range(len(self.Group)):
            self.Group[i].update_coordinates(World)
    
    def translate(self,x,y):
        for i in range(len(self.Group)):
            self.Group[i].translate(x,y)

    def Icon_draw(self):
        for i in range(len(self.Group)):
            self.Group[i].Icon.draw()

"""Basic Enemy, using swanzie as a place holder --------------------------------------------------------"""
class enemy(MOB):
    def __init__(self,Screen,coordinates):
        MOB.__init__(self,Screen,coordinates)
        self.MOB_image = pygame.image.load('Enemies/Swanzai.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        
        self.direction = 'S'
        self.Icon = Icon_Enemy(self.Screen,self.y,self.x)

        self.Player_location = (0,0)
        self.aware = False
        choice = random.randrange(0,2)
        self.death_SFX = pygame.mixer.Sound("SFX/Death Honk{}.wav".format(choice))
        self.Aware_animation = exclamation_mark()

    def SFX_death(self):
        pygame.mixer.Sound.play(self.death_SFX)

    def update_player_location(self,x,y):
        self.Player_location = (x,y)

    def choose_direction(self):
        #Zombie AI: simply move to toward the player location
        Rx = self.Player_location[0] - self.x
        Ry = self.Player_location[1] - self.y
        if Rx == 0 and Ry%2 == 0:
            #verticle
            if Ry < 0:
                self.set_S()
            else:
                self.set_N()
        elif Rx < 0: #if Rx is less than 0 that means that the player is on the left
            #west
            if Ry < 0: #if Ry is less than 0 that means that the player is below
                self.set_SW()
            else:
                self.set_NW()
        elif Rx > 0:
            #east
            if Ry < 0:
                self.set_SE()
            else:
                self.set_NE()
        elif Rx == 0:
            if Ry < 0:
                if self.off_center == 1:
                    self.set_SW()
                else:
                    self.set_SE()
            else:
                if self.off_center == 1:
                    self.set_NW()
                else:
                    self.set_NE()

    def set_direction(self,dx,dy,D):
        self.dx = dx
        self.dy = dy
        self.D = D

###Scanning Functions.........................."""
    def scan(self,Player):
        if self.aware:
            self.choose_direction()
        else:
            self.scan_radius(Player,4)
        x = Player.x
        y = Player.y
        self.update_player_location(x,y)

    def scan_radius(self,Player,r):
        dy_max = (2*r + 1)
        dy_min = r + 1
        dx = 0
        self.SR_recursion(Player,dy_min,dy_max,dx)

    def SR_recursion(self,Player,dy_min,dy,dx):
        if dy < dy_min:
            return
        y = -dy + 1
        for i in range(dy):
            if dx == 0:
                self.scan_check(Player,[dx,y])
            else:
                if self.off_center == 1:
                    if dy%2 == 1:
                        x2 = -dx
                    else:
                        x2 = -(dx)+1
                    self.scan_check(Player,[dx,y])
                    self.scan_check(Player,[x2,y])
                else:
                    if dy%2 == 1:
                        x2 = dx
                    else:
                        x2 = dx-1
                    self.scan_check(Player,[-dx,y])
                    self.scan_check(Player,[x2,y])
            y += 2
        dy -= 1
        if dy%2 ==0:
            dx += 1
        self.SR_recursion(Player,dy_min,dy,dx)

    def scan_check(self,Player,rel_coord):
        y = self.y + rel_coord[1]
        x = self.x + rel_coord[0]
        if Player.x == x and Player.y == y:
            self.aware = True
            sound = pygame.mixer.Sound("SFX/aware.wav")
            pygame.mixer.Sound.play(sound)
            self.Aware_animation.activate(
                (self.MOB_rect.centerx,self.MOB_rect.top)
                )
##Standard
    def Draw(self):
        self.Screen.blit(self.MOB_image, self.MOB_rect)
        if self.Aware_animation.active:
            self.Aware_animation.activate((self.MOB_rect.centerx,self.MOB_rect.top)) #refactored for updating
            self.Aware_animation.draw(self.Screen)

class exclamation_mark():
    def __init__(self):
        self.images = []
        for i in range(3):
            image = pygame.image.load(
                'Enemies/!{}.png'.format(i)).convert()
            image.set_colorkey((255,0,255))
            self.images.append(image)
        self.images.append(image)
        self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.Frames = 10
        self.frame = 0
        self.active = False

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        self.clock()

    def activate(self,coord):
        self.rect.centerx = coord[0]
        self.rect.bottom = coord[1]
        self.active = True

    def clock(self):
        if self.frame + 1 >= self.Frames:
            self.active = False
        else:
            self.frame += 1
        self.image = self.images[self.frame//2]
