#World creator HUD
import pygame
import pygame.font
import json

class WC_HUD():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen_rect = Screen.get_rect()
        self.hotbar = Hotbar(Screen,Ctrl_Vars)
        self.Inventory = Inventory(Screen,Ctrl_Vars)

    def draw(self):
        if self.Ctrl_Vars.WC_Tools.HUD_Visable:
            self.hotbar.draw()
            self.Inventory.draw()

class Hotbar():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.image = pygame.image.load("WC_Hex/Toolbar.png")
        self.rect = self.image.get_rect()

        Screen_rect = Screen.get_rect()
        self.rect.centerx = Screen_rect.centerx
        self.rect.bottom = Screen_rect.bottom - 50

        self.items = self.Ctrl_Vars.WC_Tools.hotbar

        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",20)
        self.font.set_bold(True)

        self.init_text()

        self.tool_images = [None for i in range(10)]

        self.highlighted = False
        self.highlight_image = pygame.image.load("WC_Hex/Tool_Highlight.png")
        self.highlight_rect = self.highlight_image.get_rect()

    def set_tool(self,index,Type,ID):
        image = pygame.image.load(
            "WC_Hex/" + Type + str(ID) + ".png"
            ).convert()
        image.set_colorkey((255,0,255))
        rect = image.get_rect()
        rect.left = self.rect.left + index * 116 + 11
        rect.centery = self.rect.centery
        for i in range(10):
            if self.tool_images[i] != None:
                if self.tool_images[i][2] == Type and self.tool_images[i][3] == ID:
                    self.remove_tool(i)
        self.tool_images[index] = [image,rect,Type,ID]

    def remove_tool(self,index):
        self.tool_images[index] = None

    def highlight(self,index):
        self.highlighted = True
        self.highlight_rect.left = self.rect.left + index * (self.highlight_rect.width + 2)
        self.highlight_rect.top = self.rect.top

    def unhighlight(self):
        self.highlighted = False

    def draw_tool_images(self):
        for i in range(10):
            item = self.tool_images[i]
            if item != None:
                image,rect = item[0],item[1]
                self.Screen.blit(image,rect)

    def init_text(self):
        self.text = self.font.render(str(self.Ctrl_Vars.WC_Tools.ID),True,(255,255,255),None)
        self.text_rect = self.text.get_rect()
        self.text_rect.top = self.rect.bottom + 10
        self.text_rect.right = self.rect.right - 25

    def draw(self):
        self.init_text()
        self.Screen.blit(self.image,self.rect)
        if self.highlighted:
            self.Screen.blit(self.highlight_image,self.highlight_rect)
        self.draw_tool_images()
        self.Screen.blit(self.text,self.text_rect)

class Inventory():
    def __init__(self,Screen,Ctrl_Vars):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Screen_rect = Screen.get_rect()
        self.Menu_box = pygame.image.load("WC_Hex/Menu.png")
        self.rect = self.Menu_box.get_rect()
        self.rect.right = self.Screen_rect.right
        self.rect.top = self.Screen_rect.top
        
        self.mode = 0
        self.active = False

        self.init_tabs()
        self.init_boxs()
        self.switch(0)

    def init_tabs(self):
        self.Tabs = [
            Tab(self.Screen,self.Ctrl_Vars,self.rect,0,"Tiles"),
            Tab(self.Screen,self.Ctrl_Vars,self.rect,1,"Enemies"),
            Tab(self.Screen,self.Ctrl_Vars,self.rect,2,"Drops"),
            Tab(self.Screen,self.Ctrl_Vars,self.rect,3,"Game")
        ]

    def init_boxs(self):
        self.inventory = []
        with open("database.json",'r') as File:
            data = json.load(File)
            for Type in data:
                Boxs = []
                num = 0
                for item in data[Type]:
                    ID = data[Type][item]['ID']
                    box = Box(self.Screen,self.Ctrl_Vars,self.rect,Type,ID,num)
                    Boxs.append(box)
                    num += 1
                self.inventory.append(Boxs)
        File.close()
            
        self.current = self.inventory[0]

    def switch(self,ID):
        self.mode = ID
        self.current = self.inventory[ID]
        for Tab in self.Tabs:
            Tab.off()
        self.Tabs[ID].on()

    def translate(self,dx,dy):
        if self.rect.left + dx < 0 or self.rect.right + dx > self.Screen_rect.right:
            dx = 0
        if self.rect.bottom + dy > self.Screen_rect.bottom or self.rect.top + dy < self.Screen_rect.top:
            dy = 0

        self.rect.left += dx
        self.rect.bottom += dy
        for Tab in self.Tabs:
            Tab.translate(dx,dy)
        for inventory in self.inventory:
            for box in inventory:
                box.translate(dx,dy)

    def draw(self):
        if self.active:
            self.Screen.blit(self.Menu_box,self.rect)
            for Tab in self.Tabs:
                Tab.draw()
            for box in self.current:
                box.draw()

    def collision(self,x,y):
        if self.active:
            if x <= self.rect.right and x >= self.rect.left:
                if y <= self.rect.bottom and y >= self.rect.top:
                    self.sub_collsion(x,y)
                    self.Ctrl_Vars.WC_Tools.move_inv = True
                    self.Ctrl_Vars.Left_MouseDown = False
                    return
        self.Ctrl_Vars.WC_Tools.move_inv = False

    def sub_collsion(self,x,y):
        for Tab in self.Tabs:
            Tab.collision(self,x,y)
        for box in self.current:
            box.collision(x,y)

    def get_collision(self,x,y):
        if self.active:
            for box in self.current:
                result = box.get_collision(x,y)
                if result != False:
                    return result
        return False

    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True

