import pygame
from Player import MOB
from RNG import seed_random_bound_int,seed_random_choice
from Tile import Icon_Enemy
import random
from Drops import Money_drop,Key

#holder class for grouops of enemies, all functiosn are just instructions on how to operate on the list of enemies
class ENEMIES():
    def __init__(self,Screen,Max_Parameters,World,Player):
        self.Screen = Screen
        self.Stats = Player.Stats
        self.Group = []
        self.Max_Parameters = Max_Parameters
        self.max_enemies = 18
        self.quotas = [['swanzai', self.max_enemies - 1],['nest',1]]
        self.spawn_random(World,Player)

###Enemy operations vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def check_kill(self,Ctrl_Vars,Drops,x,y):
        for Enemy in self.Group: #Maybe you killed something
            if Enemy.x == x and Enemy.y == y:
                Enemy.SFX_death()
                Drops.enemy_drop(Enemy,[x,y])
                self.Group.remove(Enemy)
                self.Stats.combo += 1
                return True
        return False

###Other vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
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

###Spawning vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def spawn_random(self,World,player):
        seed = World.seed
        enemies_left = self.max_enemies
        Mx = (0,self.Max_Parameters[0]-1)
        My = (0,self.Max_Parameters[1]-1)
        def compare():
            if not player.compare_spawn([y,x]):
                return False
            for Enemy in self.Group:
                if not Enemy.compare_spawn([y,x]):
                    return False
            if x == World.stairs[0] and y == World.stairs[1]:
                return False
            return True

        count = 0
        while enemies_left >= 0:
            x = seed_random_bound_int(seed,Mx,count)
            y = seed_random_bound_int(seed,My,count+1)
            count += 2
            if compare():
                self.choose_enemy(seed,count,x,y)
                #Enemy = swanzai(self.Screen,(y,x))
                enemies_left -= 1
            if count > self.max_enemies*3:
                print("Spawn went too long")
                return

        i = seed_random_bound_int(seed,(0,self.max_enemies),3)
        self.Group[i].key = True

    def choose_enemy(self,seed,count,x,y):
        def enemy_return(enemy_type):
            if enemy_type == 'swanzai':
                Enemy = swanzai(self.Screen,(y,x))
            elif enemy_type == 'nest':
                Enemy = nest(self.Screen,(y,x))
            return Enemy
            
        for i in range(len(self.quotas)):
            enemy_type,amount_left = self.quotas[i]
            if amount_left > 0:
                amount_left -= 1
                self.quotas[i][1] = amount_left
                enemy = enemy_return(enemy_type)
                self.Group.append(enemy)
                return

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
            self.Group[i].check_render()
            
    def Icon_draw(self):
        for i in range(len(self.Group)):
            self.Group[i].Icon.draw()

    def update_player_location(self,x,y):
        for i in range(len(self.Group)):
            self.Group[i].update_player_location(x,y)

    def update_Icon(self):
        for i in range(len(self.Group)):
            self.Group[i].Icon.update_coo(self.x,self.y)

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
        self.death_SFX = pygame.mixer.Sound("SFX/Critical Hit 1.wav")
        self.Aware_animation = exclamation_mark()

        self.Screen_rect = self.Screen.get_rect()
        self.check_render()
        
        self.key = False

    def check_render(self):
        self.render = False
        if self.MOB_rect.bottom >= 0 and self.MOB_rect.top <= self.Screen_rect.bottom:
            if self.MOB_rect.right >= 0 and self.MOB_rect.left <= self.Screen_rect.right:
                self.render = True

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

###Action Functions.........................."""
    def action(self,Player):
        if self.aware:
            self.choose_direction()
        else:
            self.scan(Player,4)
        x = Player.x
        y = Player.y
        self.update_player_location(x,y)

    def scan(self,Player,r):
        def check(rel_coord):
            y = self.y + rel_coord[1]
            x = self.x + rel_coord[0]
            if Player.x == x and Player.y == y:
                self.aware = True
                sound = pygame.mixer.Sound("SFX/aware.wav")
                pygame.mixer.Sound.play(sound)
                self.Aware_animation.activate(
                    (self.MOB_rect.centerx,self.MOB_rect.top)
                    )

        def Recursion(dy,dx):
            if dy < dy_min:
                return
            y = -dy + 1
            for i in range(dy):
                if dx == 0:
                    check([dx,y])
                else:
                    if self.off_center == 1:
                        if dy%2 == 1:
                            x2 = -dx
                        else:
                            x2 = -(dx)+1
                        check([dx,y])
                        check([x2,y])
                    else:
                        if dy%2 == 1:
                            x2 = dx
                        else:
                            x2 = dx-1
                        check([-dx,y])
                        check([x2,y])
                y += 2
            dy -= 1
            if dy%2 ==0:
                dx += 1
            Recursion(dy,dx)

        Player = Player
        dy_max = (2*r + 1)
        dy_min = r + 1
        dx = 0
        Recursion(dy_max,dx)

##Standard
    def Draw(self):
        if self.render:
            self.Screen.blit(self.MOB_image, self.MOB_rect)
            if self.Aware_animation.active:
                self.Aware_animation.activate((self.MOB_rect.centerx,self.MOB_rect.top)) #refactored for updating
                self.Aware_animation.draw(self.Screen)

class swanzai(enemy):
    """This will be a basic enemy that uses the most basic AI patter, it simply goes to the player
    by the shortest line. It does minimum damage and gets trapped on things easily. Dies easy too. Tutorial level"""
    def __init__(self,Screen,coordinates):
        enemy.__init__(self,Screen,coordinates)
        self.MOB_image = pygame.image.load('Enemies/Swanzai.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        choice = random.randrange(0,2)
        self.death_SFX = pygame.mixer.Sound("SFX/Death Honk{}.wav".format(choice))

class nest(enemy):
    def __init__(self,Screen,coordinates):
        enemy.__init__(self,Screen,coordinates)
        self.MOB_image = pygame.image.load('Enemies/Swanzai_nest.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()

    def Queue_movement(self,World,n):
        return

    def action(self,player):
        return

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
