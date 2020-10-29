from pygame import display,image,transform

#graphics master loops vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#main game
def Display(Screen,World,HUD,Player,Enemies,Drops):
    Screen.fill((0,0,0))
    Draw_map(World,Player,Enemies,Drops)
    HUD.draw()

def Draw_map(World,Player,Enemies,Drops):
    for row in range(World.num_rows):
        draw_row = World.num_rows - row - 1
        for col in range(World.num_cols):
            World.Map.data(col,draw_row).draw()
        if Player.row == draw_row:
            Player.Draw()
        for enemy in Enemies.Group:
            if enemy.row == draw_row:
                enemy.Draw()
        for drop in Drops.Group:
            if drop.row == draw_row:
                drop.draw()

def scale(Window,Screen,Settings):
    if not Settings.resolution == 0:
        Screen = transform.scale(Screen,(Settings.Screen_width,Settings.Screen_height))
    Window.blit(Screen,(0,0))
    display.flip()

#Menu displays
def Menu_diplay(Menu):
    Menu.draw()
    display.flip()

#graphics master loops ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^