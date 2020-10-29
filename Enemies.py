import pygame
from Player import MOB
from RNG import seed_random_bound_int,seed_random_choice
from Tile import Icon_Enemy
import random
from Drops import Money_drop,Key
from Tessellation import Animation

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
    def check_kill(self,Ctrl_Vars,Drops,col,row):
        for Enemy in self.Group: #Maybe you killed something
            if Enemy.col == col and Enemy.row == row:
                Enemy.SFX_death()
                Drops.enemy_drop(Enemy,[col,row])
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
        if Subject.dx == Object.dx and Subject.dy == Object.dy:
            Object.reset_direction()
            Object.track = []

###Spawning vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def spawn_random(self,World,player):
        seed = World.seed
        enemies_left = self.max_enemies
        Mx = (0,self.Max_Parameters[0]-1)
        My = (0,self.Max_Parameters[1]-1)
        def compare():
            if not player.compare_spawn([col,row]):
                return False
            for Enemy in self.Group:
                if not Enemy.compare_spawn([col,row]):
                    return False
            if col == World.stairs[0] and row == World.stairs[1]:
                return False
            return True

        count = 0
        while enemies_left >= 0:
            col = seed_random_bound_int(seed,Mx,count)
            row = seed_random_bound_int(seed,My,count+1)
            count += 2
            if compare():
                self.choose_enemy(World,seed,count,col,row)
                enemies_left -= 1
            if count > self.max_enemies*3:
                print("Spawn went too long")
                return

        i = seed_random_bound_int(seed,(0,self.max_enemies-1),3)
        self.Group[i].key = True

    def choose_enemy(self,World,seed,count,col,row):
        def enemy_return(enemy_type):
            if enemy_type == 'swanzai':
                Enemy = swanzai(self.Screen,World,(col,row))
            elif enemy_type == 'nest':
                Enemy = nest(self.Screen,World,self,(col,row))
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
            self.Group[i].Icon.update_coo(self.col,self.row)

"""Basic Enemy, using swanzie as a place holder --------------------------------------------------------"""
class enemy(MOB):
    def __init__(self,Screen,World,coordinates):
        MOB.__init__(self,Screen,coordinates)
        self.MOB_image = pygame.image.load('Enemies/Swanzai.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        self.Map = World.Map
        
        self.direction = 'S'
        self.Icon = Icon_Enemy(self.Screen,self.col,self.row)

        self.Player_location = (0,0)
        self.aware = False
        self.death_SFX = pygame.mixer.Sound("SFX/Critical Hit 1.wav")
        self.Aware_animation = exclamation_mark(self.Screen)

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

    def update_player_location(self,col,row):
        self.Player_location = (col,row)

    def choose_direction(self,World):
        #Zombie AI: simply move to toward the player location
        direction = World.Map.get_direction([self.col,self.row],self.Player_location)
        coords = [self.col,self.row]
        if direction == 'N':
            coords = World.Map.get_N(coords)
        elif direction == 'NE':
            coords = World.Map.get_NE(coords)
        elif direction == 'SE':
            coords = World.Map.get_SE(coords)
        elif direction == 'S':
            coords = World.Map.get_S(coords)
        elif direction == 'SW':
            coords = World.Map.get_SW(coords)
        elif direction == 'NW':
            coords = World.Map.get_NW(coords)
        self.set_direction(coords,direction)


    def set_direction(self,coords,D):
        Dcol, Drow = coords
        self.dx = Dcol
        self.dy = Drow
        self.D = D

###Action Functions.........................."""
    def action(self,Player):
        if self.aware:
            self.choose_direction()
        else:
            self.scan(Player,4)
        col = Player.col
        row = Player.row
        self.update_player_location(col,row)

    def scan(self,Player,r):
        Points = self.Map.get_circle(self.col,self.row,r)
        for point in Points:
            col,row = point
            if Player.col == col and Player.row == row:
                self.aware = True
                sound = pygame.mixer.Sound("SFX/aware.wav")
                pygame.mixer.Sound.play(sound)
                self.Aware_animation.activate(
                    (self.MOB_rect.centerx,self.MOB_rect.top)
                    )

##Standard
    def Draw(self):
        if self.render:
            self.Screen.blit(self.MOB_image, self.MOB_rect)
            if self.Aware_animation.Animation.active:
                self.Aware_animation.activate((self.MOB_rect.centerx,self.MOB_rect.top)) #refactored for updating
                self.Aware_animation.draw(self.Screen)

class swanzai(enemy):
    """This will be a basic enemy that uses the most basic AI patter, it simply goes to the player
    by the shortest line. It does minimum damage and gets trapped on things easily. Dies easy too. Tutorial level"""
    def __init__(self,Screen,World,coordinates):
        enemy.__init__(self,Screen,World,coordinates)
        self.MOB_image = pygame.image.load('Enemies/Swanzai.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        choice = random.randrange(0,2)
        self.death_SFX = pygame.mixer.Sound("SFX/Death Honk{}.wav".format(choice))

class nest(enemy):
    def __init__(self,Screen,World,Enemies,coordinates):
        enemy.__init__(self,Screen,World,coordinates)
        self.MOB_image = pygame.image.load('Enemies/Swanzai_nest.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        self.Group = Enemies.Group
        self.Clutch = []
        self.Max_Clutch = 3
        self.Action_speed = 4
        self.Turn_count = 0
        self.jiggle_frame = 0
        self.jiggle = True

    def Queue_movement(self,World,n):
        return

    def action(self,player):
        """TODO: FIXME: this function is untested: should spawn in 
        an open space near the nest. Requires hex logic"""
        return

    def animate(self,x = 1):
        if self.jiggle:
            if self.jiggle_frame +1 >= 12:
                self.jiggle_frame = 0
                self.jiggle = False
            else:
                self.jiggle_frame += 1
            if self.jiggle_frame%2 == 0:
                x *= -1
            self.MOB_rect.left += x

    def Draw(self):
        self.animate(4)
        self.Screen.blit(self.MOB_image, self.MOB_rect)

class exclamation_mark():
    def __init__(self,Screen):
        images = []
        for i in range(3):
            image = pygame.image.load(
                'Enemies/!{}.png'.format(i)).convert()
            image.set_colorkey((255,0,255))
            images.append(image)
        images.append(image)
        images.append(image)
        image = images[0]
        self.rect = image.get_rect()

        self.Animation = Animation(Screen,images,2)

    def draw(self,screen):
        self.Animation.once(self.rect)

    def activate(self,coord):
        self.rect.centerx = coord[0]
        self.rect.bottom = coord[1]
        self.active = True
        self.Animation.active = True
