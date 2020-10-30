import pygame.font,pygame,json
pygame.font.init()

"""A text file is written with dialog in it. It is written in such a way
that every dialog prompt is proceeded with an identifier code. The text_reader()
modual is responsible for decoding that document into a single object. This object is 
in the format:""" 
#[{'Character':,'Image_Code':},[["sentence","sentence",...],["sentence","sentence"...], [AND REPEAT]]]
"""The dictionary that takes up the first position has two things: 
"Character" - to be initialized into small text for the box caption. is the name of who is talking
'Image_Code' - The image load path of the portrait on the screen that displays along with whos talking"""
#["sentence","sentence","sentence",...] - This part of the object is actually a 2D array 
"""Each sentence is itself a list. The list contains a set of word objects. These objects are
simple, they contain words, and any SPECIAL information passed to it through special codes in
the txt doc. These words of instructions on how to blit to the screen, but need to be passed the
past location, as they should not act as independent objects. They need to be used in context of
an external call. Each sentence in the list is a new line. Each complex object in the dialog list
is a new dialog box."""

def load_text(Code,File):
    File = open(File,"r")
    Lines = File.readlines()
    line_count = 0
    #first task is to find the section in the txt document with relevent information
    for line in Lines:
        search = line[0:len(Code)]
        if search == Code:
            line_count += 1
            dialog = paragraph_reader(Lines,line_count)
            return dialog
        line_count += 1
    File.close()

def paragraph_reader(lines,line_count):
    #tyhe text document is formated by paragraph, this function reads through it line by line
    dialog = []
    box = []
    first = True
    box_count = 0
    while True:
        line = lines[line_count]
        profile = new_box(line) #function that defines a profile information
        if profile[0] == 0:
            #new profile
            if not first:
                dialog[box_count].append(box)
                box = []
                box_count += 1
            current_profile = profile[1]
            start = (len(current_profile['Character']) + 
                len(current_profile['Image_Code']) + 
                len(current_profile['Side']) + 4)
            dialog.append([current_profile])
            sentence = load_sentence(line,start)
        elif profile[0] == 1:
            #new box same character
            start = 1
            dialog[box_count].append(box)
            box = []
            box_count += 1
            dialog.append([current_profile])
            sentence = load_sentence(line,start)
        elif profile[0] == 2:
            dialog[box_count].append(box)
            return dialog
        else:
            #new line
            sentence = load_sentence(line,0)
        box.append(sentence)
        first = False
        line_count += 1
    #return dialog

def new_box(line):
    if line[0] == '{':
        #new character new box
        profile = fill_profile(line)
        return [0,profile]
    elif line[0] == '@':
        #start new box
        return [1]
    elif line[0] == '#':
        #end
        return [2]
    else:
        #standard
        return [None]

def load_sentence(line,start):
    #creates a list of word objects that form a sentence, gives each word customizability
    sentence = []
    tags = []
    word = ""
    count = 0
    skip = False
    for char in line[start:]:
        if skip == True:
            count += 1
            skip = False
            continue
        if char == '$' or char == '%':
            #/ - New line || $ - Color || % - Effect
            tag = char + line[start+count+1]
            tags.append(tag)
            skip = True
        elif char == " ":
            word += char
            sentence.append(
                word_object(word,tags)
                )
            word = ""
            tags = []
        else:
            word += char
        count += 1
    sentence.append(
        word_object(word[:-1],tags)
        )
    return sentence

def fill_profile(line):
    #fill out profile information
    count = 0
    name = fill_to_x(line,count,',')
    count += len(name) + 1
    image = fill_to_x(line,count,',')
    count += len(image) + 1
    side = fill_to_x(line,count,'}')
    return {'Character':name,'Image_Code':image,'Side':side}

def fill_to_x(line,count,x):
    #wills information until it reaches character x which is either a ',' or a '}'
    name = ''
    active = True
    while active:
        count += 1
        char = line[count]
        if char == x:
            active = False
        else:
            name += char
    return name

#JSON SAVE GAME - MAP READ - SAVED SETTINGS and SEEDS
#Saving World -------------------------------------------------------------

def Save_world(name,World,Player,Enemies,Drops):
    path = 'Saved Worlds/Saved.json'
    Save_map(name,World)
    stats = [Player.Stats.Health_Points,Player.Stat.Laser_Heat,Player.Stats.Money,Player.combo,Player.keys]
    info = [Player.col,Player.row,Player.elevation,stats]
    for Enemy in Enemies:
        other = Enemy.get_info()
        info = [Enemy.ID,[Enemy.col,Enemy.row],Enemy.elevation,other]
    for Drop in Drops:
        info = [type(Drop),[Drop.col,Drop.row],Drop.value]

def Save_map(name,World,save_state = None):
    path = 'Saved Worlds/Saved.json'
    Matrix = [[None for x in range(World.num_cols)] for y in range(World.num_rows)]
    for col in World.num_cols:
        for row in World.num_rows:
            tile = World.Map.get_data(col,row)
            info = [tile.ID,tile.elevation,tile.cliffs]
            Matrix[col][row] = info
    spawn = [World.spawn_col,World.spawn_row]

