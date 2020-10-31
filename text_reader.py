import pygame.font,pygame,json
pygame.font.init()

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
