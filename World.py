import Tile as T
import random
from Generation import Generation,Post_Generation

#World Object!
"""This is the most big baby mamma of all the objects! This object will contain a grid of every tile object int he world,
and each tile contains its individual properties. The World starts with size parameters that determain the size of the map, 
and by association the world generation time. A genertaion object is used to create a world case by case, so reinitializing this object
hence creates a new world."""
class World():
    def __init__(self,Screen,Seed):
        self.Screen = Screen
        #Size Parameters
        self.Max_Columns = 18   #width
        self.Max_Rows = 35      #height
        self.map_size_x = 90 * (self.Max_Columns)
        self.map_size_y = 26 * (self.Max_Rows)

        #Tile list
        self.Terrain = []
        #Spawn location
        self.spawn_row = 0
        self.spawn_col = 0

        #initialize generation object, creates a new world --------------------------------------
        max_parameters = (self.Max_Columns,self.Max_Rows)
        map_size = (self.map_size_x,self.map_size_y)
        generation = Generation(Seed,max_parameters,map_size,Screen)

        #save seed for display and copy paste use
        self.seed = generation.seed
        self.total_tiers = generation.total_tiers

        #pass master grid object
        self.master_grid = generation.master_grid
        post_generation = Post_Generation(self.master_grid,self.seed)
        self.stairs = post_generation.stairs

        self.master_grid = post_generation.grid
        self.transcribe_grid()
        #create world using matrix information ---------------------------------------------------
        #find spawn location*
        self.find_player_spawn()

    def transcribe_grid(self):
        #converts grid into tiles
        for col in range(len(self.master_grid)):
            self.Terrain.append([])
            for row in range(len(self.master_grid[0])):
                elevation = self.master_grid[col][row].elevation
                ID = self.master_grid[col][row].ID
                if self.master_grid[col][row].ID == 0:
                    tile = T.Water(self.Screen,col,row,0,0)
                elif self.master_grid[col][row].ID == 1:
                    tile = T.Grass(self.Screen,col,row,ID,elevation)
                elif self.master_grid[col][row].ID == 100:
                    tile = T.Brick(self.Screen,col,row,ID,elevation)
                elif self.master_grid[col][row].ID == 101:
                    tile = T.Stairs(self.Screen,col,row,ID,elevation)
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

    def translate(self,dx,dy):
        #move every element in the world
        for col in range(len(self.Terrain)):
            for row in range(len(self.Terrain[col])):
                self.Terrain[col][row].translate(dx,dy)
        
    def Background(self,perspective):
        #draw all tiles
        for col in range(len(self.Terrain)):
            for row in range(len(self.Terrain[col])):
                self.Terrain[-1-col][row].draw(perspective)
#-------------------------------------------------------------------------------------------------------------------#