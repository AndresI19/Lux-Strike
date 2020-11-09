#Inventory
#Tiles
Tiles = {
    "Water":{
        "ID":0,
        "Path":"Tiles/Water/",
        "Inventory":False,
        "World Creator":True,
        "Icon":True,
        "Isometric":{
            "Hexagon":{"Path":"H","Total":8,"Choice":False},
            "Left":{"Path":"L","Total":1},
            "Center":{"Path":"C","Total":1},
            "Right":{"Path":"R","Total":1}
        }
    },
    "Grass":{
        "ID":1,
        "Path":"Tiles/Grass/",
        "Inventory":False,
        "World Creator":True,
        "Icon":True,
        "Isometric":{
            "Hexagon":{"Path":"H","Total":4,"Choice":[.55,.35,.05,.05]},
            "Left":{"Path":"L","Total":1},
            "Center":{"Path":"C","Total":1},
            "Right":{"Path":"R","Total":1}
        }
    },
    "Beach":{
        "ID":2,
        "Path":"Tiles/Beach/",
        "Inventory":False,
        "World Creator":True,
        "Icon":True,
        "Isometric":{
            "Hexagon":{"Path":"H","Total":4,"Choice":[.75,.10,.10,.05]},
            "Left":{"Path":"L","Total":1},
            "Center":{"Path":"C","Total":1},
            "Right":{"Path":"R","Total":1}
        }
    },
    "Mountain":{
        "ID":3,
        "Path":"Tiles/Mountain/",
        "Inventory":False,
        "World Creator":True,
        "Icon":True,
        "Isometric":{
            "Hexagon":{"Path":"H","Total":1,"Choice":False},
            "Left":{"Path":"L","Total":1},
            "Center":{"Path":"C","Total":1},
            "Right":{"Path":"R","Total":1}
        }
    },
    "Brick":{
        "ID":100,
        "Path":"Tiles/Brick/",
        "Inventory":False,
        "World Creator":True,
        "Icon":True,
        "Isometric":{
            "Hexagon":{"Path":"H","Total":1,"Choice":False},
            "Left":{"Path":"L","Total":1},
            "Center":{"Path":"C","Total":1},
            "Right":{"Path":"R","Total":1}
        }
    },
    "Stairs":{
        "ID":101,
        "Path":"Tiles/Brick/",
        "Inventory":False,
        "World Creator":True,
        "Icon":True,
        "Isometric":{
            "Hexagon":{"Path":"HS","Total":8,"Choice":False},
            "Left":{"Path":"L","Total":1},
            "Center":{"Path":"C","Total":1},
            "Right":{"Path":"R","Total":1}
        }
    },
    "Door":{
        "ID":102,
        "Path":"Tiles/Brick/",
        "Inventory":False,
        "World Creator":True,
        "Icon":True,
        "Isometric":{
            "Hexagon":{"Path":"H","Total":8,"Choice":False},
            "Left":{"Path":"L","Total":1},
            "Center":{"Path":"CD","Total":1},
            "Right":{"Path":"R","Total":1}
        }
    },
}

#Enemies
Enemies = {
    "Swanzai":{
        "ID":0,
        "Path":"Enemies/Swanzai",
        "Inventory":False,
        "World Creator":False,
        "Isometric":True
    },
    "Nest":{
        "ID":1,
        "Path":"Enemies/Swanzai_Nest",
        "Inventory":False,
        "World Creator":False,
        "Isometric":True
    },
    "Rabbo":{
        "ID":2,
        "Path":"Enemies/Rabbo",
        "Inventory":False,
        "World Creator":False,
        "Isometric":True
    }
}

#Drops
Drops = {
    "Money":{
        "ID":0,
        "Isometric":"Drops/Money",
        "Inventory":False,
        "World Creator":False,
    },
    "Key":{
        "ID":1,
        "Isometric":"Drops/Key",
        "Inventory":False,
        "World Creator":False,
    }
}