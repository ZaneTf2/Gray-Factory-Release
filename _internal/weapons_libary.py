def find_weapon_info(weapon_name):
    """
    Поиск информации об оружии в библиотеке Weapon_Libary.
    
    :param weapon_name: Название оружия для поиска.
    :return: Словарь с информацией о классе, типе оружия и его названии, или сообщение об отсутствии.
    """
    for class_name, weapon_types in Weapon_Libary.items():
        for weapon_type, weapons in weapon_types.items():
            for weapon in weapons.values():
                if weapon["Name"].lower() == weapon_name.lower():
                    return {
                        "Class": class_name,
                        "Type": weapon_type,
                        "Name": weapon["Name"]
                    }
    return None

Weapon_Libary = {
    "Scout": {
        "Primary": {
            "Scattergun": {
                "Name": "Scattergun",
                "Id": "tf_weapon_scattergun",
                "Icon": "Backpack_Scattergun"
            },
            "Force-A-Nature": {
                "Name": "Force-A-Nature",
                "Id": "tf_weapon_scattergun",
                "Icon": "Backpack_Force-A-Nature"
            },
            "The Shortstop": {
                "Name": "The Shortstop",
                "Id": "tf_weapon_handgun_scout_primary",
                "Icon": "Backpack_Shortstop"
            },
            "The Soda Popper": {
                "Name": "The Soda Popper",
                "Id": "tf_weapon_soda_popper",
                "Icon": "Backpack_Soda_Popper"
            },
            "Festive Scattergun": {
                "Name": "Festive Scattergun",
                "Id": "tf_weapon_scattergun",
                "Icon": "scattergun_xmas"
            },
            "Baby Face's Blaster": {
                "Name": "Baby Face's Blaster",
                "Id": "tf_weapon_pep_brawler_blaster",
                "Icon": "Babyfaceblaster"
            },
            "Silver Botkiller Scattergun Mk.I": {
                "Name": "Silver Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Gold Botkiller Scattergun Mk.I": {
                "Name": "Gold Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Rust Botkiller Scattergun Mk.I": {
                "Name": "Rust Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Blood Botkiller Scattergun Mk.I": {
                "Name": "Blood Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Carbonado Botkiller Scattergun Mk.I": {
                "Name": "Carbonado Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Diamond Botkiller Scattergun Mk.I": {
                "Name": "Diamond Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Silver Botkiller Scattergun Mk.II": {
                "Name": "Silver Botkiller Scattergun Mk.II",
                "Id": "tf_weapon_scattergun",
                "Icon": "fob_e_scattergun_engi"
            },
            "Gold Botkiller Scattergun Mk.II": {
                "Name": "Gold Botkiller Scattergun Mk.II",
                "Id": "tf_weapon_scattergun",
                "Icon": "fob_e_scattergun_gold"
            },
            "Festive Force-A-Nature": {
                "Name": "Festive Force-A-Nature",
                "Id": "tf_weapon_scattergun",
                "Icon": "xms_double_barrel"
            },
        },
        "Secondary": {
            "Pistol": {
                "Name": "Pistol",
                "Id": "tf_weapon_pistol",
                "Icon": "pistol"
            },
            "Bonk! Atomic Punch": {
                "Name": "Bonk! Atomic Punch",
                "Id": "tf_weapon_lunchbox_drink",
                "Icon": "Backpack_Bonk!_Atomic_Punch"
            },
            "Crit-a-Cola": {
                "Name": "Crit-a-Cola",
                "Id": "tf_weapon_lunchbox_drink",
                "Icon": "Backpack_Crit-a-Cola"
            },
            "Mad Milk": {
                "Name": "Mad Milk",
                "Id": "tf_weapon_jar_milk",
                "Icon": "Backpack_Mad_Milk"
            },
            "Lugermorph": {
                "Name": "Lugermorph",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_Lugermorph"
            },
            "The Winger": {
                "Name": "The Winger",
                "Id": "tf_weapon_handgun_scout_secondary",
                "Icon": "Backpack_Winger"
            },
            "Pretty Boy's Pocket Pistol": {
                "Name": "Pretty Boy's Pocket Pistol",
                "Id": "tf_weapon_handgun_scout_secondary",
                "Icon": "Backpack_Pretty_Pocket"
            },
            "The Flying Guillotine": {
                "Name": "The Flying Guillotine",
                "Id": "tf_weapon_cleaver",
                "Icon": "Backpack_Flying_Guillotine"
            },
            "Mutated Milk": {
                "Name": "Mutated Milk",
                "Id": "tf_weapon_jar_milk",
                "Icon": "Backpack_Mutated_Milk"
            },
            "Festive Bonk!": {
                "Name": "Festive Bonk!",
                "Id": "tf_weapon_lunchbox_drink",
                "Icon": "xms_energy_drink"
            },
            "The C.A.P.P.E.R.": {
                "Name": "The C.A.P.P.E.R.",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_C.A.P.P.E.R"
            }
        },
        "Melee": {
            "Bat": {
                "Name": "Bat",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Bat"
            },
            "The Sandman": {
                "Name": "The Sandman",
                "Id": "tf_weapon_bat_wood",
                "Icon": "Backpack_Sandman"
            },
            "The Holy Mackerel": {
                "Name": "The Holy Mackerel",
                "Id": "tf_weapon_bat_fish",
                "Icon": "holymackerel"
            },
            "Frying Pan": {
                "Name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "The Candy Cane": {
                "Name": "The Candy Cane",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Candy_Cane"
            },
            "The Boston Basher": {
                "Name": "The Boston Basher",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Boston_Basher"
            },
            "Sun-on-a-Stick": {
                "Name": "Sun-on-a-Stick",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Sun-on-a-Stick"
            },
            "The Fan O'War": {
                "Name": "The Fan O'War",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Fan_War"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Atomizer": {
                "Name": "The Atomizer",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Atomizer"
            },
            "Three-Rune Blade": {
                "Name": "Three-Rune Blade",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Three-Rune_Blade"
            },
            "The Conscientious Objector": {
                "Name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "Unarmed Combat": {
                "Name": "Unarmed Combat",
                "Id": "tf_weapon_bat_fish",
                "Icon": "Backpack_Unarmed_Combat"
            },
            "The Wrap Assassin": {
                "Name": "The Wrap Assassin",
                "Id": "tf_weapon_bat_giftwrap",
                "Icon": "Backpack_Wrap_Assassin"
            },
            "Festive Bat": {
                "Name": "Festive Bat",
                "Id": "tf_weapon_bat",
                "Icon": "bat_xmas"
            },
            "The Freedom Staff": {
                "Name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "Name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "Name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "8mm_camera"
            },
            "Festive Holy Mackerel": {
                "Name": "Festive Holy Mackerel",
                "Id": "tf_weapon_bat_fish",
                "Icon": "holymackerel_xmas"
            },
            "The Ham Shank": {
                "Name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "Name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Batsaber": {
                "Name": "Batsaber",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Batsaber"
            },
        }
    },
    "Soldier": {
        "Primary": {
            "Rocket Launcher": {
                "Name": "Rocket Launcher",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "rocketlauncher_sold"
            },
            "The Direct Hit": {
                "Name": "The Direct Hit",
                "Id": "tf_weapon_rocketlauncher_directhit",
                "Icon": "directhit"
            },
            "The Black Box": {
                "Name": "The Black Box",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "blackbox"
            },
            "Rocket Jumper": {
                "Name": "Rocket Jumper",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "rocketjumper"
            },
            "The Liberty Launcher": {
                "Name": "The Liberty Launcher",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "liberty_launcher"
            },
            "The Cow Mangler 5000": {
                "Name": "The Cow Mangler 5000",
                "Id": "tf_weapon_particle_cannon",
                "Icon": "drg_cowmangler"
            },
            "The Original": {
                "Name": "The Original",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "Backpack_Original"
            },
            "Festive Rocket Launcher": {
                "Name": "Festive Rocket Launcher",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "rocketlauncher_xmas"
            },
            "The Beggar's Bazooka": {
                "Name": "The Beggar's Bazooka",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "Bazooka"
            },
            "Silver Botkiller Rocket Launcher Mk.I": {
                "Name": "Silver Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Gold Botkiller Rocket Launcher Mk.I": {
                "Name": "Gold Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Rust Botkiller Rocket Launcher Mk.I": {
                "Name": "Rust Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Blood Botkiller Rocket Launcher Mk.I": {
                "Name": "Blood Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Carbonado Botkiller Rocket Launcher Mk.I": {
                "Name": "Carbonado Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Diamond Botkiller Rocket Launcher Mk.I": {
                "Name": "Diamond Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Silver Botkiller Rocket Launcher Mk.II": {
                "Name": "Silver Botkiller Rocket Launcher Mk.II",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "fob_e_rocketlauncher"
            },
            "Gold Botkiller Rocket Launcher Mk.II": {
                "Name": "Gold Botkiller Rocket Launcher Mk.II",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "fob_e_rocketlauncher_gold"
            },
            "Festive Black Box": {
                "Name": "Festive Black Box",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "blackbox_xmas"
            },
            "The Air Strike": {
                "Name": "The Air Strike",
                "Id": "tf_weapon_rocketlauncher_airstrike",
                "Icon": "None"
            },
        },
        "Secondary": {
            "Shotgun": {
                "Name": "Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun"
            },
            "The Buff Banner": {
                "Name": "The Buff Banner",
                "Id": "tf_weapon_buff_item",
                "Icon": "buffpack"
            },
            "Gunboats": {
                "Name": "Gunboats",
                "Id": "tf_wearable",
                "Icon": "rocketboots_soldier"
            },
            "The Battalion's Backup": {
                "Name": "The Battalion's Backup",
                "Id": "tf_weapon_buff_item",
                "Icon": "None"
            },
            "The Concheror": {
                "Name": "The Concheror",
                "Id": "tf_weapon_buff_item",
                "Icon": "None"
            },
            "The Reserve Shooter": {
                "Name": "The Reserve Shooter",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "The Righteous Bison": {
                "Name": "The Righteous Bison",
                "Id": "tf_weapon_raygun",
                "Icon": "drg_righteousbison"
            },
            "The Mantreads": {
                "Name": "The Mantreads",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "Festive Buff Banner": {
                "Name": "Festive Buff Banner",
                "Id": "tf_weapon_buff_item",
                "Icon": "buffpack_xmas"
            },
            "The B.A.S.E. Jumper": {
                "Name": "The B.A.S.E. Jumper",
                "Id": "tf_weapon_parachute",
                "Icon": "c_paratrooper_pack"
            },
            "Festive Shotgun": {
                "Name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "Name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
        },
        "Melee": {
            "Shovel": {
                "Name": "Shovel",
                "Id": "tf_weapon_shovel",
                "Icon": "shovel"
            },
            "The Equalizer": {
                "Name": "The Equalizer",
                "Id": "tf_weapon_shovel",
                "Icon": "pickaxe_s2"
            },
            "The Pain Train": {
                "Name": "The Pain Train",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "Frying Pan": {
                "Name": "Frying Pan",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "The Half-Zatoichi": {
                "Name": "The Half-Zatoichi",
                "Id": "tf_weapon_katana",
                "Icon": "None"
            },
            "The Market Gardener": {
                "Name": "The Market Gardener",
                "Id": "tf_weapon_shovel",
                "Icon": "gardener"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Disciplinary Action": {
                "Name": "The Disciplinary Action",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "The Conscientious Objector": {
                "Name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Escape Plan": {
                "Name": "The Escape Plan",
                "Id": "tf_weapon_shovel",
                "Icon": "pickaxe"
            },
            "The Freedom Staff": {
                "Name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "Name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "Name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "Name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Crossing Guard": {
                "Name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
        }
    },
    "Pyro": {
        "Primary": {
            "Flame Thrower": {
                "Name": "Flame Thrower",
                "Id": "tf_weapon_flamethrower",
                "Icon": "Backpack_Flame_Thrower"
            },
            "The Backburner": {
                "Name": "The Backburner",
                "Id": "tf_weapon_flamethrower",
                "Icon": "backburner"
            },
            "The Degreaser": {
                "Name": "The Degreaser",
                "Id": "tf_weapon_flamethrower",
                "Icon": "degreaser"
            },
            "The Phlogistinator": {
                "Name": "The Phlogistinator",
                "Id": "tf_weapon_flamethrower",
                "Icon": "drg_phlogistinator"
            },
            "Festive Flame Thrower": {
                "Name": "Festive Flame Thrower",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_xmas"
            },
            "The Rainblower": {
                "Name": "The Rainblower",
                "Id": "tf_weapon_flamethrower",
                "Icon": "rainblower"
            },
            "Silver Botkiller Flame Thrower Mk.I": {
                "Name": "Silver Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "fob_h_flamethrower"
            },
            "Gold Botkiller Flame Thrower Mk.I": {
                "Name": "Gold Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "None"
            },
            "Rust Botkiller Flame Thrower Mk.I": {
                "Name": "Rust Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_rust"
            },
            "Blood Botkiller Flame Thrower Mk.I": {
                "Name": "Blood Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_blood"
            },
            "Carbonado Botkiller Flame Thrower Mk.I": {
                "Name": "Carbonado Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_rust"
            },
            "Diamond Botkiller Flame Thrower Mk.I": {
                "Name": "Diamond Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_diamond"
            },
            "Silver Botkiller Flame Thrower Mk.II": {
                "Name": "Silver Botkiller Flame Thrower Mk.II",
                "Id": "tf_weapon_flamethrower",
                "Icon": "fob_e_flamethrower"
            },
            "Gold Botkiller Flame Thrower Mk.II": {
                "Name": "Gold Botkiller Flame Thrower Mk.II",
                "Id": "tf_weapon_flamethrower",
                "Icon": "fob_e_flamethrower_gold"
            },
            "Festive Backburner": {
                "Name": "Festive Backburner",
                "Id": "tf_weapon_flamethrower",
                "Icon": "backburner_xmas"
            },
            "Dragon's Fury": {
                "Name": "Dragon's Fury",
                "Id": "tf_weapon_rocketlauncher_fireball",
                "Icon": "flameball"
            },
        },
        "Secondary": {
            "Shotgun": {
                "Name": "Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun"
            },
            "The Flare Gun": {
                "Name": "The Flare Gun",
                "Id": "tf_weapon_flaregun",
                "Icon": "flaregun_pyro"
            },
            "The Detonator": {
                "Name": "The Detonator",
                "Id": "tf_weapon_flaregun",
                "Icon": "detonator"
            },
            "The Reserve Shooter": {
                "Name": "The Reserve Shooter",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "The Manmelter": {
                "Name": "The Manmelter",
                "Id": "tf_weapon_flaregun_revenge",
                "Icon": "drg_manmelter"
            },
            "The Scorch Shot": {
                "Name": "The Scorch Shot",
                "Id": "tf_weapon_flaregun",
                "Icon": "None"
            },
            "Festive Flare Gun": {
                "Name": "Festive Flare Gun",
                "Id": "tf_weapon_flaregun",
                "Icon": "flaregun"
            },
            "Festive Shotgun": {
                "Name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "Name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "Thermal Thruster": {
                "Name": "Thermal Thruster",
                "Id": "tf_weapon_rocketpack",
                "Icon": "rocketpack"
            },
            "Gas Passer": {
                "Name": "Gas Passer",
                "Id": "tf_weapon_jar_gas",
                "Icon": "gascan"
            },
        },
        "Melee": {
            "Fire Axe": {
                "Name": "Fire Axe",
                "Id": "tf_weapon_fireaxe",
                "Icon": "fireaxe_pyro"
            },
            "The Axtinguisher": {
                "Name": "The Axtinguisher",
                "Id": "tf_weapon_fireaxe",
                "Icon": "axtinguisher_pyro"
            },
            "Homewrecker": {
                "Name": "Homewrecker",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Powerjack": {
                "Name": "The Powerjack",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "Frying Pan": {
                "Name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "The Back Scratcher": {
                "Name": "The Back Scratcher",
                "Id": "tf_weapon_fireaxe",
                "Icon": "back_scratcher"
            },
            "Sharpened Volcano Fragment": {
                "Name": "Sharpened Volcano Fragment",
                "Id": "tf_weapon_fireaxe",
                "Icon": "fire_axe"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Postal Pummeler": {
                "Name": "The Postal Pummeler",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Maul": {
                "Name": "The Maul",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Conscientious Objector": {
                "Name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Third Degree": {
                "Name": "The Third Degree",
                "Id": "tf_weapon_fireaxe",
                "Icon": "drg_thirddegree"
            },
            "The Lollichop": {
                "Name": "The Lollichop",
                "Id": "tf_weapon_fireaxe",
                "Icon": "lollichop"
            },
            "Neon Annihilator": {
                "Name": "Neon Annihilator",
                "Id": "tf_weapon_breakable_sign",
                "Icon": "None"
            },
            "The Freedom Staff": {
                "Name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "Name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "Name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Festive Axtinguisher": {
                "Name": "The Festive Axtinguisher",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Ham Shank": {
                "Name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Crossing Guard": {
                "Name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Hot Hand": {
                "Name": "Hot Hand",
                "Id": "tf_weapon_slap",
                "Icon": "slapping_glove"
            },
        }
    },
    "Demoman": {
        "Primary": {
            "Grenade Launcher": {
                "Name": "Grenade Launcher",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "grenadelauncher"
            },
            "The Loch-n-Load": {
                "Name": "The Loch-n-Load",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "lochnload"
            },
            "Ali Baba's Wee Booties": {
                "Name": "Ali Baba's Wee Booties",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "The Bootlegger": {
                "Name": "The Bootlegger",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "The Loose Cannon": {
                "Name": "The Loose Cannon",
                "Id": "tf_weapon_cannon",
                "Icon": "loose_cannon"
            },
            "Festive Grenade Launcher": {
                "Name": "Festive Grenade Launcher",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "grenadelauncher_xmas"
            },
            "The B.A.S.E. Jumper": {
                "Name": "The B.A.S.E. Jumper",
                "Id": "tf_weapon_parachute",
                "Icon": "None"
            },
            "The Iron Bomber": {
                "Name": "The Iron Bomber",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "None"
            },
        },
        "Secondary": {
            "Stickybomb Launcher": {
                "Name": "Stickybomb Launcher",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "stickybomb_launcher"
            },
            "The Scottish Resistance": {
                "Name": "The Scottish Resistance",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "stickybomb_defender"
            },
            "The Chargin' Targe": {
                "Name": "The Chargin' Targe",
                "Id": "tf_wearable_demoshield",
                "Icon": "targe"
            },
            "Sticky Jumper": {
                "Name": "Sticky Jumper",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "sticky_jumper"
            },
            "The Splendid Screen": {
                "Name": "The Splendid Screen",
                "Id": "tf_wearable_demoshield",
                "Icon": "None"
            },
            "Festive Stickybomb Launcher": {
                "Name": "Festive Stickybomb Launcher",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "stickybomb_launcher_xmas"
            },
            "Silver Botkiller Stickybomb Launcher Mk.I": {
                "Name": "Silver Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Gold Botkiller Stickybomb Launcher Mk.I": {
                "Name": "Gold Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Rust Botkiller Stickybomb Launcher Mk.I": {
                "Name": "Rust Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Blood Botkiller Stickybomb Launcher Mk.I": {
                "Name": "Blood Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Carbonado Botkiller Stickybomb Launcher Mk.I": {
                "Name": "Carbonado Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Diamond Botkiller Stickybomb Launcher Mk.I": {
                "Name": "Diamond Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Silver Botkiller Stickybomb Launcher Mk.II": {
                "Name": "Silver Botkiller Stickybomb Launcher Mk.II",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "botkillere_stickybomb"
            },
            "Gold Botkiller Stickybomb Launcher Mk.II": {
                "Name": "Gold Botkiller Stickybomb Launcher Mk.II",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "botkillere_stickybomb_gold"
            },
            "The Tide Turner": {
                "Name": "The Tide Turner",
                "Id": "tf_wearable_demoshield",
                "Icon": "None"
            },
            "Festive Targe": {
                "Name": "Festive Targe",
                "Id": "tf_wearable_demoshield",
                "Icon": "targe_xmas"
            },
            "The Quickiebomb Launcher": {
                "Name": "The Quickiebomb Launcher",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
        },
        "Melee": {
            "Bottle": {
                "Name": "Bottle",
                "Id": "tf_weapon_bottle",
                "Icon": "bottle"
            },
            "The Eyelander": {
                "Name": "The Eyelander",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "The Pain Train": {
                "Name": "The Pain Train",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "The Scotsman's Skullcutter": {
                "Name": "The Scotsman's Skullcutter",
                "Id": "tf_weapon_sword",
                "Icon": "battleaxe"
            },
            "Frying Pan": {
                "Name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "Horseless Headless Horsemann's Headtaker": {
                "Name": "Horseless Headless Horsemann's Headtaker",
                "Id": "tf_weapon_sword",
                "Icon": "headtaker"
            },
            "Ullapool Caber": {
                "Name": "Ullapool Caber",
                "Id": "tf_weapon_stickbomb",
                "Icon": "caber"
            },
            "The Claidheamh Mòr": {
                "Name": "The Claidheamh Mòr",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "The Half-Zatoichi": {
                "Name": "The Half-Zatoichi",
                "Id": "tf_weapon_katana",
                "Icon": "None"
            },
            "The Persian Persuader": {
                "Name": "The Persian Persuader",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Conscientious Objector": {
                "Name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "Nessie's Nine Iron": {
                "Name": "Nessie's Nine Iron",
                "Id": "tf_weapon_sword",
                "Icon": "golfclub"
            },
            "The Scottish Handshake": {
                "Name": "The Scottish Handshake",
                "Id": "tf_weapon_bottle",
                "Icon": "None"
            },
            "The Freedom Staff": {
                "Name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "Name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "Name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "Name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "Festive Eyelander": {
                "Name": "Festive Eyelander",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Crossing Guard": {
                "Name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
        }
    },
    "Heavy": {
        "Primary": {
            "Minigun": {
                "Name": "Minigun",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Natascha": {
                "Name": "Natascha",
                "Id": "tf_weapon_minigun",
                "Icon": "natasha"
            },
            "Iron Curtain": {
                "Name": "Iron Curtain",
                "Id": "tf_weapon_minigun",
                "Icon": "curtain"
            },
            "The Brass Beast": {
                "Name": "The Brass Beast",
                "Id": "tf_weapon_minigun",
                "Icon": "gatling_gun"
            },
            "Tomislav": {
                "Name": "Tomislav",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Festive Minigun": {
                "Name": "Festive Minigun",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun_xmas"
            },
            "Silver Botkiller Minigun Mk.I": {
                "Name": "Silver Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Gold Botkiller Minigun Mk.I": {
                "Name": "Gold Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "The Huo-Long Heater": {
                "Name": "The Huo-Long Heater",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Deflector": {
                "Name": "Deflector",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Rust Botkiller Minigun Mk.I": {
                "Name": "Rust Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Blood Botkiller Minigun Mk.I": {
                "Name": "Blood Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Carbonado Botkiller Minigun Mk.I": {
                "Name": "Carbonado Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Diamond Botkiller Minigun Mk.I": {
                "Name": "Diamond Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "None"
            },
            "Silver Botkiller Minigun Mk.II": {
                "Name": "Silver Botkiller Minigun Mk.II",
                "Id": "tf_weapon_minigun",
                "Icon": "fob_e_minigun"
            },
            "Gold Botkiller Minigun Mk.II": {
                "Name": "Gold Botkiller Minigun Mk.II",
                "Id": "tf_weapon_minigun",
                "Icon": "fob_e_minigun_gold"
            },
        },
        "Secondary": {
            "Shotgun": {
                "Name": "Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun"
            },
            "Sandvich": {
                "Name": "Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "robo_sandwich"
            },
            "The Dalokohs Bar": {
                "Name": "The Dalokohs Bar",
                "Id": "tf_weapon_lunchbox",
                "Icon": "None"
            },
            "The Buffalo Steak Sandvich": {
                "Name": "The Buffalo Steak Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "None"
            },
            "The Family Business": {
                "Name": "The Family Business",
                "Id": "tf_weapon_shotgun_hwg",
                "Icon": "None"
            },
            "Fishcake": {
                "Name": "Fishcake",
                "Id": "tf_weapon_lunchbox",
                "Icon": "None"
            },
            "Robo-Sandvich": {
                "Name": "Robo-Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "robo_sandwich"
            },
            "Festive Sandvich": {
                "Name": "Festive Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "sandwich_xmas"
            },
            "Festive Shotgun": {
                "Name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "Name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "Second Banana": {
                "Name": "Second Banana",
                "Id": "tf_weapon_lunchbox",
                "Icon": "banana"
            },
        },
        "Melee": {
            "Fists": {
                "Name": "Fists",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "The Killing Gloves of Boxing": {
                "Name": "The Killing Gloves of Boxing",
                "Id": "tf_weapon_fists",
                "Icon": "boxing_gloves"
            },
            "Gloves of Running Urgently": {
                "Name": "Gloves of Running Urgently",
                "Id": "tf_weapon_fists",
                "Icon": "boxing_gloves_urgency"
            },
            "Frying Pan": {
                "Name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "Warrior's Spirit": {
                "Name": "Warrior's Spirit",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "Fists of Steel": {
                "Name": "Fists of Steel",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Eviction Notice": {
                "Name": "The Eviction Notice",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "The Conscientious Objector": {
                "Name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "Apoco-Fists": {
                "Name": "Apoco-Fists",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "The Holiday Punch": {
                "Name": "The Holiday Punch",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "The Freedom Staff": {
                "Name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "Name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "Name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "Name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "Festive Gloves of Running Urgently (G.R.U.)": {
                "Name": "Festive Gloves of Running Urgently (G.R.U.)",
                "Id": "tf_weapon_fists",
                "Icon": "boxing_gloves_xmas"
            },
            "The Bread Bite": {
                "Name": "The Bread Bite",
                "Id": "tf_weapon_fists",
                "Icon": "breadmonster_gloves"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Crossing Guard": {
                "Name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
        }
    },
    "Engineer": {
        "Primary": {
            "Shotgun": {
                "Name": "Shotgun",
                "Id": "tf_weapon_shotgun_primary",
                "Icon": "shotgun"
            },
            "Shotgun (Renamed/Str": {
                "Name": "Shotgun (Renamed/Str",
                "Id": "ange)tf_weapon_shotgun",
                "Icon": "None"
            },
            "The Frontier Justice": {
                "Name": "The Frontier Justice",
                "Id": "tf_weapon_sentry_revenge",
                "Icon": "frontierjustice"
            },
            "The Widowmaker": {
                "Name": "The Widowmaker",
                "Id": "tf_weapon_shotgun_primary",
                "Icon": "None"
            },
            "The Pomson 6000": {
                "Name": "The Pomson 6000",
                "Id": "tf_weapon_drg_pomson",
                "Icon": "drg_pomson"
            },
            "The Rescue Ranger": {
                "Name": "The Rescue Ranger",
                "Id": "tf_weapon_shotgun_building_rescue",
                "Icon": "None"
            },
            "Festive Frontier Jus": {
                "Name": "Festive Frontier Jus",
                "Id": "ticetf_weapon_sentry_revenge",
                "Icon": "frontierjustice_xmas"
            },
            "Festive Shotgun": {
                "Name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "Name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
        },
        "Secondary": {
            "Pistol": {
                "Name": "Pistol",
                "Id": "tf_weapon_pistol",
                "Icon": "pistol"
            },
            "The Wrangler": {
                "Name": "The Wrangler",
                "Id": "tf_weapon_laser_pointer",
                "Icon": "wrangler"
            },
            "Lugermorph": {
                "Name": "Lugermorph",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_Lugermorph"
            },
            "The Short Circuit": {
                "Name": "The Short Circuit",
                "Id": "tf_weapon_mechanical_arm",
                "Icon": "None"
            },
            "Festive Wrangler": {
                "Name": "Festive Wrangler",
                "Id": "tf_weapon_laser_pointer",
                "Icon": "wrangler_xmas"
            },
            "Red Rock Roscoe": {
                "Name": "Red Rock Roscoe",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Homemade Heater": {
                "Name": "Homemade Heater",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Hickory Holepuncher": {
                "Name": "Hickory Holepuncher",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Local Hero": {
                "Name": "Local Hero",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Black Dahlia": {
                "Name": "Black Dahlia",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Sandstone Special": {
                "Name": "Sandstone Special",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Macabre Web": {
                "Name": "Macabre Web",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Nutcracker": {
                "Name": "Nutcracker",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Blue Mew": {
                "Name": "Blue Mew",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Brain Candy": {
                "Name": "Brain Candy",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Shot to Hell": {
                "Name": "Shot to Hell",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Dressed To Kill": {
                "Name": "Dressed To Kill",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Blitzkrieg": {
                "Name": "Blitzkrieg",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "The C.A.P.P.E.R.": {
                "Name": "The C.A.P.P.E.R.",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_C.A.P.P.E.R"
            },
            "The Gigar Counter": {
                "Name": "The Gigar Counter",
                "Id": "tf_weapon_laser_pointer",
                "Icon": "None"
            }
        },
        "Melee": {
            "Wrench": {
                "Name": "Wrench",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench"
            },
            "The Gunslinger": {
                "Name": "The Gunslinger",
                "Id": "tf_weapon_robot_arm",
                "Icon": "gunslinger"
            },
            "The Southern Hospitality": {
                "Name": "The Southern Hospitality",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Golden Wrench": {
                "Name": "Golden Wrench",
                "Id": "tf_weapon_wrench",
                "Icon": "botkiller_wrench_gold"
            },
            "The Jag": {
                "Name": "The Jag",
                "Id": "tf_weapon_wrench",
                "Icon": "jag"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Eureka Effect": {
                "Name": "The Eureka Effect",
                "Id": "tf_weapon_wrench",
                "Icon": "drg_wrenchmotron"
            },
            "Festive Wrench": {
                "Name": "Festive Wrench",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_xmas"
            },
            "Silver Botkiller Wrench Mk.I": {
                "Name": "Silver Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "fob_h_wrench"
            },
            "Gold Botkiller Wrench Mk.I": {
                "Name": "Gold Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "fob_h_wrench_gold"
            },
            "Rust Botkiller Wrench Mk.I": {
                "Name": "Rust Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_rust"
            },
            "Blood Botkiller Wrench Mk.I": {
                "Name": "Blood Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_blood"
            },
            "Carbonado Botkiller Wrench Mk.I": {
                "Name": "Carbonado Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Diamond Botkiller Wrench Mk.I": {
                "Name": "Diamond Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_diamond"
            },
            "Diamond Black Botkiller Wrench Mk.I": {
                "Name": "Diamond Black Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_diamond_black"
            },
            "Silver Botkiller Wrench Mk.II": {
                "Name": "Silver Botkiller Wrench Mk.II",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Gold Botkiller Wrench Mk.II": {
                "Name": "Gold Botkiller Wrench Mk.II",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "None"
            },
        },
        "PDA": {
            "Construction PDA": {
                "Name": "Construction PDA",
                "Id": "tf_weapon_pda_engineer_build",
                "Icon": "builder"
            },
            "Destruction PDA": {
                "Name": "Destruction PDA",
                "Id": "tf_weapon_pda_engineer_destroy",
                "Icon": "pda_engineer"
            }
        }
    },
    "Medic": {
        "Primary": {
            "Syringe Gun": {
                "Name": "Syringe Gun",
                "Id": "tf_weapon_syringegun_medic",
                "Icon": "syringegun"
            },
            "The Blutsauger": {
                "Name": "The Blutsauger",
                "Id": "tf_weapon_syringegun_medic",
                "Icon": "bloodsiger"
            },
            "Crusader's Crossbow": {
                "Name": "Crusader's Crossbow",
                "Id": "tf_weapon_crossbow",
                "Icon": "None"
            },
            "The Overdose": {
                "Name": "The Overdose",
                "Id": "tf_weapon_syringegun_medic",
                "Icon": "overdose"
            },
            "Festive Crusader's Crossbow": {
                "Name": "Festive Crusader's Crossbow",
                "Id": "tf_weapon_crossbow",
                "Icon": "None"
            }
        },
        "Secondary": {
            "Medi Gun": {
                "Name": "Medi Gun",
                "Id": "tf_weapon_medigun",
                "Icon": "w_medigun"
            },
            "The Kritzkrieg": {
                "Name": "The Kritzkrieg",
                "Id": "tf_weapon_medigun",
                "Icon": "medigun_overhealer"
            },
            "The Quick-Fix": {
                "Name": "The Quick-Fix",
                "Id": "tf_weapon_medigun",
                "Icon": "proto_medigun"
            },
            "Festive Medi Gun": {
                "Name": "Festive Medi Gun",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Silver Botkiller Medi Gun Mk.I": {
                "Name": "Silver Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Gold Botkiller Medi Gun Mk.I": {
                "Name": "Gold Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Rust Botkiller Medi Gun Mk.I": {
                "Name": "Rust Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Blood Botkiller Medi Gun Mk.I": {
                "Name": "Blood Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Carbonado Botkiller Medi Gun Mk.I": {
                "Name": "Carbonado Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Diamond Botkiller Medi Gun Mk.I": {
                "Name": "Diamond Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Silver Botkiller Medi Gun Mk.II": {
                "Name": "Silver Botkiller Medi Gun Mk.II",
                "Id": "tf_weapon_medigun",
                "Icon": "fob_h_medigun"
            },
            "Gold Botkiller Medi Gun Mk.II": {
                "Name": "Gold Botkiller Medi Gun Mk.II",
                "Id": "tf_weapon_medigun",
                "Icon": "fob_h_medigun_gold"
            },
            "The Vaccinator": {
                "Name": "The Vaccinator",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
        },
        "Melee": {
            "Bonesaw": {
                "Name": "Bonesaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "bonesaw"
            },
            "The Ubersaw": {
                "Name": "The Ubersaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "ubersaw"
            },
            "The Vita-Saw": {
                "Name": "The Vita-Saw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "uberneedle"
            },
            "Frying Pan": {
                "Name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "Amputator": {
                "Name": "Amputator",
                "Id": "tf_weapon_bonesaw",
                "Icon": "amputator"
            },
            "The Solemn Vow": {
                "Name": "The Solemn Vow",
                "Id": "tf_weapon_bonesaw",
                "Icon": "hippocrates_bust"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Conscientious Objector": {
                "Name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Freedom Staff": {
                "Name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "Name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "Name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "Festive Ubersaw": {
                "Name": "Festive Ubersaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "ubersaw_xmas"
            },
            "The Ham Shank": {
                "Name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Crossing Guard": {
                "Name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Festive Bonesaw": {
                "Name": "Festive Bonesaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "bonesaw_xmas"
            },
        }
    },
    "Sniper": {
        "Primary": {
            "Rifle": {
                "Name": "Rifle",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "fob_e_sniperrifle"
            },
            "The Huntsman": {
                "Name": "The Huntsman",
                "Id": "tf_weapon_compound_bow",
                "Icon": "bow"
            },
            "The Sydney Sleeper": {
                "Name": "The Sydney Sleeper",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "The Bazaar Bargain": {
                "Name": "The Bazaar Bargain",
                "Id": "tf_weapon_sniperrifle_decap",
                "Icon": "bazaar_sniper"
            },
            "The Machina": {
                "Name": "The Machina",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Festive Sniper Rifle": {
                "Name": "Festive Sniper Rifle",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "sniperrifle_xmas"
            },
            "The Hitman's Heatmaker": {
                "Name": "The Hitman's Heatmaker",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Silver Botkiller Sniper Rifle Mk.I": {
                "Name": "Silver Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Gold Botkiller Sniper Rifle Mk.I": {
                "Name": "Gold Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "The AWPer Hand": {
                "Name": "The AWPer Hand",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "awp"
            },
            "Rust Botkiller Sniper Rifle Mk.I": {
                "Name": "Rust Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Blood Botkiller Sniper Rifle Mk.I": {
                "Name": "Blood Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Carbonado Botkiller Sniper Rifle Mk.I": {
                "Name": "Carbonado Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Diamond Botkiller Sniper Rifle Mk.I": {
                "Name": "Diamond Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Silver Botkiller Sniper Rifle Mk.II": {
                "Name": "Silver Botkiller Sniper Rifle Mk.II",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "fob_e_sniperrifle"
            },
            "Gold Botkiller Sniper Rifle Mk.II": {
                "Name": "Gold Botkiller Sniper Rifle Mk.II",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "fob_e_sniperrifle_gold"
            },
            "Festive Huntsman": {
                "Name": "Festive Huntsman",
                "Id": "tf_weapon_compound_bow",
                "Icon": "bow_xmas"
            },
            "The Fortified Compound": {
                "Name": "The Fortified Compound",
                "Id": "tf_weapon_compound_bow",
                "Icon": "None"
            },
            "The Classic": {
                "Name": "The Classic",
                "Id": "tf_weapon_sniperrifle_classic",
                "Icon": "tfc_sniperrifle"
            },
            "Shooting Star": {
                "Name": "Shooting Star",
                "Id": "tf_weapon_sniperrifle ",
                "Icon": "None"
            }
        },
        "Secondary": {
            "SMG": {
                "Name": "SMG",
                "Id": "tf_weapon_smg",
                "Icon": "smg"
            },
            "The Razorback": {
                "Name": "The Razorback",
                "Id": "tf_wearable_razorback",
                "Icon": "None"
            },
            "Jarate": {
                "Name": "Jarate",
                "Id": "tf_weapon_jar",
                "Icon": "urinejar"
            },
            "Darwin's Danger Shield": {
                "Name": "Darwin's Danger Shield",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "Cozy Camper": {
                "Name": "Cozy Camper",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "The Cleaner's Carbine": {
                "Name": "The Cleaner's Carbine",
                "Id": "tf_weapon_charged_smg",
                "Icon": "None"
            },
            "Festive Jarate": {
                "Name": "Festive Jarate",
                "Id": "tf_weapon_jar",
                "Icon": "xms_urinejar"
            },
            "The Self-Aware Beauty Mark": {
                "Name": "The Self-Aware Beauty Mark",
                "Id": "tf_weapon_jar",
                "Icon": "breadmonster"
            },
            "Festive SMG": {
                "Name": "Festive SMG",
                "Id": "tf_weapon_smg",
                "Icon": "smg_xmas"
            },
        },
        "Melee": {
            "Kukri": {
                "Name": "Kukri",
                "Id": "tf_weapon_club",
                "Icon": "machete"
            },
            "The Tribalman's Shiv": {
                "Name": "The Tribalman's Shiv",
                "Id": "tf_weapon_club",
                "Icon": "wood_machete"
            },
            "The Bushwacka": {
                "Name": "The Bushwacka",
                "Id": "tf_weapon_club",
                "Icon": "None"
            },
            "Frying Pan": {
                "Name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "The Shahanshah": {
                "Name": "The Shahanshah",
                "Id": "tf_weapon_club",
                "Icon": "None"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Conscientious Objector": {
                "Name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Freedom Staff": {
                "Name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "Name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "Name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "Name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "Name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Crossing Guard": {
                "Name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Prinny Machete": {
                "Name": "Prinny Machete",
                "Id": "saxxy",
                "Icon": "None"
            }
        }
    },
    "Spy": {
        "Primary": {
            "Revolver": {
                "Name": "Revolver",
                "Id": "tf_weapon_revolver",
                "Icon": "revolver"
            },
            "The Ambassador": {
                "Name": "The Ambassador",
                "Id": "tf_weapon_revolver",
                "Icon": "ambassador_opt"
            },
            "Big Kill": {
                "Name": "Big Kill",
                "Id": "tf_weapon_revolver",
                "Icon": "None"
            },
            "L'Etranger": {
                "Name": "L'Etranger",
                "Id": "tf_weapon_revolver",
                "Icon": "letranger"
            },
            "The Enforcer": {
                "Name": "The Enforcer",
                "Id": "tf_weapon_revolver",
                "Icon": "None"
            },
            "The Diamondback": {
                "Name": "The Diamondback",
                "Id": "tf_weapon_revolver",
                "Icon": "None"
            },
            "Festive Ambassador": {
                "Name": "Festive Ambassador",
                "Id": "tf_weapon_revolver",
                "Icon": "ambassador_xmas"
            },
            "Festive Revolver": {
                "Name": "Festive Revolver",
                "Id": "tf_weapon_revolver",
                "Icon": "revolver_xmas"
            },
        },
        "Secondary": {
            "Sapper": {
                "Name": "Sapper",
                "Id": "tf_weapon_builder",
                "Icon": "sapper"
            },
            "The Red-Tape Recorder": {
                "Name": "The Red-Tape Recorder",
                "Id": "tf_weapon_sapper",
                "Icon": "None"
            },
            "The Ap-Sap (Genuine)": {
                "Name": "The Ap-Sap (Genuine)",
                "Id": "tf_weapon_sapper",
                "Icon": "p2rec"
            },
            "Festive Sapper": {
                "Name": "Festive Sapper",
                "Id": "tf_weapon_sapper",
                "Icon": "sapper_xmas"
            },
            "The Snack Attack": {
                "Name": "The Snack Attack",
                "Id": "tf_weapon_sapper",
                "Icon": "breadmonster_sap"
            }
        },
        "Melee": {
            "Knife": {
                "Name": "Knife",
                "Id": "tf_weapon_knife",
                "Icon": "knife"
            },
            "Your Eternal Reward": {
                "Name": "Your Eternal Reward",
                "Id": "tf_weapon_knife",
                "Icon": "eternal_reward"
            },
            "Conniver's Kunai": {
                "Name": "Conniver's Kunai",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Saxxy": {
                "Name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Big Earner": {
                "Name": "The Big Earner",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "The Wanga Prick": {
                "Name": "The Wanga Prick",
                "Id": "tf_weapon_knife",
                "Icon": "voodoo_pin"
            },
            "The Sharp Dresser": {
                "Name": "The Sharp Dresser",
                "Id": "tf_weapon_knife",
                "Icon": "acr_hookblade"
            },
            "The Spy-cicle": {
                "Name": "The Spy-cicle",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Festive Knife": {
                "Name": "Festive Knife",
                "Id": "tf_weapon_knife",
                "Icon": "knife_xmas"
            },
            "The Black Rose": {
                "Name": "The Black Rose",
                "Id": "tf_weapon_knife",
                "Icon": "ava_roseknife_v"
            },
            "Silver Botkiller Knife Mk.I": {
                "Name": "Silver Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Gold Botkiller Knife Mk.I": {
                "Name": "Gold Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Rust Botkiller Knife Mk.I": {
                "Name": "Rust Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_rust"
            },
            "Blood Botkiller Knife Mk.I": {
                "Name": "Blood Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_blood"
            },
            "Carbonado Botkiller Knife Mk.I": {
                "Name": "Carbonado Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Diamond Botkiller Knife Mk.I": {
                "Name": "Diamond Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_diamond"
            },
            "Diamond Black Botkiller Knife Mk.I": {
                "Name": "Diamond Black Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_diamond_black"
            },
            "Silver Botkiller Knife Mk.II": {
                "Name": "Silver Botkiller Knife Mk.II",
                "Id": "tf_weapon_knife",
                "Icon": "knife_botkiller_mk2"
            },
            "Gold Botkiller Knife Mk.II": {
                "Name": "Gold Botkiller Knife Mk.II",
                "Id": "tf_weapon_knife",
                "Icon": "knife_botkiller_mk2_gold"
            },
            "Gold Frying Pan": {
                "Name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
        },
        "Clock": {
            "Invis Watch": {
                "Name": "Invis Watch",
                "Id": "tf_weapon_invis",
                "Icon": "spy_watch"
            },
            "The Dead Ringer": {
                "Name": "The Dead Ringer",
                "Id": "tf_weapon_invis",
                "Icon": "pocket_watch"
            },
            "The Cloak and Dagger": {
                "Name": "The Cloak and Dagger",
                "Id": "tf_weapon_invis",
                "Icon": "leather_watch"
            },
            "Enthusiast's Timepiece": {
                "Name": "Enthusiast's Timepiece",
                "Id": "tf_weapon_invis",
                "Icon": "ttg_watch"
            },
            "The Quackenbirdt": {
                "Name": "The Quackenbirdt",
                "Id": "tf_weapon_invis ",
                "Icon": "None"
            }
        }
    }
}