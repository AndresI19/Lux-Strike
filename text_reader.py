import pygame.font
import pygame
import json
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

class word_object():
    #Word object, is nothing more than a rendered text object, with the ability to display in a certain way
    def __init__(self,word,tags):
        self.word = word
        self.length = len(self.word)
        self.text = ""
        self.frame = 0
        self.full = False
        self.quake = False
        self.flash = False
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
                y += 1
            elif self.frame%4 == 2:
                y -= 1
        if self.flash:
            if self.frame%40 == 0:
                self.font_image = self.font.render(self.text,True,self.color,None)
            elif self.frame%40 == 20:
                self.font_image = self.font.render(self.text,True,(0,0,0),None)
        return (x,y)

    def draw(self,Screen,coordinates):
        if self.frame >= len(self.word):
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

#Settings,_________________________________________________________________
"""The following are functions that allow you load and save settings to file."""
def find(Lines,Code):
    #works just like load_text, at least the first step, could be refactored. suggested to be refactored actually
    line_count = 0
    offset = 0
    for line in Lines:
        search = line[0:len(Code)]
        if search == Code:
            return [line_count,offset]
        offset += len(line)
        line_count += 1

def recieve_setting(Lines,location,Code):
    #gets a value from file
    line = Lines[location]
    start = len(Code)+3
    setting = ''
    for char in line[start:]:
        setting += char
    return setting.strip()

"""main calls %%%%%%%%%%%%%%%%%%%%%"""
def get_settings(Code):
    #parces file, this file v for a setting by code, to retrieve data.
    File = 'Saved_Worlds/Settings.txt'
    File = open(File,"r+")
    Lines = File.readlines()
    location = find(Lines,Code)
    line_location = location[0]
    setting = recieve_setting(Lines,line_location,Code)
    File.close()
    return int(setting)

def set_setting(Code,Setting):
    #saves current settings to file, well, saves passed arguement. intended for settings
    File = 'Saved_Worlds/Settings.txt'
    File = open(File,"r+")
    Lines = File.readlines()
    location = find(Lines,Code)
    offset = location[1]
    File.seek(offset)
    File.writelines("{} = {} ".format(Code,Setting))
    File.close()

#JSON SAVE GAME - MAP READ - SAVED SETTINGS and SEEDS