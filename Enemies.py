import pygame,random
from Player import MOB
from RNG import seed_random_bound_int,seed_random_choice
from Tile import Icon_Enemy
from Drops import Money_drop,Key
from Tessellation import Animation

#holder class for grouops of enemies, all functiosn are just instructions on how to operate on the list of enemies
class ENEMIES():
    def __init__(self,Screen,Max_Parameters,World,Player,DATA = None):
        self.Screen = Screen
        self.Stats = Player.Stats
        self.Group = []
        if DATA == None:
            self.Max_Parameters = Max_Parameters
            self.max_enemies = 18
            self.quotas = [['swanzai', self.max_enemies - 3],['nest',1],['rabbo',2]]
            self.spawn_random(World,Player)
        else:
            for data in DATA['Enemies']:
                #[Enemy.ID,[Enemy.col,Enemy.row],Enemy.elevation]
                ID,coords,elevation = data
                if ID == 0:
                    enemy = swanzai(self.Screen,World,coords,elevation)
                elif ID == 1:
                    enemy = nest(self.Screen,World,self,coords,elevation)
                elif ID == 2:
                    enemy = rabbit(self.Screen,World,coords,elevation)
                self.Group.append(enemy)

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
            elif enemy_type == 'rabbo':
                Enemy = rabbit(self.Screen,World,(col,row))
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
    def update_coordinates(self):
        for i in range(len(self.Group)):
            self.Group[i].update_coordinates()
    
    def translate(self,x,y):
        for i in range(len(self.Group)):
            self.Group[i].translate(x,y)
            self.Group[i].check_render()
            
    def Icon_draw(self):
        for i in range(len(self.Group)):
            self.Group[i].Icon.draw()

    def update_player_location(self,Player):
        for i in range(len(self.Group)):
            self.Group[i].update_player_location(Player)

    def update_Icon(self):
        for i in range(len(self.Group)):
            self.Group[i].Icon.update_coo(self.col,self.row)

