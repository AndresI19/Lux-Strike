# Lux-Strike
Project Name: Lux Strike
Author: Andres Irarragorri
Other Credits:
    Electo Bridge.mp3 = Jake Sanabria| Website : Jakesanabria.com, IG : @youandme.ost,
    Vicrory Animation = Dan Valle| IG: @dandaminifig
==================================================================================================================
This is an early version of my game engine.
-There are two game modes:
    * Main game: Navigate to 'Player' -> Any button
    * World Creator: Navigate to 'Extras' -> 'World Creator'
------------------------------------------------------------------------------------------------------------------
Main Game:
-Controls:
    Movement Keys:
        q,w,e,a,s,d Moves in hexagonal directions
    Mouse:
        Left click and drag to scroll map
    Actions:
        LShift hold: toggle face direct / press: toggle camera on player / while held hit space, fires invisible laser
    Navigation:
        Esc = Menu
    Debugging:
        F1 = initiates dialog, gives location
        F2 = opens stairs
        F3 = Saves world to json file
-------------------------------------------------------------------------------------------------------------------
World Creator:
    Controls:
        e = open/close inventory
        Lmouse = Draw, choose item from inventory
        LShift + Lmouse = scroll
        number bar = While over inventory, sets hotbar, otherwise, selects said item from hotbar
        f = recursive fill
        Esc = Back to title screen
===================================================================================================================
Main:
    -Debuging currently:
        -Loading screen not active.
        -Laser stops over vallies

    -To optimize:
        -Blank for now
        -Corner double blits (small)
        TODO: CLEAN UP/REFACTOR LITERALLY EVERYTHING

    -Adding soon:
        -scaling mini map
        -World generation update
        -animation
        -visible laser
        -drops: health pick ups
        -better game objectives
        -the kitchen sink

World Creator:
    -To debug:
        -hotbar elemtents set to none when set twice but image still shows

    -To Optimize:
        -Render distances: hitbox and blit

    -To add:
        -Saving/Loading
        -Naming
        -Elevation
        -Line snap
        -Track changes: Undo command
        -The kitchen sink