class Dialog_box():
    def __init__(self,Screen,Ctrl_Vars):
        self.path = 'Dialog/Dialog.json'
        self.Screen = Screen
        self.Screen_rect = self.Screen.get_rect()
        self.Ctrl_Vars = Ctrl_Vars
        color,alpha = (2,2,70),185
        self.init_background(color,alpha)

        self.dialog_x,self.dialog_y = self.background_rect.left + 40, self.background_rect.top + 20
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",25)
        self.font.set_bold(True)

        self.character_name = ''

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
    def init_background(self,color,alpha):
        self.background_image = pygame.Surface(
            (self.Screen_rect.width//2,self.Screen_rect.height//5)
            )
        self.background_image.convert()
        self.background_image.fill(color)
        self.background_image.set_alpha(alpha)
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

#EXAMPLE OF DOCUMENT______________________________________________________________________________________________
"""dialog = {                           |                                                                         |
    'Event':[                           |Event code, which dialog event to look for. As many as there are events. |
        {                               |For each even there is: The name of the speaker, their picture path,     |
        'Speaker' = 'Dr.Navy',          |and the actual dialog                                                    |
        'Portrait' = 'Code',            |                                                                         |
        'Dialog' = []                   |Each entry in this list is a string, there should be may say 4 maximum.  |
        },                              |This gets converted into word objects.                                   |
        {                               |                                                                         |
        'Speaker' = 'Swanzai',          | path =  'Dialog/Dialog.json'                                            |
        'Portrait' = 'Code2',           |                                                                         |
        'Dialog' = []                   |    TODO: Maybe there will need to be voice file codes in the future     |
        }                               |                                                                         |
    ]                                   |                                                                         |
}"""#___________________________________|_________________________________________________________________________|

dialog = {
    'Event':[                      
        {                      
        'Speaker' : 'Dr.Navy',
        'Portrait' : 'Code',
        'Dialog' : ['Wah']               
        },
        {                             
        'Speaker' : 'Swanzai',
        'Portrait' : 'Code2',
        'Dialog' : []
        }
    ]
}

#TODO:NEXT INSTRUCTIONS:
#Run each entry of dialog list into a word object conversion. Find a way to pace this to the class object.
#Craft a code that will handle playing all the data simultaniusly. Instead of blitting to the screen, blit to the box.

def load_event(Event_Code):
    path =  'Dialog/Dialog.json'
    with open(path,'r') as File:
        Events = json.load(File)
        event = Events[Event_Code]
    for Page in event:
        Speaker = Page['Speaker']
        Portrait = Page['Portrait']
        Dialog = Page['Dialog']
        print(Speaker)
        print(Portrait)
        print(Dialog)

"""path =  'Dialog/Dialog.json'
with open(path,'w') as File:
    json.dump(dialog,File)
load_event('Event')"""



class word_object():
    #Word object, is nothing more than a rendered text object, with the ability to display in a certain way
    def __init__(self,word,tags):
        self.word = word
        self.length = len(self.word)
        self.text = ""
        self.frame = 0
        self.full = False
        self.quake,self.flash = False,False
        self.set_tags(tags)
        font_size = 28
        self.font = pygame.font.Font("galaxy-bt/GalaxyBT.ttf",font_size)
        self.font.set_bold(True)
        self.sound = pygame.mixer.Sound("SFX/letter type.wav")

    def init_text(self):
        self.font_image = self.font.render(self.text,True,self.color,None)
        self.font_rect = self.font_image.get_rect()

    def set_tags(self,tags):
        #/ - New line || $ - Color || % - Effect
        self.color = (255,255,255)
        for tag in tags:
            if tag[0] == '$':
                if tag[1] == 'R':
                    self.color = (255,0,0)
                elif tag[1] == 'G':
                    self.color = (0,255,0)
                elif tag[1] == 'B':
                    self.color = (0,0,255)
                elif tag[1] == 'Y':
                    self.color = (255,255,0)
            elif tag[0] == '%':
                if tag[1] == 'Q':
                    self.quake = True
                elif tag[1] == 'F':
                    self.flash = True

    def after_effects(self,coordinates):
        x = coordinates[0]
        y = coordinates[1]
        if self.quake:
            if self.frame%4 == 0:
                y += 2
            elif self.frame%4 == 2:
                y -= 2
        if self.flash:
            if self.frame%40 == 0:
                self.font_image = self.font.render(self.text,True,self.color,None)
            elif self.frame%40 == 20:
                self.font_image = self.font.render(self.text,True,(0,0,0),None)
        return (x,y)

    def draw(self,Screen,coordinates):
        if self.frame >= self.length:
            self.full = True
            pass
        else:
            self.text += self.word[self.frame]
            self.init_text()
            pygame.mixer.Sound.play(self.sound)
        self.frame += 1
        coordinates = self.after_effects(coordinates)
        Screen.blit(self.font_image,coordinates)

    def print(self):#for testing. will delete
        print(self.word)