"""Basic Enemy, using swanzie as a place holder --------------------------------------------------------"""
class enemy(MOB):
    def __init__(self,Screen,World,coordinates,elevation = None):
        MOB.__init__(self,Screen,coordinates)
        self.MOB_image = pygame.image.load('Enemies/Swanzai.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        self.Map = World.Map
        
        self.direction = 'S'
        self.Icon = Icon_Enemy(self.Screen,self.col,self.row)

        self.Player_location = (0,0)
        self.death_SFX = pygame.mixer.Sound("SFX/Critical Hit 1.wav")

        self.Screen_rect = self.Screen.get_rect()
        self.check_render()
        if elevation != None:
            self.elevaiton = elevation
        
        self.key = False
        self.init_aware()

    def init_aware(self):
        self.aware = False
        images = []
        for i in range(3):
            image = pygame.image.load(
                'Enemies/!{}.png'.format(i)).convert()
            image.set_colorkey((255,0,255))
            images.append(image)
        images.append(image)
        images.append(image)
        self.exclaimation = Animation(self.Screen,images,3,2)

    def check_render(self):
        self.render = False
        if self.MOB_rect.bottom >= 0 and self.MOB_rect.top <= self.Screen_rect.bottom:
            if self.MOB_rect.right >= 0 and self.MOB_rect.left <= self.Screen_rect.right:
                self.render = True

    def SFX_death(self):
        pygame.mixer.Sound.play(self.death_SFX)

    def update_player_location(self,Player):
        self.Player_location = [Player.col,Player.row]

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
        if coords != False:
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
        self.update_player_location(Player)

    def scan(self,Player,r):
        Points = self.Map.get_circle(self.col,self.row,r)
        for point in Points:
            col,row = point
            if Player.col == col and Player.row == row:
                self.aware = True
                sound = pygame.mixer.Sound("SFX/aware.wav")
                pygame.mixer.Sound.play(sound)
                self.exclaimation.toggle()

##Standard
    def Draw(self):
        if self.render:
            self.Screen.blit(self.MOB_image, self.MOB_rect)
            if self.exclaimation.clock():
                rect = self.exclaimation.get_rect()
                rect.centerx = self.MOB_rect.centerx
                rect.bottom = self.MOB_rect.top
                self.exclaimation.draw(rect)

class swanzai(enemy):
    """This will be a basic enemy that uses the most basic AI patter, it simply goes to the player
    by the shortest line. It does minimum damage and gets trapped on things easily. Dies easy too. Tutorial level"""
    def __init__(self,Screen,World,coordinates,elevation = None):
        enemy.__init__(self,Screen,World,coordinates,elevation)
        self.ID = 0
        self.MOB_image = pygame.image.load('Enemies/Swanzai.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        choice = random.randrange(0,2)
        self.death_SFX = pygame.mixer.Sound("SFX/Death Honk{}.wav".format(choice))

class nest(enemy):
    def __init__(self,Screen,World,Enemies,coordinates,elevation = None):
        enemy.__init__(self,Screen,World,coordinates,elevation)
        self.ID = 1
        self.MOB_image = pygame.image.load('Enemies/Swanzai_nest.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()
        self.Group = Enemies.Group
        self.Clutch = []
        self.Max_Clutch = 3
        self.Action_speed = 7
        self.Turn_count = 0
        self.jiggle_frame = 0
        self.jiggle = True
        self.spawn_circle = World.Map.get_circle(self.col,self.row,1)
        for point in self.spawn_circle:
            col,row = point
            if World.Map.check_bounds(col,row) == False:
                self.spawn_circle.remove([col,row])
        self.spawn_circle.remove([self.col,self.row])
        self.World = World

    def Queue_movement(self,World,n):
        return

    def action(self,player):
        def compare(coords):
            col, row = coords
            if player.col == col and player.row == row:
                return False
            for Enemy in self.Group:
                if Enemy.col == col and Enemy.row == row:
                    return False
            return True

        def choose_spawn():
            active = True
            temp = self.spawn_circle.copy()
            while active:
                choice = random.choice(temp)
                if compare(choice):
                    active = False
                    new_mob = swanzai(self.Screen,self.World,choice)
                    self.Group.append(new_mob)
                    self.Clutch.append(new_mob)
                else:
                    temp.remove(choice)
                    if len(temp) == 0:
                        active = False

        if self.Turn_count + 1 >= self.Action_speed:
            self.Turn_count = 0
            choose_spawn()
        else:
            if self.Turn_count + 1 == self.Action_speed - 1:
                self.jiggle = True
            self.Turn_count += 1

    def animate(self,x = 1):
        if self.jiggle:
            if self.jiggle_frame +1 >= 32:
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

class rabbit(enemy):
    def __init__(self,Screen,World,coordinates,elevation = None):
        enemy.__init__(self,Screen,World,coordinates,elevation)
        self.ID = 2
        self.MOB_image = pygame.image.load('Enemies/Rabbo.png').convert()
        self.MOB_image.set_colorkey((255,0,255))
        self.MOB_rect = self.MOB_image.get_rect()

    def action(self,Player):
        if self.aware:
            self.choose_direction()
        else:
            self.scan(Player,2)
        self.update_player_location(Player)

    def choose_direction(self,World):
        #Zombie AI: simply move to toward the player location
        direction = World.Map.get_direction([self.col,self.row],self.Player_location)
        coords = [self.col,self.row]
        if direction == 'N':
            coords = World.Map.get_S(coords)
        elif direction == 'NE':
            coords = World.Map.get_SW(coords)
        elif direction == 'SE':
            coords = World.Map.get_NW(coords)
        elif direction == 'S':
            coords = World.Map.get_N(coords)
        elif direction == 'SW':
            coords = World.Map.get_NE(coords)
        elif direction == 'NW':
            coords = World.Map.get_SE(coords)
        self.set_direction(coords,direction)

