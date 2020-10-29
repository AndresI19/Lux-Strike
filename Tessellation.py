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
        self.Matrix = []
        self.build()

    def build(self):
        for col in range(self.num_cols):
            self.Matrix.append([])
            for row in range(self.num_rows):
                self.Matrix[col].append(None)
    
    def check_bounds(self,col,row):
        if col >= 0 and col < self.num_cols:
            if row >= 0 and row < self.num_rows:
                return True
        #print("col: {} Row: {}".format(col,row))
        return False

    def index_allowed(self,col,row):
        if col >= -self.num_cols and col < self.num_cols:
            if row >= -self.num_rows and row < self.num_rows:
                return True
        #print("Index not allowed: col: {} Row: {}".format(col,row))
        return False       
        
    def write(self,Data,col,row):
        if self.index_allowed(col,row):
            self.Matrix[col][row] = Data
        else:
            return None
            #print("Out of bounds error: Col:{} Row:{} is not supported".format(col,row))

    def data(self,col,row):
        if self.index_allowed(col,row):
            return self.Matrix[col][row]

    def print(self):
        for row in range(self.num_rows):
            x = "   "
            for col in range(self.num_cols):
                x += str(self.Matrix[col][-1-row]) + "|"
            if row%2 == 0:
                x = "S_" + x
            print(x)

    def print_type(self):
        for row in range(self.num_rows):
            x = "   "
            for col in range(self.num_cols):
                x += str(type(self.data(col,-1-row)))[13:-2] + "|"
            if row%2 == 0:
                x = "S_" + x
            print(x)

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

class Animation():
    def __init__(self,Screen,reel,speed = 1):
        self.Screen = Screen
        self.reel = reel
        self.speed = speed
        self.frames = len(reel) * self.speed
        self.active = False

        self.count = 0 

    def loop(self,rect):
        if self.count + 1 >= self.frames:
            self.count = 0
        else:
            self.image = self.reel[self.count//self.speed]
            self.count += 1
        self.Screen.blit(self.image,rect)

    def once(self,rect):
        if self.count + 1 >= self.frames:
            self.active = False
        else:
            self.image = self.reel[self.count//self.speed]
            self.count += 1
        self.Screen.blit(self.image,rect)

"""Grid = Hex_Grid(11,17)
c,r = 4,7
Points = Grid.get_diamond(c,r,2)
print(Points)
count = "_1__"
for point in Points:
    col,row = point
    Grid.write(count,col,row)
Grid.write("WAH_",c,r)
Grid.print()"""