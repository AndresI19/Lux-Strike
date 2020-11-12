import json
#class for player input variables; ei knowing the mouse is down or what menu is on
class Ctrl_Vars():
    def __init__(self,debug):
        self.timer_init()
        self.set_button_downs()
        self.initialized = False #memory used to know if game objects have already been loaded and dont need to be re initialized

        self.page_count = 0

        self.foreground_list = [0,0] #to rework and delete
        self.seed = "" #this is a 'soft' version of the seed, it is not used as the seed unless the player indicates so.
        self.world_name = ""
        self.Start_Vars = Start_Menu_vars()
        self.Game_Menu_Vars = Game_Menu_vars(debug)
        self.WC_Tools = WC_tools()
        self.restart_world = False

        self.keyboard = ''

        self.main = True
        self.world_creator = False
        self.WC_initialized = False


##Dynamic game stats
        self.wallet = 0
#Key Controls _____________________________________________
#HOLD KEYS____________________________________________________________
        self.Left_MouseDown = False
        self.LSHIFT_DOWN = False
        self.L_click_memory = False
        self.Left_click = False
        self.Right_MouseDown = False

    def set_button_downs(self):
        self.q_down = False
        self.w_down = False
        self.e_down = False
        self.a_down = False
        self.s_down = False
        self.d_down = False

    def mouse_down_update(self):
        #Fucntional way to know and act on the exact frame the mouse was clicked. Probably a better way to do this.
        if self.Left_MouseDown:
            if not self.L_click_memory:
                self.Left_click = True
                self.L_click_memory = True
            else:
                self.Left_click = False
        else:
            self.L_click_memory = False

    def clear_keyboard(self):
        self.keyboard = ''

#Clocks ______________________________________________________________
    def timer_init(self):
        #Turn timer variables
        self.Turn_Frames = 60
        self.turn_frame = 0
        self.TURN_PLAYER = True
        self.TURN_ENEMY = False
    
        self.phase_frame = 0
        self.phase_Frames = 4 #set to 2 for no animation frames
        self.phase_active = False

    def switch_turns(self):
        #simple flip flop function for swtiching player/AI turns
        if self.TURN_PLAYER:
            self.TURN_PLAYER = False
            self.TURN_ENEMY = True
        elif self.TURN_ENEMY:
            self.TURN_PLAYER = True
            self.TURN_ENEMY = False     
        self.turn_frame = 0

    def merge_timer(self):
        if self.phase_active:
            if self.phase_frame + 1 >= self.phase_Frames:
                self.end_phase()
            else:
                self.phase_frame += 1
        else:
            if self.turn_frame + 1 >= self.Turn_Frames:
                self.end_turn()
            else:
                self.turn_frame += 1

    def end_phase(self):
        self.phase_frame = 0
        self.phase_active = False
        self.switch_turns()

    def end_turn(self):
        self.turn_frame = 0
        self.phase_active = True   

"""Menu Controls%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
class Game_Menu_vars():
    def __init__(self,debug):
        self.menu_select = True
        self.Start_Screen = True

        self.Game_active = False #True win playing game, false if in menu
        self.Pause = False
        self.Game_Win = False
        self.Game_Over = False
        self.load_world = False #the bool called to load a new world
        self.Random = False
        self.Custom = False
        self.Load = False
        if debug == True:
            self.menu_select = False
            self.Start_Screen = False
            self.load_world = True
            self.Random = True

    def Menu_reset(self):
        self.Game_active = False #True win playing game, false if in menu
        self.menu_select = True
        #menus
        self.Pause = False
        self.Start_Screen = False
        self.Game_Win = False
        self.Game_Over = False
        self.load_world = False

class Start_Menu_vars():
    def __init__(self):
        self.Title = True
        self.load_menu = True

        self.Num_pad = False
        self.Load_pad = False
        self.Jukebox = False
        self.Display_Settings = False
        self.Sound_Settings = False

    def Menu_reset(self):
        self.load_menu = True

        self.Title = False
        self.Num_pad = False
        self.Load_pad = False
        self.Jukebox = False
        self.Display_Settings = False
        self.Sound_Settings = False

    def Set_Menu(self,Menu):
        if Menu == "Title":
            self.Title = True
        elif Menu == "Num_Pad":
            self.Num_pad = True
        elif Menu == "Load_Pad":
            self.Load_pad = True
        elif Menu == "Jukebox":
            self.Jukebox = True
        elif Menu == "Display_Settings":
            self.Display_Settings = True
        elif Menu == "Sound_Settings":
            self.Sound_Settings = True

class WC_tools():
    def __init__(self):
        self.ID = 1
        self.Type = 'Tile'
        self.HUD_Visable = True
        self.Pause = False

        self.hotbar = [{'Type':None,'ID':None} for i in range(10)]
        self.active_tool = self.hotbar[0]

        self.move_inv = False
    
    def set_hotbar(self,index,Type,ID):
        count = 0
        for item in self.hotbar:
            if item['Type'] == Type and item['ID'] == ID:
                self.remove_hotbar(count)
                count += 1

        self.hotbar[index]['Type'] = Type
        self.hotbar[index]['ID'] = ID

    def set_TypeID(self,index):
        self.Type = self.hotbar[index]['Type']
        self.ID = self.hotbar[index]['ID']

    def remove_hotbar(self,index):
        self.hotbar[index]['Type'] = None
        self.hotbar[index]['ID'] = None

    def toggle_HUD(self):
        if self.HUD_Visable:
            self.HUD_Visable = False
        else:
            self.HUD_Visable = True