class Tab():
    def __init__(self,Screen,Ctrl_Vars,Menu_rect,ID,text = "N/A"):
        self.Screen = Screen
        self.ID = ID
        self.Ctrl_Vars = Ctrl_Vars
        self.images = [pygame.image.load("WC_Hex/Tab.png"),pygame.image.load("WC_Hex/Tab1.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",23)
        text = font.render(text,True,(0,0,0),None)
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.centerx
        text_rect.centery = self.rect.centery
        self.images[0].blit(text,text_rect)
        self.images[1].blit(text,text_rect)

        self.rect.left = Menu_rect.left + self.rect.width * ID + 10
        self.rect.top = Menu_rect.top + 10

        self.active = False
        self.set_Type()

    def set_Type(self):
        if self.ID == 0:
            self.Type = 'Tile'
        elif self.ID == 1:
            self.Type = 'Enemies'
        elif self.ID == 2:
            self.Type = 'Drops'
        elif self.ID == 3:
            self.Type = 'Game'

    def off(self):
        self.active = False
        self.image = self.images[0]
    
    def on(self):
        self.active = True
        self.image = self.images[1]

    def translate(self,dx,dy):
        self.rect.left += dx
        self.rect.bottom += dy

    def update(self):
        return

    def collision(self,inventory,x,y):
        if x <= self.rect.right and x >= self.rect.left:
            if y <= self.rect.bottom and y >= self.rect.top:
                if self.Ctrl_Vars.Left_MouseDown:
                    inventory.switch(self.ID)
                
    def draw(self):
        self.Screen.blit(self.image,self.rect)

class Box():
    def __init__(self,Screen,Ctrl_Vars,Menu_rect,Type,ID,num):
        self.Screen = Screen
        self.Ctrl_Vars = Ctrl_Vars
        self.Type = Type
        self.ID = ID
        self.hide_text = False
        self.image = pygame.image.load("WC_Hex/EmptyItem.png")
        self.rect = self.image.get_rect()

        self.set_image()
        self.position(Menu_rect,num)

    def set_image(self):
        image = pygame.image.load(
            "WC_Hex/" + self.Type + str(self.ID) + ".png"
            ).convert()
        image.set_colorkey((255,0,255))
        image_rect = image.get_rect()
        image_rect.centerx,image_rect.centery = self.rect.centerx,self.rect.centery
        self.image.blit(image,image_rect)

    def position(self,Menu_rect,ID):
        x = ID%6
        y = ID//6
        self.rect.left = Menu_rect.left + (self.rect.width * x) + 10
        self.rect.top = Menu_rect.top + (self.rect.height * y) + 66

    def translate(self,dx,dy):
        self.rect.left += dx
        self.rect.bottom += dy

    def collision(self,x,y):
        if x <= self.rect.right and x >= self.rect.left:
            if y <= self.rect.bottom and y >= self.rect.top:
                if self.Ctrl_Vars.Left_MouseDown:
                    self.Ctrl_Vars.Left_MouseDown = False
                    self.Ctrl_Vars.WC_Tools.Type = self.Type
                    self.Ctrl_Vars.WC_Tools.ID = self.ID

    def get_collision(self,x,y):
        if x <= self.rect.right and x >= self.rect.left:
            if y <= self.rect.bottom and y >= self.rect.top:
                return [self.Type,self.ID]
        return False

    def draw(self):
        self.Screen.blit(self.image,self.rect)

class x_out():
    def __init__(self,Screen,ID):
        self.Screen = Screen
