#!/usr/bin/env python
import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
        name = "Lux Strike",options = {"build_exe":{
                "packages":["pygame","time","math","sys","random","pygame.font","numpy","os"],
                "include_files":['galaxy-bt','HUD','Music','Player','Portraits','Saved_Worlds','SFX','Tiles',
                'Title','Dialog','Enemies','Drops']
                }
        }
        ,executables = executables,version = '1.0.0'
)
