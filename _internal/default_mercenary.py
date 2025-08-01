from Icons_Archive import icons 
import weapons_libary
from resources import resources
from pathlib import Path

Mercenary = {
    "Scout" : { 
        "Name" : "Scout",
        "Class" : 0,
        "Class Name" : "Scout",
        "Health" : 125,
        "Icon" : icons["leaderboard_class_scout"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
        
        "Tag" : [],
        "Cosmetics" : [],
        
        "Primary Weapon" : weapons_libary.Weapon_Libary["Scout"]["Primary"]["Scattergun"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Scout"]["Secondary"]["Pistol"],
        "Melee" : weapons_libary.Weapon_Libary["Scout"]["Melee"]["Bat"],
        
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {},
    },
    "Soldier" : {
        "Name" : "Soldier",
        "Class" : 1,
        "Class Name" : "Soldier",
        "Health" : 200,
        "Icon" : icons["leaderboard_class_soldier"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
        
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Soldier"]["Primary"]["Rocket Launcher"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Soldier"]["Secondary"]["Shotgun"],
        "Melee" : weapons_libary.Weapon_Libary["Soldier"]["Melee"]["Shovel"],
    
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {},
    },
    "Pyro" : {
        "Name" : "Pyro",
        "Class" : 2,
        "Class Name" : "Pyro",
        "Health" : 175,
        "Icon" : icons["leaderboard_class_pyro"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Pyro"]["Primary"]["Flame Thrower"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Pyro"]["Secondary"]["Shotgun"],
        "Melee" : weapons_libary.Weapon_Libary["Pyro"]["Melee"]["Fire Axe"],
    
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {},
    },
    "Demoman" : {
        "Name" : "Demo",
        "Class" : 3,
        "Class Name" : "Demoman",
        "Health" : 175,
        "Icon" : icons["leaderboard_class_demo"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Demoman"]["Primary"]["Grenade Launcher"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Demoman"]["Secondary"]["Stickybomb Launcher"],
        "Melee" : weapons_libary.Weapon_Libary["Demoman"]["Melee"]["Bottle"],
    
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {},
    },
    "Heavy" : {
        "Name" : "Heavy",
        "Class Name" : "Heavy",
        "Class" : 4,
        "Health" : 300,
        "Icon" : icons["leaderboard_class_heavy"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Heavy"]["Primary"]["Festive Minigun"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Heavy"]["Secondary"]["Shotgun"],
        "Melee" : weapons_libary.Weapon_Libary["Heavy"]["Melee"]["The Killing Gloves of Boxing"],
    
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {}
        #{
        #    "obj" : Path(f"{resources()}/model/bot_heavy.mdl"), 
        #    "texture": Path(f"{resources()}/model/bot_heavy_blue.vtf"),
        #    "mtl": Path(f"{resources()}/model/bot_heavy.mtl"),
        #}
    },
    "Engineer" : {
        "Name" : "Engineer",
        "Class" : 5,
        "Class Name" : "Engineer",
        "Health" : 275,
        "Icon" : icons["leaderboard_class_engineer"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Engineer"]["Primary"]["Shotgun"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Engineer"]["Secondary"]["Pistol"],
        "Melee" : weapons_libary.Weapon_Libary["Engineer"]["Melee"]["Wrench"],
    
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {},
    },
    "Medic" : {
        "Name" : "Medic",
        "Class" : 6,
        "Class Name" : "Medic",
        "Health" : 150,
        "Icon" : icons["leaderboard_class_medic"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Medic"]["Primary"]["Syringe Gun"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Medic"]["Secondary"]["Medi Gun"],
        "Melee" : weapons_libary.Weapon_Libary["Medic"]["Melee"]["Bonesaw"],
    
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {}
        #{
        #    "obj" : Path(f"{resources()}/resources/Models/Medic/bot_medic.obj"), 
        #    "texture": Path(f"{resources()}/resources/Models/Medic/bot_medic_blue.png"),
        #    "mtl": Path(f"{resources()}/resources/Models/Medic/bot_medic.mtl"),
        #}
    },
    "Sniper" : {
        "Name" : "Sniper",
        "Class" : 7,
        "Class Name" : "Sniper",
        "Health" : 125,
        "Icon" : icons["leaderboard_class_sniper"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Sniper"]["Primary"]["Rifle"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Sniper"]["Secondary"]["SMG"],
        "Melee" : weapons_libary.Weapon_Libary["Sniper"]["Melee"]["Kukri"],
    
        "Tag_Attributes": [],
        "Custom Parametrs" :  str,
        "Model" : {},
    },
    "Spy" : {
        "Name" : "Spy",
        "Class" : 8,
        "Class Name" : "Spy",
        "Health" : 125,
        "Icon" : icons["leaderboard_class_spy"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
    
        "Tag" : [],
        "Cosmetics" : [],
    
        "Primary Weapon" : weapons_libary.Weapon_Libary["Spy"]["Primary"]["Revolver"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Spy"]["Secondary"]["Sapper"],
        "Melee" : weapons_libary.Weapon_Libary["Spy"]["Melee"]["Knife"],
        
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {},
    },
    
    "Tank" : { 
        "Name" : "Tank",
        "Class" : 9,
        "Class Name" : "Tank",
        "Health" : 20000,
        "Icon" : icons["leaderboard_class_tank"],
        "Scale" : 1,
        "MaxVision" : -1,
        "AutoJump Min" : -1,
        "AutoJump Max" : -1,
        "Skill" : 0,
        "Weapon Restriction" : 0,
        "Behavior" : 0,
        
        "Tag" : [],
        "Cosmetics" : [],
        
        "Primary Weapon" : weapons_libary.Weapon_Libary["Scout"]["Primary"]["Scattergun"],
        "Secondary Weapons" : weapons_libary.Weapon_Libary["Scout"]["Secondary"]["Pistol"],
        "Melee" : weapons_libary.Weapon_Libary["Scout"]["Melee"]["Bat"],
        
        "Tag_Attributes": [],
        "Custom Parametrs" :  """""",
        "Model" : {},
    },
}
