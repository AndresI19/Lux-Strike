import Tile as T
import random
from Generation import Generation,Post_Generation

#World Object!
"""This is the most big baby mamma of all the objects! This object will contain a grid of every tile object int he world,
and each tile contains its individual properties. The World starts with size parameters that determain the size of the map, 
and by association the world generation time. A genertaion object is used to create a world case by case, so reinitializing this object
hence creates a new world."""
class World():
    def __init__(self,Screen,Seed,Window,Settings):
        self.Screen = Screen
        #Size Parameters
        self.Max_Columns = 18   #width
        self.Max_Rows = 35      #height

        #Tile list
        self.Terrain = []
        self.highlighted_list = []
        #Spawn location
        self.spawn_row = 0
        self.spawn_col = 0

        self.generate_map(Seed,Window,Settings)
        self.find_player_spawn()

###MAP GENERATION/ INITIALIZATION vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def generate_map(self,Seed,Window,Settings):
        #initialize generation object, creates a new world --------------------------------------
        max_parameters = (self.Max_Columns,self.Max_Rows)
        generation = Generation(Seed,max_parameters,self.Screen,Window,Settings)
        #save seed for display and copy paste use
        self.seed = generation.seed
        self.total_tiers = generation.total_tiers

        #pass master grid object
        self.master_grid = generation.master_grid
        post_generation = Post_Generation(self.master_grid,self.seed)
        self.stairs = post_generation.stairs

        #create world using matrix information ---------------------------------------------------
        self.master_grid = post_generation.grid
        self.transcribe_grid()

    def transcribe_grid(self):
        #converts grid into tiles
        for col in range(len(self.master_grid)):
            self.Terrain.append([])
            for row in range(len(self.master_grid[0])):
                elevation = self.master_grid[col][row].elevation
                ID = self.master_grid[col][row].ID
                cliffs = self.master_grid[col][row].cliffs
                #TODO: I dont think you need to pass ID, its set for each already
                if ID == 0:
                    tile = T.Water(self.Screen,col,row,0,cliffs,0)
                elif ID == 1:
                    tile = T.Grass(self.Screen,col,row,ID,cliffs,elevation)
                elif ID == 2:
                    tile = T.Beach(self.Screen,col,row,ID,cliffs,elevation)
                elif ID == 100:
                    tile = T.Brick(self.Screen,col,row,ID,cliffs,elevation)
                elif ID == 101:
                    tile = T.Stairs(self.Screen,col,row,ID,cliffs,elevation)
                self.Terrain[col].append(tile) 

    def find_player_spawn(self):
        #what it says it does
        """simply worlds by finding the first sea level land going left to right, down to up. if it fails,
        plays just spawns in the corner"""
        for col in range(len(self.master_grid)):
            for row in range(len(self.master_grid[0])):
                if self.master_grid[col][row].ID == 1:
                    self.spawn_row = row
                    self.spawn_col = col
                    return

##Checks vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def check_bounds(self,x,y):
        BX = x < self.Max_Columns and x > -1
        BY = y < self.Max_Rows and y > -1
        if BX and BY:
            return False
        else:
            return True

    def check_cliff(self,MOB,y,x):
        if self.Terrain[y][x].ID == 0:
            return False
        else:
            current_elevation = self.Terrain[MOB.y][MOB.x].elevation
            projected_elevation = self.Terrain[y][x].elevation
            cliff_height = projected_elevation - current_elevation
            if cliff_height <= 1 and cliff_height >= -2:
                return False
            else:
                return True

##Standard Functionalities
    def translate(self,dx,dy):
        #move every element in the world
        for col in range(len(self.Terrain)):
            for row in range(len(self.Terrain[col])):
                self.Terrain[col][row].translate(dx,dy)
        
    def Draw(self):
        #draw all tiles
        for col in range(len(self.Terrain)):
            for row in range(len(self.Terrain[col])):
                self.Terrain[-1-col][row].draw()

    def reset_highlight(self):
        for i in range(len(self.highlighted_list)):
            y = self.highlighted_list[i][0]
            x = self.highlighted_list[i][1]
            self.Terrain[y][x].highlighted = False
        self.highlighted_list = []           
#-------------------------------------------------------------------------------------------------------------------#