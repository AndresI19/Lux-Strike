import pygame
import pygame.font
import text_reader
pygame.mixer.init()

#Envelope class containing all border rectangles
class HUD():
    def __init__(self,Settings,Screen,Ctrl_Vars,World,Player,Enemies):
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.Settings = Settings
        self.HUD_Borders = self.make_HUD_Borders()
        self.Player_Stats = Player_Stats(Screen,Player.Stats)
        self.Money_bar = Currency_bar(Screen,Player.Stats)
        self.Mini_map = Mini_map(Screen,World,Player,Enemies)
        self.Dialog_box = Dialog_box(Screen,Ctrl_Vars)
        self.Combo = Combo_meter(Screen,Player.Stats)
        self.Keys = Keys(Screen,Player.Stats)
        self.Laser_Gauge = Laser_Gauge(Screen,Player.Stats)
        self.init_text(World)

    def init_text(self,World):
        #initialize the text that displays the seed
        self.text_color = ((255,255,255))
        self.font_size = 15
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",self.font_size)
        self.font.set_bold(True)
        self.font_image = self.font.render("Seed: "+ World.seed,True,self.text_color,None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.right = self.Screen_rect.right - 1
        self.font_rect.bottom = self.Screen_rect.bottom -3

    def make_HUD_Borders(self):
        #left border margin
        Left = pygame.image.load("HUD/Left frame.png").convert()
        Left.set_colorkey((255,0,255))
        Left_rect = Left.get_rect()

        #Bottom border margin
        Bottom = pygame.image.load("HUD/Bottom frame.png").convert()
        Bottom.set_colorkey((255,0,255))
        Bottom_rect = Bottom.get_rect()
        Bottom_rect.bottom = Left_rect.bottom
        Bottom_rect.left = Left_rect.right

        #Right border margin
        Right = pygame.image.load("HUD/Right frame.png").convert()
        Right.set_colorkey((255,0,255))
        Right_rect = Right.get_rect()
        Right_rect.right = self.Screen_rect.right

        Middle = pygame.image.load("HUD/Map frame.png").convert()
        Middle.set_colorkey((255,0,255))
        Middle_rect = Middle.get_rect()
        Middle_rect.bottom = Bottom_rect.top
        Middle_rect.right = Right_rect.right

        #add all border margins to a list for easy operation
        HUD_Borders = [Left,Bottom,Right,Middle]
        HUD_rects = [Left_rect,Bottom_rect,Right_rect,Middle_rect]

        return (HUD_Borders,HUD_rects)

    def draw(self):
        for i in range(len(self.HUD_Borders[0])):
            self.Screen.blit(self.HUD_Borders[0][i],self.HUD_Borders[1][i])
        self.Mini_map.draw()
        self.Player_Stats.draw()
        self.Money_bar.draw()
        self.Combo.draw()
        self.Keys.draw()
        self.Laser_Gauge.draw()
        self.Screen.blit(self.font_image,self.font_rect)
        self.Dialog_box.draw()
        
#Left
class Player_Stats():
    def __init__(self,Screen,Stats):
        self.Screen = Screen
        self.Stats = Stats
        self.Empty_bar = pygame.image.load("HUD/HealthBar.png").convert()
        self.Empty_bar.set_colorkey((255,0,255))
        self.Empty_bar_rect = self.Empty_bar.get_rect()
        self.Empty_bar_rect.top = 5
        self.Empty_bar_rect.left = 5

        self.Health_Points_display = []
        self.position_health_points()

    def position_health_points(self):
        j = 2
        i = 0
        flip = 1
        while i <= 5:
            healthIcon = HealthIcon(j,i)
            self.Health_Points_display.append(healthIcon)
            if flip == 1:
                j -= 1
                i += 1
            else:
                j += 1
            flip *= -1

    def draw(self):
        self.Screen.blit(self.Empty_bar,self.Empty_bar_rect)
        #draw each icon over it
        for i in range(self.Stats.Health_Points):
            self.Health_Points_display[i].draw(self.Screen)

class HealthIcon():
    def __init__(self,x,y):
        #a single health icon
        self.HealthIcon = pygame.image.load("HUD/HealthIcon.png").convert()
        self.HealthIcon.set_colorkey((255,0,255))
        self.HealthIcon_rect = self.HealthIcon.get_rect()
        self.build(x,y)

    def build(self,x,y):
        outline = 1

        width = self.HealthIcon_rect.right
        side_length = width//2
        offset = side_length * (3/2)
        
        position_y = 41
        position_x = 5

        self.HealthIcon_rect.bottom = x * ((self.HealthIcon_rect.height / 2) - outline) + position_y
        self.HealthIcon_rect.left = y * (width + side_length) + position_x
        if x%2 == 0:
            self.HealthIcon_rect.left += offset

    def draw(self,Screen):
        Screen.blit(self.HealthIcon,self.HealthIcon_rect)

class Mini_map():
    def __init__(self,Screen,World,Player,Enemies):
        self.Screen = Screen
        self.World = World
        self.Player = Player
        self.Enemies = Enemies
        self.scaling_factor = 4

    def draw(self):
        for col in range(len(self.World.Terrain)):
            for row in range(len(self.World.Terrain[col])):
                self.World.Terrain[-1-col][row].Icon.draw()
        self.Enemies.Icon_draw()
        self.Player.Icon.draw()

class Dialog_box():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.Ctrl_Vars = Ctrl_Vars
        self.init_background()

        self.dialog_x = self.background_rect.left + 30
        self.dialog_y = self.background_rect.top + 10

        self.character_name = ''
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",25)
        self.font.set_bold(True)

        self.frame = 0
        self.box = []
        self.dialog = []
        self.dialog_play = False
        self.SFX = pygame.mixer.Sound("SFX/new dialog box.wav")

    def init_dialog(self,Code):
        File = "Dialog/Dialog.txt"
        self.dialog = text_reader.load_text(Code,File)
        self.init_box()
        self.dialog_play = True

##Initializing Dialog Box
    def init_background(self):
        self.background_image = pygame.Surface(
            (self.Screen_rect.width//2,self.Screen_rect.height//5)
            )
        self.background_image.convert()
        self.background_image.fill((2,2,70))
        self.background_image.set_alpha(185)
        self.background_rect = self.background_image.get_rect()
        self.background_rect.centerx = self.Screen_rect.centerx
        self.background_rect.bottom = self.Screen_rect.bottom - 100

    def init_box(self):
        if self.Ctrl_Vars.box_count < len(self.dialog):
            count = self.Ctrl_Vars.box_count
            profile = self.dialog[count][0]
            self.character_name = profile['Character']
            self.init_character_text()
            self.image_path = profile['Image_Code']
            self.portrait_side = profile['Side']
            self.init_portraits()
            self.box = self.dialog[count][1]
            pygame.mixer.Sound.play(self.SFX)

    def init_character_text(self):
        self.font_image = self.font.render(self.character_name,True,(255,255,255),None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.right = self.background_rect.right - 15
        self.font_rect.bottom = self.background_rect.bottom - 10

    def init_portraits(self):
        self.portrait = pygame.image.load("Portraits/{}.png".format(
            self.image_path)).convert()
        self.portrait.set_colorkey((255,0,255))
        self.portrait_rect = self.portrait.get_rect()
        self.portrait_rect.centery = self.background_rect.centery
        self.portrait_rect.centerx = (self.background_rect.centerx - (
            int(self.portrait_side)*(self.background_rect.right - self.background_rect.centerx + 75))
            )
        if int(self.portrait_side) == -1:
            self.portrait = pygame.transform.flip(self.portrait, True, False)
##Drawing Dialog Box
    def draw(self):
        if self.dialog_play:
            if self.Ctrl_Vars.box_count < len(self.dialog):
                self.Screen.blit(self.background_image, self.background_rect)
                self.Screen.blit(self.font_image, self.font_rect)
                self.text_scroll()
                self.Screen.blit(self.portrait, self.portrait_rect)
            else:
                self.dialog_play = False
                self.Ctrl_Vars.box_count = 0

    def text_scroll(self):
        x = self.dialog_x
        y = self.dialog_y
        for line in self.box:
            for word in line:
                word.draw(self.Screen,(x,y))
                if word.full == False:
                    break
                x += word.font_rect.right
            if not line[-1].full:
                break
            y += word.font_rect.bottom
            x = self.dialog_x
        
#When worlds become sufficiently large this will be necessary but it would need to be accompanied by rendering function and would require defined space
"""TODO:    def translate(self,x,y):
        for col in range(len(self.World.Terrain)):
            for row in range(len(self.World.Terrain[col])):
                self.World.Terrain[-1-col][row].image_rect.centerx += x / self.scaling_factor
                self.World.Terrain[-1-col][row].image_rect.bottom += y / self.scaling_factor"""

#Planned UI elements
"""TODO: class Terrain_info():
    def __init__(self,Screen):
        self.Screen = Screen"""

class Currency_bar():
    def __init__(self,Screen,Stats):
        self.Screen = Screen
        self.Stats = Stats
        self.Currency_images = []
        for i in range(17):
            image = pygame.image.load(
                'HUD/Money{}.png'.format(i)
                ).convert()
            image.set_colorkey((255,0,255))
            self.Currency_images.append(image)
        self.Currency_image = self.Currency_images[0]
        self.Currency_rect = self.Currency_image.get_rect()
        self.position((1735,20))

        self.value = self.Stats.Money
        self.display_amount = self.value
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",28)
        self.font.set_bold(True)
        self.init_text()

        self.animate_text = False
        self.Frames = 17 * 2
        self.frame = 0
        self.frame2 = 0
        
    def position(self,coords):
        self.Currency_rect.left = coords[0]
        self.Currency_rect.top = coords[1]

    def init_text(self):
        self.font_image = self.font.render(
            str(self.display_amount),True,(255,255,255),None)
        self.font_rect = self.font_image.get_rect()
        self.font_rect.left = self.Currency_rect.right + 10
        self.font_rect.centery = self.Currency_rect.centery

    def clock(self):
        if self.frame + 1 >= self.Frames * 5:
            if self.frame2 + 1 >= self.Frames:
                self.frame = 0
                self.frame2 = 0
            self.frame2 += 1
        else:
            self.frame += 1
        self.Currency_image = self.Currency_images[self.frame2//2]

    def queue(self):
        self.value = self.Stats.Money
        differance = self.value - self.display_amount
        self.increment = differance // 5
        self.animate_text = True

    def number_animate(self):
        if self.animate_text:
            if self.display_amount >= self.value:
                self.display_amount = self.value
                self.animate_text = False
            else:
                self.display_amount += self.increment
            self.init_text()

    def draw(self):
        self.clock()
        self.number_animate()
        self.Screen.blit(self.Currency_image,self.Currency_rect)
        self.Screen.blit(self.font_image,self.font_rect)

class Combo_meter():
    def __init__(self,Screen,Stats):
        """---------------------------
        I DO NOT HAVE LICENCE TO USE FONT
        ------------------------------"""
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.Stats = Stats
        size = 60
        self.color = (255,255,255)
        self.font = pygame.font.Font("HUD/Error.ttf",size)
        self.frame = 0
        self.frames = 10
        self.update()

    def color_switch(self):
        if self.Stats.combo < 8:
            x = 255 - self.Stats.combo*64
            y=255
            if self.Stats.combo >= 4:
                x = 0
                y = 255 - (self.Stats.combo - 4)*64
            self.color = (255,y,x)
        else:
            self.color = (255,0,0)

    def update(self):
        self.animate = True
        self.color_switch()
        self.image = self.font.render("x{}".format(self.Stats.combo),False,self.color,None)
        self.rect = self.image.get_rect()
        self.position()

    def position(self):
        self.rect.right = self.Screen_rect.right - 40
        self.rect.top = self.Screen_rect.top + 200

    def Animate(self):
        if self.animate:
            if self.frame >= self.frames:
                self.frame = 0
                self.animate = False
            else:
                x = 2
                if self.frame%2 ==0:
                    x = -1
                self.rect.right += x*2
                self.frame += 1
                
    def draw(self):
        self.Animate()
        self.Screen.blit(self.image,self.rect)

class Keys():
    def __init__(self,Screen,Stats):
        """---------------------------
        I DO NOT HAVE LICENCE TO USE FONT
        ------------------------------"""
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.Stats = Stats
        size = 40
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",size)
        self.init_key()

        self.update()

    def init_key(self):
        self.key = pygame.image.load('Drops/Key.png').convert()
        self.key.set_colorkey((255,0,255))
        self.key_rect = self.key.get_rect()
        self.key_rect.right = self.Screen_rect.right - 85
        self.key_rect.top = self.Screen_rect.top + 120

    def update(self):
        color = (255,255,255)
        self.text_image = self.font.render(": x{}".format(self.Stats.keys),False,color,None)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.left = self.key_rect.right
        self.text_rect.bottom = self.key_rect.bottom
     
    def draw(self):
        self.Screen.blit(self.key,self.key_rect)
        self.Screen.blit(self.text_image,self.text_rect)

class Laser_Gauge():
    def __init__(self,Screen,Stats):
        self.Screen = Screen
        self.Screen_rect = Screen.get_rect()
        self.Stats = Stats
        self.colors = [(0,0,0),(0,255,217),(187,255,0),(255,255,0),(255,115,0),(255,0,42)]
        self.init_images()
        self.init_charge()
        self.frames = 0
        self.count = 0

    def init_images(self):
        self.background = pygame.image.load("HUD/gauge back.png")
        self.background_rect = self.background.get_rect()
        self.fore_bar = pygame.image.load("HUD/gauge fore.png").convert()
        self.fore_bar.set_colorkey((255,0,255))
        self.bar_rect = self.fore_bar.get_rect()

        self.background_rect.left = self.Screen_rect.left + 30
        self.background_rect.bottom = self.Screen_rect.bottom - 100

        self.bar_rect.left = self.background_rect.left + 6
        self.bar_rect.bottom = self.background_rect.bottom - 90

    def init_charge(self):
        i = self.Stats.Laser_Heat
        color = self.colors[i]
        self.charge = pygame.Surface((62,85*i))
        self.charge.fill(color)
        self.charge_rect = self.charge.get_rect()
        self.charge_rect.left = self.background_rect.left + 6
        self.charge_rect.bottom = self.background_rect.bottom - 10
        self.set_jiggle()

    def set_jiggle(self):
        self.loop = False
        self.frames = 6 + 2 * (self.Stats.Laser_Heat * self.Stats.Laser_Heat)/2
        self.range = self.Stats.Laser_Heat

    def jiggle(self,):
        x = self.range
        if self.frames != 0:
            if self.count%2 == 0:
                x *= -1
            self.background_rect.left += x
            self.charge_rect.left += x
            self.bar_rect.left += x
            self.count += 1
            if self.count+1  >= self.frames:
                self.frames = 0
                self.count = 0

    def draw(self):
        self.jiggle()
        self.Screen.blit(self.background,self.background_rect)
        self.Screen.blit(self.charge,self.charge_rect)
        for i in range(4):
            bar = self.bar_rect.copy()
            bar.bottom -= i * 85
            self.Screen.blit(self.fore_bar,bar)


"""#Bottom
class Time_Weather():
    def __init__(self,Screen):
        self.Screen = Screen

class Weapons_Menu():
    def __init__(self,Screen):
        self.Screen = Screen"""