#Hexagon Data Structure
class Hex_Grid():
    def __init__(self,Cols = 1,Rows = 1):
        """This is a data structure for a hexagonal tessilation and will greatly simplify the methods
        of operating within the structure. The general rules are:
        -The orientation of this matrix is defined by having a true North/South but no East/West.
        -This is like a matrix but every other ROW is considered staggered. %2 is staggered
        -Each data entry has 6 adjecent entries (unlesss the edges are reached).
        -These adjecent sides depend on the stagger greatly
        -Because the stagger, it can be expected that there will be more Rows than Cols
        self.Grid = []"""
        self.num_cols = Cols
        self.num_rows = Rows
        self.num = 0 #iterator
        self.total = self.num_rows*self.num_cols
        self.Matrix = []
        self.get_ = {
            'N':self.get_N,
            'NE':self.get_NE,
            'SE':self.get_SE,
            'S':self.get_S,
            'SW':self.get_SW,
            'NW':self.get_NW
        }
        self.build()

    def build(self):
        #Simple function that initializes objects matrix base, all objects default to None
        for col in range(self.num_cols):
            self.Matrix.append([])
            for row in range(self.num_rows):
                self.Matrix[col].append(None)
    
    def check_bounds(self,col,row):
        #Makes sure that indices passed are contianed, will not allow negatice indices.
        if col >= 0 and col < self.num_cols:
            if row >= 0 and row < self.num_rows:
                return True
        return False

    def index_allowed(self,col,row):
        #makes sure that such an index is allowable.
        if col >= -self.num_cols and col < self.num_cols:
            if row >= -self.num_rows and row < self.num_rows:
                return True
        return False       
        
    def write(self,Data,col,row):
        #Writes data to given index
        if self.index_allowed(col,row):
            self.Matrix[col][row] = Data

    def data(self,col,row):
        #Retrives data at given index
        if self.index_allowed(col,row):
            return self.Matrix[col][row]

#directionals
    """Moving on a hexagon grid is complicated, as the columns go up and contain a list of staggard rows. The way to maneuver this is to
    define every other row as staggard. Hence, if row%2 = 0 col goes += 1. Moving up or down requires a row change of plus or minus 2. 
    At each possible control a check_move is preformed."""
    def get_NE(self,coords):
        col,row = coords
        stagger = self.check_stagger(row)
        if stagger == -1:
            C,R = col,row + 1
        elif stagger == 1:
            C,R = col + 1,row + 1
        if self.check_bounds(C,R):
            return [C,R]
        else:
            return False

    def get_N(self,coords):
        col,row = coords
        C,R = col,row + 2
        if self.check_bounds(C,R):
            return [C,R]
        else:
            return False

    def get_NW(self,coords):
        col,row = coords
        stagger = self.check_stagger(row)
        if stagger == 1:
            C,R = col,row + 1
        elif stagger == -1:
            C,R = col - 1,row + 1
        if self.check_bounds(C,R):
            return [C,R]
        else:
            return False

    def get_SW(self,coords):
        col,row = coords
        stagger = self.check_stagger(row)
        if stagger == 1:
            C,R = col,row - 1
        elif stagger == -1:
            C,R = col - 1,row - 1
        if self.check_bounds(C,R):
            return [C,R]
        else:
            return False

    def get_S(self,coords):
        col,row = coords
        C,R = col,row - 2
        if self.check_bounds(C,R):
            return [C,R]
        else:
            return False

    def get_SE(self,coords):
        col,row = coords
        stagger = self.check_stagger(row)
        if stagger == 1:
            C,R = col +1,row - 1
        elif stagger == -1:
            C,R = col,row - 1
        if self.check_bounds(C,R):
            return [C,R]
        else:
            return False
#
    def check_stagger(self,row):
        if row%2 == 0:
            stagger = 1 #True
        else:
            stagger = -1
        return stagger

    def get_circle(self,col,row,r=1):
        def Recursion(Length,Expansion):
            if Length <= Min_Cond:
                return
            offset = -Length + 1
            for i in range(Length):
                if Expansion == 0:
                    Points.append([col+Expansion,row+offset])
                else:
                    if stagger == 1:
                        if Length%2 == 1:
                            Dcol = -Expansion
                        else:
                            Dcol = -Expansion + 1
                        Points.append([col + Expansion,row+offset])
                        Points.append([col + Dcol,row+offset])
                    else:
                        if Length%2 == 1:
                            Dcol = Expansion
                        else:
                            Dcol = Expansion - 1
                        #Left
                        Points.append([col - Expansion,row+offset])
                        #Right
                        Points.append([col + Dcol,row+offset])
                offset += 2
            Length -= 1
            if Length%2 == 0:
                Expansion += 1
            Recursion(Length,Expansion)

        Min_Cond = r
        Length = (2*r + 1)
        stagger = self.check_stagger(row)
        Expansion = 0
        Points = []
        Recursion(Length,Expansion)
        return Points

    def get_direction(self,Subj,Obj):
        col,row = Subj
        col2,row2 = Obj
        Dcol,Drow = col2-col, row2 - row
        if Dcol == 0:
            if Drow%2 == 0:
                #verticle assumes that 0,0 is not an option
                if Drow < 0:
                    return 'S'
                else:
                    return 'N'
            elif Drow < 0:
                if self.check_stagger(row) == 1: #Tie breaker
                    return 'SW'
                else:
                    return 'SE'
            else:
                if self.check_stagger(row) == 1: #Tie Breaker
                    return 'NW'
                else:
                    return 'NE'
        elif Dcol < 0: #if Dcol is less than 0 that means that the obj is on the left
            #west
            if Drow < 0: #if Drow is less than 0 that means that the obj is below
                return 'SW'
            else:
                return 'NW'
        elif Dcol > 0:
            #east
            if Drow < 0:
                return 'SE'
            else:
                return 'NE'

    def __str__(self):
        x = ""
        for row in range(self.num_rows):
            y = ''
            for col in range(self.num_cols):
                y += str(type(self.data(col,-1-row)))[8:-2] + "|"
            if row%2 == 0:
                y = "__|" + y
            x += y + "\n"
        return x

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.num < self.total:
            self.Itrow = self.num//self.num_cols
            self.Itcol = self.num - (self.Itrow * self.num_cols)
            self.num = self.num + 1
            return self.Matrix[self.Itcol][self.Itrow]
        else:
            self.Itcol = 0
            self.ItRow = 0
            raise StopIteration()

    def __getitem__(self,key):
        row = key//self.num_cols
        col = key - (row * self.num_cols)
        return self.Matrix[col][row]

    def __setitem__(self,key,data):
        row = key//self.num_cols
        col = key - (row * self.num_cols)
        self.Matrix[col][row] = data
        
    def __len__(self):
        return self.total

#print("Hello\nWorld")
"""Grid = Hex_Grid(11,17)
for i in range(len(Grid)):
    Grid[i] = i
"""