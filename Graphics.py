from pygame import display,image

#graphics master loops vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#main game
def Display(Screen,World,HUD,Player,Enemies):
    Screen.fill((0,0,0))
    Draw_map(World,Player,Enemies)
    HUD.draw()
    display.flip()

def Draw_map(World,Player,Enemies):
    Max_Columns = len(World.Terrain)
    for col in range(Max_Columns):
        for row in range(len(World.Terrain[col])):
            World.Terrain[-1-col][row].draw()
        if Player.y == Max_Columns - col - 1:
            Player.Draw()
        for enemy in Enemies.Group:
            if enemy.y == Max_Columns - col - 1:
                enemy.Draw()

#Menu displays
def Menu_diplay(Menu):
    Menu.draw()
    display.flip()

#graphics master loops ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^