from pygame import display,image

#graphics master loops vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#main game
def Display(Screen,World,HUD,Player,Enemies,Drops):
    Screen.fill((0,0,0))
    Draw_map(World,Player,Enemies,Drops)
    HUD.draw()
    display.flip()

def Draw_map(World,Player,Enemies,Drops):
    Max_Columns = len(World.Terrain)
    for col in range(Max_Columns):
        draw_row = Max_Columns - col - 1
        for row in range(len(World.Terrain[col])):
            World.Terrain[-1-col][row].draw()
        if Player.y == draw_row:
            Player.Draw()
        for enemy in Enemies.Group:
            if enemy.y == draw_row:
                enemy.Draw()
        for drop in Drops.Group:
            if drop.y == draw_row:
                drop.draw()

#Menu displays
def Menu_diplay(Menu):
    Menu.draw()
    display.flip()

#graphics master loops ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^