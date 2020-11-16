import json

#JSON SAVE GAME - MAP READ - SAVED SETTINGS and SEEDS
#Saving World -------------------------------------------------------------
def Save_world(name,World,Player,Enemies,Drops):
    if name_collision(name):
        print("Cannot")
        return
    def find_drop_position(col,row):
        #if the drops ever start spawning in wierd loactions, itll be because of thise function. 100%
        width,height = 120,73
        elevation = World.Map.data(col,row).elevation
        bot = 1080 - row * ((height / 2)-1)
        left = col * (3*width/2 - 4)
        if row%2 == 0:
            left += 3*width/4 - 2 
        posx = left + width/2
        posy = bot - round(height * (3/4))
        if elevation > 1:
            posy -= 25
        return [posx,posy]

    path = 'Saved_Worlds/Saves.json'
    Map_info = Save_map(World)
    Player_info = [Player.col,Player.row,Player.elevation]
    PS = Player.Stats
    Stats = [PS.Health_Points,PS.Laser_Heat,PS.Money,PS.combo,PS.keys]
    Enemy_info = []
    for Enemy in Enemies.Group:
        info = [Enemy.ID,[Enemy.col,Enemy.row],Enemy.elevation]
        Enemy_info.append(info)
    Drop_info = []
    for Drop in Drops.Group:
        posx,posy = find_drop_position(Drop.col,Drop.row)
        info = [Drop.ID,[Drop.col,Drop.row],[posx,posy],Drop.value]
        Drop_info.append(info)
    save_data = {
            'Map': Map_info,
            'Player': Player_info,
            'Stats': Stats,
            'Enemies' : Enemy_info,
            'Drops' : Drop_info
    }
    with open(path,'r') as Save_file:
        all_data = json.load(Save_file)
        all_data[name] = save_data
    with open(path,'w') as Save_file:
        json.dump(all_data,Save_file)
    Save_file.close()

def Save_map(World):
    Matrix = [[None for x in range(World.num_rows)] for y in range(World.num_cols)]
    for col in range(World.num_cols):
        for row in range(World.num_rows):
            tile = World.Map.data(col,row)
            info = [tile.ID,tile.elevation,[
                tile.L_num,tile.C_num,tile.R_num
            ]]
            Matrix[col][row] = info
    spawn = [World.spawn_col,World.spawn_row]
    return {'Matrix':Matrix,'spawn': spawn}

def Load_map(name):
    path = 'Saved_Worlds/Saves.json'
    with open(path,'r') as Save_file:
        All_SAVES = json.load(Save_file)
        World = All_SAVES[name]
    Save_file.close()
    return World

def name_collision(name1):
    path = 'Saved_Worlds/Saves.json'
    with open(path,'r') as Save_file:
        all_data = json.load(Save_file)
    Save_file.close()
    for name2 in all_data:
        if name1 == name2:
            return True
    return False