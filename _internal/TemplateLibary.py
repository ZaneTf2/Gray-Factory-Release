def find_robot_by_name(robot_name):
    """
    Ищет робота по имени и выводит имя блока, в котором он находится.
    
    :param robot_name: Имя робота для поиска.
    :return: Имя блока, если найдено; сообщение об ошибке в противном случае.
    """
    for block_name, robot_data in Template.items():
        if robot_data.get("Name") == robot_name:
            return block_name
    print(f"Robot with name '{robot_name}' not found in the library.")
    return None

Template = {
    "T_TFBot_Giant_Scout": {
        "Class": "Scout",
        "Name": "Giant Scout",
        "ClassIcon": "scout_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 1600.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "CharacterAttributes": {
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.7,
            "override footstep sound set": 5.0
        }
    },
    "T_TFBot_Giant_Soldier": {
        "Class": "Soldier",
        "Name": "Giant Soldier",
        "ClassIcon": "soldier_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3800.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "HoldFireUntilFullReload",
            "MiniBoss"
        ],
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0
        }
    },
    "T_TFBot_Giant_Pyro": {
        "Class": "Pyro",
        "Name": "Giant Pyro",
        "ClassIcon": "pyro_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3000.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.6,
            "airblast vulnerability multiplier": 0.6,
            "override footstep sound set": 6.0
        }
    },
    "T_TFBot_Giant_Demoman": {
        "Class": "Demoman",
        "Name": "Giant Rapid Fire Demoman",
        "ClassIcon": "demo_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3300.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "HoldFireUntilFullReload",
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_GRENADELAUNCHER",
            "faster reload rate": -0.4,
            "fire rate bonus": 0.75
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.5,
            "airblast vulnerability multiplier": 0.5,
            "override footstep sound set": 4.0
        }
    },
    "T_TFBot_Giant_Demo_RapidFire": {
        "Class": "Demoman",
        "Name": "Giant Rapid Fire Demoman",
        "ClassIcon": "demo_giant",
        "Health": 3000.0,
        "Skill": "Expert",
        "Scale": 1.75,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "HoldFireUntilFullReload",
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_GRENADELAUNCHER",
            "fire rate bonus": 0.5,
            "damage force reduction": 0.5
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "airblast vulnerability multiplier": 0.5,
            "override footstep sound set": 4.0
        }
    },
    "T_TFBot_Giant_Heavyweapons": {
        "Class": "Heavy",
        "Name": "Giant Heavy",
        "ClassIcon": "heavy_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "WeaponRestrictions": "PrimaryOnly",
        "MaxVisionRange": 1200.0,
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_MINIGUN",
            "damage bonus": 1.5
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Giant_Medic": {
        "Class": "Medic",
        "Name": "Giant Medic",
        "ClassIcon": "medic_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 4500.0,
        "Attributes": [
            "SpawnWithFullCharge",
            "MiniBoss"
        ],
        "Items": [
            "The Quick-Fix"
        ],
        "WeaponRestrictions": "SecondaryOnly",
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_SYRINGEGUN_MEDIC",
            "damage penalty": 0.1
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.6,
            "airblast vulnerability multiplier": 0.6,
            "heal rate bonus": 200.0
        }
    },
    "T_TFBot_Giant_Heavyweapons_Deflector": {
        "Class": "Heavy",
        "Name": "Giant Deflector Heavy",
        "ClassIcon": "heavy_deflector",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "Items": [
            "The U-clank-a",
            "Deflector"
        ],
        "WeaponRestrictions": "PrimaryOnly",
        "MaxVisionRange": 1200.0,
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "Deflector",
            "damage bonus": 1.5,
            "attack projectiles": 1.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Giant_Heavyweapons_Shotgun": {
        "Class": "Heavy",
        "Name": "Giant Shotgun Heavy",
        "ClassIcon": "heavy_shotgun",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "WeaponRestrictions": "SecondaryOnly",
        "MaxVisionRange": 1200.0,
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_SHOTGUN_HWG",
            "fire rate bonus": 2.5,
            "bullets per shot bonus": 10.0,
            "damage penalty": 0.5,
            "faster reload rate": 0.1
        },
        "CharacterAttributes": {
            "move speed bonus": 0.7,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "attack projectiles": 1.0,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Giant_Heavyweapons_BrassBeast": {
        "Class": "Heavy",
        "Name": "Giant Heavy",
        "ClassIcon": "heavy_giant",
        "Items": [
            "The Brass Beast"
        ],
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The Brass Beast",
            "damage bonus": 1.5
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Giant_Heavyweapons_Natascha": {
        "Class": "Heavy",
        "Name": "Giant Heavy",
        "ClassIcon": "heavy_giant",
        "Items": [
            "Natascha"
        ],
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "Natascha",
            "damage bonus": 1.5
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Giant_Heavyweapons_HealOnKill": {
        "Class": "Heavy",
        "Name": "Giant Heavy",
        "ClassIcon": "heavy_deflector_healonkill",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "WeaponRestrictions": "PrimaryOnly",
        "MaxVisionRange": 1200.0,
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "Deflector",
            "damage bonus": 1.2,
            "attack projectiles": 2.0,
            "heal on kill": 5000.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.35,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Chief_Heavyweapons_HealOnKill": {
        "Class": "Heavy",
        "Name": "Giant Heavy",
        "ClassIcon": "heavy_deflector_healonkill",
        "Skill": "Expert",
        "Items": [
            "The Tungsten Toque",
            "Deflector"
        ],
        "Health": 70000.0,
        "Scale": 1.8,
        "MaxVisionRange": 1600.0,
        "Attributes": [
            "UseBossHealthBar",
            "MiniBoss"
        ],
        "WeaponRestrictions": "PrimaryOnly",
        "ItemAttributes": {
            "ItemName": "Deflector",
            "damage bonus": 1.2,
            "attack projectiles": 2.0,
            "heal on kill": 8000.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.4,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.4,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.9,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Heavyweapons_Heater": {
        "Class": "Heavy",
        "Name": "Heavy Heater",
        "ClassIcon": "heavy_heater_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Items": [
            "The Huo Long Heatmaker"
        ],
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The Huo Long Heatmaker",
            "damage bonus": 1.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Giant_Scout_Fast": {
        "Class": "Scout",
        "Name": "Super Scout",
        "ClassIcon": "scout_giant_fast",
        "Skill": "Easy",
        "Scale": 1.75,
        "Items": [
            "Bonk Boy",
            "The Holy Mackerel"
        ],
        "Health": 1200.0,
        "WeaponRestrictions": "MeleeOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "CharacterAttributes": {
            "move speed bonus": 2.0,
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.7,
            "override footstep sound set": 5.0
        }
    },
    "T_TFBot_Giant_Scout_FAN": {
        "Class": "Scout",
        "Name": "Force-a-Nature Super Scout",
        "ClassIcon": "scout_fan_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Items": [
            "The Fed-Fightin' Fedora",
            "The Bolt Boy",
            "The Force-a-Nature"
        ],
        "Health": 1200.0,
        "Attributes": [
            "MiniBoss",
            "HoldFireUntilFullReload"
        ],
        "MaxVisionRange": 1200.0,
        "ItemAttributes": {
            "ItemName": "The Force-a-Nature",
            "bullets per shot bonus": 2.0,
            "fire rate bonus": 0.5,
            "faster reload rate": 1.7,
            "scattergun knockback mult": 6.0,
            "damage penalty": 0.35,
            "weapon spread bonus": 0.4
        },
        "CharacterAttributes": {
            "move speed bonus": 1.1,
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.7,
            "override footstep sound set": 5.0
        }
    },
    "T_TFBot_Giant_Scout_Jumping_Sandman": {
        "Class": "scout",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 1200.0,
        "ClassIcon": "scout_jumping_g",
        "Name": "Giant Jumping Sandman",
        "WeaponRestrictions": "MeleeOnly",
        "Items": [
            "The Sandman",
            "The Hanger-On Hood",
            "The Flight of the Monarch"
        ],
        "Attributes": [
            "MiniBoss",
            "AutoJump"
        ],
        "AutoJumpMin": 5.0,
        "AutoJumpMax": 5.0,
        "ItemAttributes": {
            "ItemName": "The Sandman",
            "damage bonus": 2.0,
            "effect bar recharge rate increased": 0.1
        },
        "CharacterAttributes": {
            "increased jump height": 2.0,
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.7,
            "override footstep sound set": 5.0,
            "head scale": 1.5
        }
    },
    "T_TFBot_Giant_DemoMan_PrinceTavish": {
        "Class": "Demoman",
        "ClassIcon": "demoknight_giant",
        "Name": "Giant Demoknight",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3300.0,
        "Items": [
            "Prince Tavish's Crown",
            "The Chargin' Targe",
            "The Eyelander",
            "Ali Baba's Wee Booties"
        ],
        "WeaponRestrictions": "MeleeOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The Eyelander",
            "critboost on kill": 3.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.5,
            "airblast vulnerability multiplier": 0.5,
            "override footstep sound set": 4.0
        }
    },
    "T_TFBot_Giant_Scout_Baseball": {
        "Class": "Scout",
        "Name": "League Scout",
        "ClassIcon": "scout_stun_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 1600.0,
        "Items": [
            "Batter's Helmet",
            "MNC Mascot Outfit",
            "The Sandman"
        ],
        "WeaponRestrictions": "MeleeOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The Sandman",
            "effect bar recharge rate increased": 0.1
        },
        "CharacterAttributes": {
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.7,
            "override footstep sound set": 5.0
        }
    },
    "T_TFBot_Giant_Scout_Baseball_Armored": {
        "Class": "Scout",
        "Name": "Armored Sandman Scout",
        "ClassIcon": "scout_stun_giant_armored",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3000.0,
        "Items": [
            "Batter's Helmet",
            "The Sandman"
        ],
        "WeaponRestrictions": "MeleeOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The Sandman",
            "effect bar recharge rate increased": 0.05
        },
        "CharacterAttributes": {
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.7,
            "override footstep sound set": 5.0,
            "move speed penalty": 0.75
        }
    },
    "T_TFBot_Giant_Scout_Bonk": {
        "Class": "Scout",
        "Name":  "Bonk Scout",
        "Skill": "Easy",
        "Scale": 1.75,
        "Items": [
            "Bonk! Atomic Punch",
            "Bonk Helm"
        ],
        "WeaponRestrictions": "MeleeOnly",
        "ClassIcon": "scout_bonk_giant",
        "Health": 1600.0,
        "Attributes": [
            "MiniBoss"
        ],
        "CharacterAttributes": {
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.7,
            "override footstep sound set": 5.0,
            "effect bar recharge rate increased": 0.55
        }
    },
    "T_TFBot_Giant_Soldier_Crit": {
        "Class": "Soldier",
        "Name": "Giant Charged Soldier",
        "ClassIcon": "soldier_crit",
        "Skill": "Normal",
        "Scale": 1.75,
        "Health": 3800.0,
        "Items": [
            "The Original"
        ],
        "Attributes": [
            "AlwaysCrit",
            "MiniBoss"
        ],
        "WeaponRestrictions": "PrimaryOnly",
        "ItemAttributes": {
            "ItemName": "The Original",
            "faster reload rate": 0.2,
            "fire rate bonus": 2.0,
            "Projectile speed increased": 0.5
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0
        }
    },
    "T_TFBot_Giant_Pyro_Flare_Spammer": {
        "Class": "Pyro",
        "Name": "Giant Flare Pyro",
        "ClassIcon": "pyro_flare_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3000.0,
        "Items": [
            "The detonator",
            "Old Guadalajara"
        ],
        "WeaponRestrictions": "SecondaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The detonator",
            "fire rate bonus": 0.3
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.6,
            "airblast vulnerability multiplier": 0.6,
            "override footstep sound set": 6.0
        }
    },
    "T_TFBot_Giant_Pyro_Flare_Spammer_ScorchShot": {
        "Class": "Pyro",
        "Name": "Giant Flare Pyro",
        "ClassIcon": "pyro_flare_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3000.0,
        "Items": [
            "The Scorch Shot"
        ],
        "WeaponRestrictions": "SecondaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The Scorch Shot",
            "fire rate bonus": 0.2,
            "damage causes airblast": 1.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.35,
            "damage force reduction": 0.6,
            "airblast vulnerability multiplier": 0.6,
            "override footstep sound set": 6.0
        }
    },
    "T_TFBot_Giant_Pyro_Pusher": {
        "Class": "Pyro",
        "ClassIcon": "pyro_airblast",
        "Name": "Giant Airblast Pyro",
        "Skill": "Expert",
        "Scale": 1.75,
        "Items": [
            "The Degreaser",
            "Traffic Cone"
        ],
        "Health": 3000.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "The Degreaser",
            "damage bonus": 0.05,
            "fire rate bonus": 1.0,
            "airblast pushback scale": 5.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.6,
            "airblast vulnerability multiplier": 0.6,
            "override footstep sound set": 6.0
        }
    },
    "T_TFBot_Giant_Boxing_Heavy": {
        "Class": "Heavy",
        "Name": "Super Heavyweight Champ",
        "ClassIcon": "heavy_champ_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 5000.0,
        "Items": [
            "the killing gloves of boxing",
            "Pugilist's Protector"
        ],
        "WeaponRestrictions": "MeleeOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "the killing gloves of boxing",
            "fire rate bonus": 0.6,
            "damage bonus": 1.2
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0
        }
    },
    "T_TFBot_Giant_Demo_Burst": {
        "Class": "Demoman",
        "Name": "Giant Burst Fire Demo",
        "ClassIcon": "demo_burst_giant",
        "Health": 3300.0,
        "Skill": "Expert",
        "Scale": 1.75,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss",
            "HoldFireUntilFullReload"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_GRENADELAUNCHER",
            "faster reload rate": 0.65,
            "fire rate bonus": 0.1,
            "clip size upgrade atomic": 7.0,
            "projectile spread angle penalty": 5.0,
            "Projectile speed increased": 1.1
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 4.0
        }
    },
    "T_TFBot_Giant_Demo_Spammer_Reload_Chief": {
        "Class": "Demoman",
        "Name": "Giant Rapid Fire Demo Chief",
        "ClassIcon": "demo_giant",
        "Health": 60000.0,
        "Scale": 1.9,
        "Skill": "Expert",
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar",
            "HoldFireUntilFullReload",
            "AlwaysCrit",
            "MiniBoss",
            "HoldFireUntilFullReload"
        ],
        "WeaponRestrictions": "PrimaryOnly",
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_GRENADELAUNCHER",
            "faster reload rate": 0.65,
            "fire rate bonus": 0.1,
            "clip size upgrade atomic": 7.0,
            "projectile spread angle penalty": 2.0,
            "Projectile speed increased": 1.1
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 4.0
        }
    },
    "T_TFBot_Giant_Soldier_Spammer": {
        "Class": "Soldier",
        "Name": "Giant Rapid Fire Soldier",
        "ClassIcon": "soldier_spammer",
        "Health": 3800.0,
        "Skill": "Expert",
        "Scale": 1.75,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_ROCKETLAUNCHER",
            "faster reload rate": -0.8,
            "fire rate bonus": 0.5
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "Projectile speed increased": 0.65
        }
    },
    "T_TFBot_Giant_Soldier_Spammer_Reload": {
        "Class": "Soldier",
        "Name": "Giant Burst Fire Soldier",
        "ClassIcon": "soldier_burstfire",
        "Health": 3800.0,
        "Skill": "Expert",
        "Scale": 1.75,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss",
            "HoldFireUntilFullReload"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_ROCKETLAUNCHER",
            "move speed bonus": 0.5,
            "faster reload rate": 0.6,
            "fire rate bonus": 0.1,
            "clip size upgrade atomic": 5.0,
            "Projectile speed increased": 0.65
        },
        "CharacterAttributes": {
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0
        }
    },
    "T_TFBot_Giant_Soldier_Extended_Buff_Banner": {
        "Class": "Soldier",
        "Name": "Giant Buff Banner Soldier",
        "ClassIcon": "soldier_buff_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3800.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "HoldFireUntilFullReload",
            "MiniBoss",
            "SpawnWithFullCharge"
        ],
        "Items": [
            "The Buff Banner"
        ],
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "increase buff duration": 9.0
        }
    },
    "T_TFBot_Giant_Soldier_Extended_Concheror": {
        "Class": "Soldier",
        "Name": "Giant Concheror Soldier",
        "ClassIcon": "soldier_conch_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3800.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "HoldFireUntilFullReload",
            "MiniBoss",
            "SpawnWithFullCharge"
        ],
        "Items": [
            "The Concheror"
        ],
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "increase buff duration": 9.0
        }
    },
    "T_TFBot_Giant_Soldier_Extended_Battalion": {
        "Class": "Soldier",
        "Name": "Giant Battalion Soldier ",
        "ClassIcon": "soldier_backup_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 3800.0,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "HoldFireUntilFullReload",
            "MiniBoss",
            "SpawnWithFullCharge"
        ],
        "Items": [
            "The Battalion's Backup"
        ],
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "increase buff duration": 9.0
        }
    },
    "T_TFBot_Giant_Soldier_RocketShotgun": {
        "Class": "Soldier",
        "ClassIcon": "soldier_blackbox_giant",
        "Name": "Giant Black Box Soldier",
        "Health": 4200.0,
        "Items": [
            "The Black Box"
        ],
        "Skill": "Expert",
        "Scale": 1.75,
        "Attributes": [
            "MiniBoss",
            "HoldFireUntilFullReload"
        ],
        "WeaponRestrictions": "PrimaryOnly",
        "ItemAttributes": {
            "ItemName": "The Black Box",
            "damage bonus": 0.45,
            "fire rate bonus": 0.001,
            "clip size upgrade atomic": 0.0,
            "faster reload rate": 1.6,
            "blast radius increased": 1.25,
            "projectile spread angle penalty": 4.0,
            "heal on hit for rapidfire": 1000.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "Projectile speed increased": 0.9
        }
    },
    "T_TFBot_Giant_Medic_Regen": {
        "Class": "Medic",
        "Name": "Giant Medic",
        "ClassIcon": "medic_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 4500.0,
        "Items": [
            "The Quick-Fix",
            "The Surgeon's Stahlhelm"
        ],
        "Attributes": [
            "MiniBoss"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_SYRINGEGUN_MEDIC",
            "damage penalty": 0.1
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.6,
            "airblast vulnerability multiplier": 0.6,
            "heal rate bonus": 200.0,
            "health regen": 40.0
        }
    },
    "T_TFBot_Soldier_BurstFire": {
        "Class": "Soldier",
        "Name": "Giant Burst Fire Soldier",
        "ClassIcon": "soldier_burstfire",
        "Health": 4200.0,
        "Skill": "Expert",
        "Scale": 1.75,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss",
            "HoldFireUntilFullReload",
            "AlwaysCrit"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_ROCKETLAUNCHER",
            "damage bonus": 2.0,
            "faster reload rate": 0.4,
            "fire rate bonus": 0.2,
            "clip size upgrade atomic": 5.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "Projectile speed increased": 0.9
        }
    },
    "T_TFBot_Giant_Soldier_SlowBarrage": {
        "Class": "Soldier",
        "Name": "Colonel Barrage",
        "ClassIcon": "soldier_barrage",
        "Health": 4000.0,
        "Tag": [
            "bot_giant"
        ],
        "Skill": "Expert",
        "Scale": 1.75,
        "WeaponRestrictions": "PrimaryOnly",
        "Attributes": [
            "MiniBoss",
            "HoldFireUntilFullReload"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_ROCKETLAUNCHER",
            "clip size upgrade atomic": 26.0,
            "faster reload rate": 0.22,
            "fire rate bonus": 0.2,
            "projectile spread angle penalty": 5.0
        },
        "CharacterAttributes": {
            "health regen": 40.0,
            "move speed bonus": 0.5,
            "damage bonus": 1.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "Projectile speed increased": 0.4
        }
    },
    "T_TFBot_Chief_Gauntlet": {
        "Class": "Heavy",
        "Skill": "Expert",
        "WeaponRestrictions": "MeleeOnly",
        "Name": "Captain Punch",
        "ClassIcon": "heavy_chief",
        "Health": 60000.0,
        "Scale": 1.9,
        "Items": [
            "War Head",
            "Fists of Steel"
        ],
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar"
        ],
        "ItemAttributes": {
            "ItemName": "Fists of Steel",
            "fire rate bonus": 0.6,
            "damage bonus": 5.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.4,
            "health regen": 250.0,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    },
    "T_TFBot_Chief_Tavish": {
        "Class": "Demoman",
        "Skill": "Expert",
        "WeaponRestrictions": "MeleeOnly",
        "Name": "Chief Tavish",
        "ClassIcon": "demoknight_giant",
        "Health": 55000.0,
        "Scale": 1.9,
        "Items": [
            "Prince Tavish's Crown",
            "The Chargin' Targe",
            "The Eyelander",
            "Ali Baba's Wee Booties"
        ],
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar"
        ],
        "ItemAttributes": {
            "ItemName": "The Eyelander",
            "damage bonus": 5.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.4,
            "health regen": 500.0,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    },
    "T_TFBot_Chief_Pyro": {
        "Class": "Pyro",
        "Skill": "Expert",
        "WeaponRestrictions": "PrimaryOnly",
        "Name": "Chief Pyro",
        "ClassIcon": "pyro_giant",
        "Health": 55000.0,
        "Scale": 1.9,
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_FLAMETHROWER",
            "airblast pushback scale": 2.0,
            "damage bonus": 5.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.4,
            "health regen": 500.0,
            "damage force reduction": 0.3,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 2.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    },
    "T_TFBot_Chief_Soldier": {
        "Class": "Soldier",
        "Skill": "Expert",
        "WeaponRestrictions": "PrimaryOnly",
        "Name": "Sergeant Crits",
        "ClassIcon": "soldier_sergeant_crits",
        "Health": 60000.0,
        "Scale": 1.9,
        "Items": [
            "Tyrant's Helm"
        ],
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar",
            "HoldFireUntilFullReload",
            "AlwaysCrit"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_ROCKETLAUNCHER",
            "damage bonus": 1.5,
            "faster reload rate": 0.6,
            "fire rate bonus": 0.2,
            "clip size upgrade atomic": 7.0,
            "Projectile speed increased": 1.3
        },
        "CharacterAttributes": {
            "health regen": 250.0,
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    },
    "T_TFBot_Chief_Soldier_SlowCrit": {
        "Class": "Soldier",
        "Skill": "Expert",
        "WeaponRestrictions": "PrimaryOnly",
        "Name": "Major Crits",
        "Items": [
            "Full Metal Drill Hat"
        ],
        "ClassIcon": "soldier_major_crits",
        "Health": 60000.0,
        "Scale": 1.9,
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar",
            "HoldFireUntilFullReload",
            "AlwaysCrit"
        ],
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_ROCKETLAUNCHER",
            "clip size upgrade atomic": 26.0,
            "faster reload rate": 0.4,
            "fire rate bonus": 0.2,
            "projectile spread angle penalty": 5.0,
            "Projectile speed increased": 0.4
        },
        "CharacterAttributes": {
            "health regen": 250.0,
            "move speed bonus": 0.5,
            "damage bonus": 1.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    },
    "T_TFBot_Giant_Soldier_RocketPush": {
        "Class": "Soldier",
        "Skill": "Expert",
        "Scale": 1.75,
        "WeaponRestrictions": "PrimaryOnly",
        "Items": [
            "The Liberty Launcher"
        ],
        "ClassIcon": "soldier_libertylauncher_giant",
        "Attributes": [
            "MiniBoss",
            "HoldFireUntilFullReload"
        ],
        "Name": "Giant Blast Soldier",
        "Health": 3800.0,
        "ItemAttributes": {
            "ItemName": "The Liberty Launcher",
            "damage causes airblast": 1.0,
            "damage bonus": 0.75,
            "fire rate bonus": 0.25,
            "clip size upgrade atomic": 5.0,
            "faster reload rate": 0.2,
            "Blast radius decreased": 1.2,
            "projectile spread angle penalty": 4.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "override footstep sound set": 3.0,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "airblast vertical vulnerability multiplier": 0.1
        }
    },
    "T_TFBot_Chief_Soldier_RocketPush": {
        "Class": "Soldier",
        "Skill": "Expert",
        "WeaponRestrictions": "PrimaryOnly",
        "Items": [
            "The Liberty Launcher"
        ],
        "ClassIcon": "soldier_libertylauncher",
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar",
            "HoldFireUntilFullReload"
        ],
        "Health": 60000.0,
        "Scale": 1.8,
        "Name": "Chief Blast Soldier",
        "ItemAttributes": {
            "ItemName": "The Liberty Launcher",
            "damage causes airblast": 1.0,
            "damage bonus": 1.0,
            "fire rate bonus": 0.25,
            "clip size upgrade atomic": 5.0,
            "faster reload rate": 0.4,
            "Blast radius decreased": 1.2,
            "projectile spread angle penalty": 4.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "override footstep sound set": 3.0,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.15
        }
    },
    "T_TFBot_Chief_Soldier_Atomic": {
        "Class": "Soldier",
        "Skill": "Expert",
        "WeaponRestrictions": "PrimaryOnly",
        "Name": "Major Crits",
        "Items": [
            "The Team Captain",
            "The Black Box",
            "Fancy Dress Uniform",
            "The Gunboats"
        ],
        "ClassIcon": "soldier_sergeant_crits",
        "Health": 40000.0,
        "Scale": 1.9,
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar",
            "HoldFireUntilFullReload",
            "AlwaysCrit"
        ],
        "ItemAttributes": {
            "ItemName": "The Black Box",
            "damage bonus": 5.0,
            "damage causes airblast": 1.0,
            "faster reload rate": 3.0,
            "fire rate bonus": 2.0,
            "projectile spread angle penalty": 1.0,
            "use large smoke explosion": 1.0,
            "blast radius increased": 2.0,
            "Projectile speed increased": 1.0
        },
        "CharacterAttributes": {
            "health regen": 1.0,
            "move speed bonus": 0.4,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "airblast vertical vulnerability multiplier": 0.1
        }
    },
    "T_TFBot_Chief_Demo_Atomic": {
        "Class": "Demoman",
        "Name": "Sir Nukesalot",
        "ClassIcon": "demo_giant",
        "Health": 50000.0,
        "Scale": 1.9,
        "Skill": "Expert",
        "WeaponRestrictions": "PrimaryOnly",
        "Items": [
            "The Loose Cannon"
        ],
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar",
            "HoldFireUntilFullReload",
            "AlwaysFireWeapon",
            "AlwaysCrit"
        ],
        "ItemAttributes": {
            "ItemName": "The Loose Cannon",
            "grenade launcher mortar mode": 0.0,
            "faster reload rate": 1.8,
            "fire rate bonus": 2.0,
            "clip size penalty": 0.5,
            "Projectile speed increased": 0.8,
            "projectile spread angle penalty": 5.0,
            "damage bonus": 7.0,
            "damage causes airblast": 1.0,
            "blast radius increased": 1.2,
            "use large smoke explosion": 1.0
        },
        "CharacterAttributes": {
            "move speed bonus": 0.35,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 4.0
        }
    },
    "T_TFBot_Giant_Major_League": {
        "Class": "Scout",
        "Name": "Major League",
        "ClassIcon": "scout_stun_giant",
        "Skill": "Expert",
        "Scale": 1.75,
        "Health": 10000.0,
        "Items": [
            "Genuine Cockfighter",
            "The Boston Boom-Bringer",
            "Summer Shades",
            "The Sandman"
        ],
        "WeaponRestrictions": "MeleeOnly",
        "Attributes": [
            "MiniBoss",
            "UseBossHealthBar"
        ],
        "ItemAttributes": {
            "ItemName": "The Sandman",
            "effect bar recharge rate increased": 0.001
        },
        "CharacterAttributes": {
            "move speed bonus": 8.0,
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 3.0,
            "override footstep sound set": 5.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    },
    "T_TFBot_Giant_Metalbeard": {
        "Class": "Demoman",
        "Name": "Major Bomber",
        "ClassIcon": "demo_bomber",
        "Skill": "Normal",
        "Scale": 1.75,
        "Health": 40000.0,
        "Items": [
            "Prince Tavish's Crown"
        ],
        "Attributes": [
            "AlwaysCrit",
            "MiniBoss",
            "UseBossHealthBar",
            "HoldFireUntilFullReload"
        ],
        "WeaponRestrictions": "PrimaryOnly",
        "ItemAttributes": {
            "ItemName": "TF_WEAPON_GRENADELAUNCHER",
            "fire rate bonus": 0.2,
            "faster reload rate": 0.3,
            "clip size penalty": 3.0,
            "Projectile speed increased": 1.5
        },
        "CharacterAttributes": {
            "health regen": 200.0,
            "move speed bonus": 0.32,
            "damage force reduction": 0.7,
            "airblast vulnerability multiplier": 0.3,
            "override footstep sound set": 4.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    },
    "T_TFBot_Chief_Soldier_Extended_Concheror": {
        "Class": "Soldier",
        "Name": "Chief Concheror Soldier",
        "ClassIcon": "soldier_conch_giant",
        "Attributes": [
            "UseBossHealthBar",
            "HoldFireUntilFullReload",
            "MiniBoss",
            "SpawnWithFullCharge"
        ],
        "Skill": "Expert",
        "Health": 50000.0,
        "Scale": 1.8,
        "WeaponRestrictions": "PrimaryOnly",
        "Items": [
            "The Concheror"
        ],
        "CharacterAttributes": {
            "move speed bonus": 0.5,
            "damage force reduction": 0.4,
            "airblast vulnerability multiplier": 0.4,
            "override footstep sound set": 3.0,
            "increase buff duration": 9.0,
            "airblast vertical vulnerability multiplier": 0.1,
            "rage giving scale": 0.1
        }
    }
}