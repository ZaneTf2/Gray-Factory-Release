def find_weapon_info(weapon_name):
    """
    Поиск информации об оружии в библиотеке Weapon_Libary.
    
    :param weapon_name: Название оружия для поиска.
    :return: Словарь с информацией о классе, типе оружия и его названии, или сообщение об отсутствии.
    """
    for class_name, weapon_types in Weapon_Libary.items():
        for weapon_type, weapons in weapon_types.items():
            for weapon in weapons.values():
                if weapon["name"].lower() == weapon_name.lower():
                    return {
                        "Class": class_name,
                        "Type": weapon_type,
                        "name": weapon["name"]
                    }
    return None

Weapon_Libary = {
    "Scout": {
        "Primary": {
            "Scattergun": {
                "name": "Scattergun",
                "Id": "tf_weapon_scattergun",
                "Icon": "Backpack_Scattergun"
            },
            "Force-A-Nature": {
                "name": "Force-A-Nature",
                "Id": "tf_weapon_scattergun",
                "Icon": "Backpack_Force-A-Nature"
            },
            "The Shortstop": {
                "name": "The Shortstop",
                "Id": "tf_weapon_handgun_scout_primary",
                "Icon": "Backpack_Shortstop"
            },
            "The Soda Popper": {
                "name": "The Soda Popper",
                "Id": "tf_weapon_soda_popper",
                "Icon": "Backpack_Soda_Popper"
            },
            "Festive Scattergun": {
                "name": "Festive Scattergun",
                "Id": "tf_weapon_scattergun",
                "Icon": "scattergun_xmas"
            },
            "Baby Face's Blaster": {
                "name": "Baby Face's Blaster",
                "Id": "tf_weapon_pep_brawler_blaster",
                "Icon": "Babyfaceblaster"
            },
            "Silver Botkiller Scattergun Mk.I": {
                "name": "Silver Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Gold Botkiller Scattergun Mk.I": {
                "name": "Gold Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Rust Botkiller Scattergun Mk.I": {
                "name": "Rust Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Blood Botkiller Scattergun Mk.I": {
                "name": "Blood Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Carbonado Botkiller Scattergun Mk.I": {
                "name": "Carbonado Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Diamond Botkiller Scattergun Mk.I": {
                "name": "Diamond Botkiller Scattergun Mk.I",
                "Id": "tf_weapon_scattergun",
                "Icon": "None"
            },
            "Silver Botkiller Scattergun Mk.II": {
                "name": "Silver Botkiller Scattergun Mk.II",
                "Id": "tf_weapon_scattergun",
                "Icon": "fob_e_scattergun_engi"
            },
            "Gold Botkiller Scattergun Mk.II": {
                "name": "Gold Botkiller Scattergun Mk.II",
                "Id": "tf_weapon_scattergun",
                "Icon": "fob_e_scattergun_gold"
            },
            "Festive Force-A-Nature": {
                "name": "Festive Force-A-Nature",
                "Id": "tf_weapon_scattergun",
                "Icon": "xms_double_barrel"
            },
        },
        "Secondary": {
            "Pistol": {
                "name": "Pistol",
                "Id": "tf_weapon_pistol",
                "Icon": "pistol"
            },
            "Bonk! Atomic Punch": {
                "name": "Bonk! Atomic Punch",
                "Id": "tf_weapon_lunchbox_drink",
                "Icon": "Backpack_Bonk!_Atomic_Punch"
            },
            "Crit-a-Cola": {
                "name": "Crit-a-Cola",
                "Id": "tf_weapon_lunchbox_drink",
                "Icon": "Backpack_Crit-a-Cola"
            },
            "Mad Milk": {
                "name": "Mad Milk",
                "Id": "tf_weapon_jar_milk",
                "Icon": "Backpack_Mad_Milk"
            },
            "Lugermorph": {
                "name": "Lugermorph",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_Lugermorph"
            },
            "The Winger": {
                "name": "The Winger",
                "Id": "tf_weapon_handgun_scout_secondary",
                "Icon": "Backpack_Winger"
            },
            "Pretty Boy's Pocket Pistol": {
                "name": "Pretty Boy's Pocket Pistol",
                "Id": "tf_weapon_handgun_scout_secondary",
                "Icon": "Backpack_Pretty_Pocket"
            },
            "The Flying Guillotine": {
                "name": "The Flying Guillotine",
                "Id": "tf_weapon_cleaver",
                "Icon": "Backpack_Flying_Guillotine"
            },
            "Mutated Milk": {
                "name": "Mutated Milk",
                "Id": "tf_weapon_jar_milk",
                "Icon": "Backpack_Mutated_Milk"
            },
            "Festive Bonk!": {
                "name": "Festive Bonk!",
                "Id": "tf_weapon_lunchbox_drink",
                "Icon": "xms_energy_drink"
            },
            "The C.A.P.P.E.R.": {
                "name": "The C.A.P.P.E.R.",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_C.A.P.P.E.R"
            }
        },
        "Melee": {
            "Bat": {
                "name": "Bat",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Bat"
            },
            "The Sandman": {
                "name": "The Sandman",
                "Id": "tf_weapon_bat_wood",
                "Icon": "Backpack_Sandman"
            },
            "The Holy Mackerel": {
                "name": "The Holy Mackerel",
                "Id": "tf_weapon_bat_fish",
                "Icon": "holymackerel"
            },
            "Frying Pan": {
                "name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "The Candy Cane": {
                "name": "The Candy Cane",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Candy_Cane"
            },
            "The Boston Basher": {
                "name": "The Boston Basher",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Boston_Basher"
            },
            "Sun-on-a-Stick": {
                "name": "Sun-on-a-Stick",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Sun-on-a-Stick"
            },
            "The Fan O'War": {
                "name": "The Fan O'War",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Fan_War"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Atomizer": {
                "name": "The Atomizer",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Atomizer"
            },
            "Three-Rune Blade": {
                "name": "Three-Rune Blade",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Three-Rune_Blade"
            },
            "The Conscientious Objector": {
                "name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "Unarmed Combat": {
                "name": "Unarmed Combat",
                "Id": "tf_weapon_bat_fish",
                "Icon": "Backpack_Unarmed_Combat"
            },
            "The Wrap Assassin": {
                "name": "The Wrap Assassin",
                "Id": "tf_weapon_bat_giftwrap",
                "Icon": "Backpack_Wrap_Assassin"
            },
            "Festive Bat": {
                "name": "Festive Bat",
                "Id": "tf_weapon_bat",
                "Icon": "bat_xmas"
            },
            "The Freedom Staff": {
                "name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "8mm_camera"
            },
            "Festive Holy Mackerel": {
                "name": "Festive Holy Mackerel",
                "Id": "tf_weapon_bat_fish",
                "Icon": "holymackerel_xmas"
            },
            "The Ham Shank": {
                "name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Batsaber": {
                "name": "Batsaber",
                "Id": "tf_weapon_bat",
                "Icon": "Backpack_Batsaber"
            },
        }
    },
    "Soldier": {
        "Primary": {
            "Rocket Launcher": {
                "name": "Rocket Launcher",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "rocketlauncher_sold"
            },
            "The Direct Hit": {
                "name": "The Direct Hit",
                "Id": "tf_weapon_rocketlauncher_directhit",
                "Icon": "directhit"
            },
            "The Black Box": {
                "name": "The Black Box",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "blackbox"
            },
            "Rocket Jumper": {
                "name": "Rocket Jumper",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "rocketjumper"
            },
            "The Liberty Launcher": {
                "name": "The Liberty Launcher",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "liberty_launcher"
            },
            "The Cow Mangler 5000": {
                "name": "The Cow Mangler 5000",
                "Id": "tf_weapon_particle_cannon",
                "Icon": "drg_cowmangler"
            },
            "The Original": {
                "name": "The Original",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "Backpack_Original"
            },
            "Festive Rocket Launcher": {
                "name": "Festive Rocket Launcher",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "rocketlauncher_xmas"
            },
            "The Beggar's Bazooka": {
                "name": "The Beggar's Bazooka",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "Bazooka"
            },
            "Silver Botkiller Rocket Launcher Mk.I": {
                "name": "Silver Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Gold Botkiller Rocket Launcher Mk.I": {
                "name": "Gold Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Rust Botkiller Rocket Launcher Mk.I": {
                "name": "Rust Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Blood Botkiller Rocket Launcher Mk.I": {
                "name": "Blood Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Carbonado Botkiller Rocket Launcher Mk.I": {
                "name": "Carbonado Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Diamond Botkiller Rocket Launcher Mk.I": {
                "name": "Diamond Botkiller Rocket Launcher Mk.I",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "None"
            },
            "Silver Botkiller Rocket Launcher Mk.II": {
                "name": "Silver Botkiller Rocket Launcher Mk.II",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "fob_e_rocketlauncher"
            },
            "Gold Botkiller Rocket Launcher Mk.II": {
                "name": "Gold Botkiller Rocket Launcher Mk.II",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "fob_e_rocketlauncher_gold"
            },
            "Festive Black Box": {
                "name": "Festive Black Box",
                "Id": "tf_weapon_rocketlauncher",
                "Icon": "blackbox_xmas"
            },
            "The Air Strike": {
                "name": "The Air Strike",
                "Id": "The Air Strike",
                "Icon": "Backpack_Air_Strike"
            },
        },
        "Secondary": {
            "Shotgun": {
                "name": "Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun"
            },
            "The Buff Banner": {
                "name": "The Buff Banner",
                "Id": "tf_weapon_buff_item",
                "Icon": "buffpack"
            },
            "The Gunboats": {
                "name": "The Gunboats",
                "Id": "tf_wearable",
                "Icon": "rocketboots_soldier"
            },
            "The Battalion's Backup": {
                "name": "The Battalion's Backup",
                "Id": "tf_weapon_buff_item",
                "Icon": "None"
            },
            "The Concheror": {
                "name": "The Concheror",
                "Id": "tf_weapon_buff_item",
                "Icon": "None"
            },
            "The Reserve Shooter": {
                "name": "The Reserve Shooter",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "The Righteous Bison": {
                "name": "The Righteous Bison",
                "Id": "tf_weapon_raygun",
                "Icon": "drg_righteousbison"
            },
            "The Mantreads": {
                "name": "The Mantreads",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "Festive Buff Banner": {
                "name": "Festive Buff Banner",
                "Id": "tf_weapon_buff_item",
                "Icon": "buffpack_xmas"
            },
            "The B.A.S.E. Jumper": {
                "name": "The B.A.S.E. Jumper",
                "Id": "tf_weapon_parachute",
                "Icon": "c_paratrooper_pack"
            },
            "Festive Shotgun": {
                "name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
        },
        "Melee": {
            "Shovel": {
                "name": "Shovel",
                "Id": "tf_weapon_shovel",
                "Icon": "shovel"
            },
            "The Equalizer": {
                "name": "The Equalizer",
                "Id": "tf_weapon_shovel",
                "Icon": "pickaxe_s2"
            },
            "The Pain Train": {
                "name": "The Pain Train",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "Frying Pan": {
                "name": "Frying Pan",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "The Half-Zatoichi": {
                "name": "The Half-Zatoichi",
                "Id": "tf_weapon_katana",
                "Icon": "None"
            },
            "The Market Gardener": {
                "name": "The Market Gardener",
                "Id": "tf_weapon_shovel",
                "Icon": "gardener"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Disciplinary Action": {
                "name": "The Disciplinary Action",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "The Conscientious Objector": {
                "name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Escape Plan": {
                "name": "The Escape Plan",
                "Id": "tf_weapon_shovel",
                "Icon": "pickaxe"
            },
            "The Freedom Staff": {
                "name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
        }
    },
    "Pyro": {
        "Primary": {
            "Flame Thrower": {
                "name": "Flame Thrower",
                "Id": "tf_weapon_flamethrower",
                "Icon": "Backpack_Flame_Thrower"
            },
            "The Backburner": {
                "name": "The Backburner",
                "Id": "tf_weapon_flamethrower",
                "Icon": "backburner"
            },
            "The Degreaser": {
                "name": "The Degreaser",
                "Id": "tf_weapon_flamethrower",
                "Icon": "degreaser"
            },
            "The Phlogistinator": {
                "name": "The Phlogistinator",
                "Id": "tf_weapon_flamethrower",
                "Icon": "drg_phlogistinator"
            },
            "Festive Flame Thrower": {
                "name": "Festive Flame Thrower",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_xmas"
            },
            "The Rainblower": {
                "name": "The Rainblower",
                "Id": "tf_weapon_flamethrower",
                "Icon": "rainblower"
            },
            "Silver Botkiller Flame Thrower Mk.I": {
                "name": "Silver Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "fob_h_flamethrower"
            },
            "Gold Botkiller Flame Thrower Mk.I": {
                "name": "Gold Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "None"
            },
            "Rust Botkiller Flame Thrower Mk.I": {
                "name": "Rust Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_rust"
            },
            "Blood Botkiller Flame Thrower Mk.I": {
                "name": "Blood Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_blood"
            },
            "Carbonado Botkiller Flame Thrower Mk.I": {
                "name": "Carbonado Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_rust"
            },
            "Diamond Botkiller Flame Thrower Mk.I": {
                "name": "Diamond Botkiller Flame Thrower Mk.I",
                "Id": "tf_weapon_flamethrower",
                "Icon": "flamethrower_diamond"
            },
            "Silver Botkiller Flame Thrower Mk.II": {
                "name": "Silver Botkiller Flame Thrower Mk.II",
                "Id": "tf_weapon_flamethrower",
                "Icon": "fob_e_flamethrower"
            },
            "Gold Botkiller Flame Thrower Mk.II": {
                "name": "Gold Botkiller Flame Thrower Mk.II",
                "Id": "tf_weapon_flamethrower",
                "Icon": "fob_e_flamethrower_gold"
            },
            "Festive Backburner": {
                "name": "Festive Backburner",
                "Id": "tf_weapon_flamethrower",
                "Icon": "backburner_xmas"
            },
            "Dragon's Fury": {
                "name": "Dragon's Fury",
                "Id": "tf_weapon_rocketlauncher_fireball",
                "Icon": "flameball"
            },
        },
        "Secondary": {
            "Shotgun": {
                "name": "Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun"
            },
            "The Flare Gun": {
                "name": "The Flare Gun",
                "Id": "tf_weapon_flaregun",
                "Icon": "flaregun_pyro"
            },
            "The Detonator": {
                "name": "The Detonator",
                "Id": "tf_weapon_flaregun",
                "Icon": "detonator"
            },
            "The Reserve Shooter": {
                "name": "The Reserve Shooter",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "The Manmelter": {
                "name": "The Manmelter",
                "Id": "tf_weapon_flaregun_revenge",
                "Icon": "drg_manmelter"
            },
            "The Scorch Shot": {
                "name": "The Scorch Shot",
                "Id": "tf_weapon_flaregun",
                "Icon": "None"
            },
            "Festive Flare Gun": {
                "name": "Festive Flare Gun",
                "Id": "tf_weapon_flaregun",
                "Icon": "flaregun"
            },
            "Festive Shotgun": {
                "name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "Thermal Thruster": {
                "name": "Thermal Thruster",
                "Id": "tf_weapon_rocketpack",
                "Icon": "rocketpack"
            },
            "Gas Passer": {
                "name": "Gas Passer",
                "Id": "tf_weapon_jar_gas",
                "Icon": "gascan"
            },
        },
        "Melee": {
            "Fire Axe": {
                "name": "Fire Axe",
                "Id": "tf_weapon_fireaxe",
                "Icon": "fireaxe_pyro"
            },
            "The Axtinguisher": {
                "name": "The Axtinguisher",
                "Id": "tf_weapon_fireaxe",
                "Icon": "axtinguisher_pyro"
            },
            "Homewrecker": {
                "name": "Homewrecker",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Powerjack": {
                "name": "The Powerjack",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "Frying Pan": {
                "name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "The Back Scratcher": {
                "name": "The Back Scratcher",
                "Id": "tf_weapon_fireaxe",
                "Icon": "back_scratcher"
            },
            "Sharpened Volcano Fragment": {
                "name": "Sharpened Volcano Fragment",
                "Id": "tf_weapon_fireaxe",
                "Icon": "fire_axe"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Postal Pummeler": {
                "name": "The Postal Pummeler",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Maul": {
                "name": "The Maul",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Conscientious Objector": {
                "name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Third Degree": {
                "name": "The Third Degree",
                "Id": "tf_weapon_fireaxe",
                "Icon": "drg_thirddegree"
            },
            "The Lollichop": {
                "name": "The Lollichop",
                "Id": "tf_weapon_fireaxe",
                "Icon": "lollichop"
            },
            "Neon Annihilator": {
                "name": "Neon Annihilator",
                "Id": "tf_weapon_breakable_sign",
                "Icon": "None"
            },
            "The Freedom Staff": {
                "name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Festive Axtinguisher": {
                "name": "The Festive Axtinguisher",
                "Id": "tf_weapon_fireaxe",
                "Icon": "None"
            },
            "The Ham Shank": {
                "name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Hot Hand": {
                "name": "Hot Hand",
                "Id": "tf_weapon_slap",
                "Icon": "slapping_glove"
            },
        }
    },
    "Demoman": {
        "Primary": {
            "Grenade Launcher": {
                "name": "Grenade Launcher",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "grenadelauncher"
            },
            "The Loch-n-Load": {
                "name": "The Loch-n-Load",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "lochnload"
            },
            "Ali Baba's Wee Booties": {
                "name": "Ali Baba's Wee Booties",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "The Bootlegger": {
                "name": "The Bootlegger",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "The Loose Cannon": {
                "name": "The Loose Cannon",
                "Id": "tf_weapon_cannon",
                "Icon": "loose_cannon"
            },
            "Festive Grenade Launcher": {
                "name": "Festive Grenade Launcher",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "grenadelauncher_xmas"
            },
            "The B.A.S.E. Jumper": {
                "name": "The B.A.S.E. Jumper",
                "Id": "tf_weapon_parachute",
                "Icon": "None"
            },
            "The Iron Bomber": {
                "name": "The Iron Bomber",
                "Id": "tf_weapon_grenadelauncher",
                "Icon": "None"
            },
        },
        "Secondary": {
            "Stickybomb Launcher": {
                "name": "Stickybomb Launcher",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "stickybomb_launcher"
            },
            "The Scottish Resistance": {
                "name": "The Scottish Resistance",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "stickybomb_defender"
            },
            "The Chargin' Targe": {
                "name": "The Chargin' Targe",
                "Id": "tf_wearable_demoshield",
                "Icon": "targe"
            },
            "Sticky Jumper": {
                "name": "Sticky Jumper",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "sticky_jumper"
            },
            "The Splendid Screen": {
                "name": "The Splendid Screen",
                "Id": "tf_wearable_demoshield",
                "Icon": "None"
            },
            "Festive Stickybomb Launcher": {
                "name": "Festive Stickybomb Launcher",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "stickybomb_launcher_xmas"
            },
            "Silver Botkiller Stickybomb Launcher Mk.I": {
                "name": "Silver Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Gold Botkiller Stickybomb Launcher Mk.I": {
                "name": "Gold Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Rust Botkiller Stickybomb Launcher Mk.I": {
                "name": "Rust Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Blood Botkiller Stickybomb Launcher Mk.I": {
                "name": "Blood Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Carbonado Botkiller Stickybomb Launcher Mk.I": {
                "name": "Carbonado Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Diamond Botkiller Stickybomb Launcher Mk.I": {
                "name": "Diamond Botkiller Stickybomb Launcher Mk.I",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
            "Silver Botkiller Stickybomb Launcher Mk.II": {
                "name": "Silver Botkiller Stickybomb Launcher Mk.II",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "botkillere_stickybomb"
            },
            "Gold Botkiller Stickybomb Launcher Mk.II": {
                "name": "Gold Botkiller Stickybomb Launcher Mk.II",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "botkillere_stickybomb_gold"
            },
            "The Tide Turner": {
                "name": "The Tide Turner",
                "Id": "tf_wearable_demoshield",
                "Icon": "None"
            },
            "Festive Targe": {
                "name": "Festive Targe",
                "Id": "tf_wearable_demoshield",
                "Icon": "targe_xmas"
            },
            "The Quickiebomb Launcher": {
                "name": "The Quickiebomb Launcher",
                "Id": "tf_weapon_pipebomblauncher",
                "Icon": "None"
            },
        },
        "Melee": {
            "Bottle": {
                "name": "Bottle",
                "Id": "tf_weapon_bottle",
                "Icon": "bottle"
            },
            "The Eyelander": {
                "name": "The Eyelander",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "The Pain Train": {
                "name": "The Pain Train",
                "Id": "tf_weapon_shovel",
                "Icon": "None"
            },
            "The Scotsman's Skullcutter": {
                "name": "The Scotsman's Skullcutter",
                "Id": "tf_weapon_sword",
                "Icon": "battleaxe"
            },
            "Frying Pan": {
                "name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "Horseless Headless Horsemann's Headtaker": {
                "name": "Horseless Headless Horsemann's Headtaker",
                "Id": "tf_weapon_sword",
                "Icon": "headtaker"
            },
            "Ullapool Caber": {
                "name": "Ullapool Caber",
                "Id": "tf_weapon_stickbomb",
                "Icon": "caber"
            },
            "The Claidheamh Mòr": {
                "name": "The Claidheamh Mòr",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "The Half-Zatoichi": {
                "name": "The Half-Zatoichi",
                "Id": "tf_weapon_katana",
                "Icon": "None"
            },
            "The Persian Persuader": {
                "name": "The Persian Persuader",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Conscientious Objector": {
                "name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "Nessie's Nine Iron": {
                "name": "Nessie's Nine Iron",
                "Id": "tf_weapon_sword",
                "Icon": "golfclub"
            },
            "The Scottish Handshake": {
                "name": "The Scottish Handshake",
                "Id": "tf_weapon_bottle",
                "Icon": "None"
            },
            "The Freedom Staff": {
                "name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "Festive Eyelander": {
                "name": "Festive Eyelander",
                "Id": "tf_weapon_sword",
                "Icon": "None"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
        }
    },
    "Heavy": {
        "Primary": {
            "Minigun": {
                "name": "Minigun",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun1"
            },
            "Natascha": {
                "name": "Natascha",
                "Id": "tf_weapon_minigun",
                "Icon": "natasha"
            },
            "Iron Curtain": {
                "name": "Iron Curtain",
                "Id": "tf_weapon_minigun",
                "Icon": "curtain"
            },
            "The Brass Beast": {
                "name": "The Brass Beast",
                "Id": "tf_weapon_minigun",
                "Icon": "gatling_gun"
            },
            "Tomislav": {
                "name": "Tomislav",
                "Id": "tf_weapon_minigun",
                "Icon": "tomislav"
            },
            "Australium Tomislav": {
                "name": "Australium Tomislav",
                "Id": "tf_weapon_minigun",
                "Icon": "tomislav_gold"
            },
            "Festive Minigun": {
                "name": "Festive Minigun",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun_xmas"
            },
            "Silver Botkiller Minigun Mk.I": {
                "name": "Silver Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "fob_h_minigun"
            },
            "Gold Botkiller Minigun Mk.I": {
                "name": "Gold Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "fob_h_minigun_gold"
            },
            "The Huo-Long Heater": {
                "name": "The Huo-Long Heater",
                "Id": "tf_weapon_minigun",
                "Icon": "Backpack_Huo-Long_Heater"
            },
            "Deflector": {
                "name": "Deflector",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun1"
            },
            "Rust Botkiller Minigun Mk.I": {
                "name": "Rust Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun_rust"
            },
            "Blood Botkiller Minigun Mk.I": {
                "name": "Blood Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun_blood"
            },
            "Carbonado Botkiller Minigun Mk.I": {
                "name": "Carbonado Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun_diamond_black"
            },
            "Diamond Botkiller Minigun Mk.I": {
                "name": "Diamond Botkiller Minigun Mk.I",
                "Id": "tf_weapon_minigun",
                "Icon": "minigun_diamond"
            },
            "Silver Botkiller Minigun Mk.II": {
                "name": "Silver Botkiller Minigun Mk.II",
                "Id": "tf_weapon_minigun",
                "Icon": "fob_e_minigun"
            },
            "Gold Botkiller Minigun Mk.II": {
                "name": "Gold Botkiller Minigun Mk.II",
                "Id": "tf_weapon_minigun",
                "Icon": "fob_e_minigun_gold"
            },
        },
        "Secondary": {
            "Shotgun": {
                "name": "Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun"
            },
            "Sandvich": {
                "name": "Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "sandwich"
            },
            "The Dalokohs Bar": {
                "name": "The Dalokohs Bar",
                "Id": "tf_weapon_lunchbox",
                "Icon": "None"
            },
            "The Buffalo Steak Sandvich": {
                "name": "The Buffalo Steak Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "None"
            },
            "The Family Business": {
                "name": "The Family Business",
                "Id": "tf_weapon_shotgun_hwg",
                "Icon": "None"
            },
            "Fishcake": {
                "name": "Fishcake",
                "Id": "tf_weapon_lunchbox",
                "Icon": "None"
            },
            "Robo-Sandvich": {
                "name": "Robo-Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "robo_sandwich"
            },
            "Festive Sandvich": {
                "name": "Festive Sandvich",
                "Id": "tf_weapon_lunchbox",
                "Icon": "sandwich_xmas"
            },
            "Festive Shotgun": {
                "name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
            "Second Banana": {
                "name": "Second Banana",
                "Id": "tf_weapon_lunchbox",
                "Icon": "banana"
            },
        },
        "Melee": {
            "Fists": {
                "name": "Fists",
                "Id": "tf_weapon_fists",
                "Icon": "Backpack_Fists"
            },
            "The Killing Gloves of Boxing": {
                "name": "The Killing Gloves of Boxing",
                "Id": "tf_weapon_fists",
                "Icon": "boxing_gloves"
            },
            "Gloves of Running Urgently": {
                "name": "Gloves of Running Urgently",
                "Id": "tf_weapon_fists",
                "Icon": "boxing_gloves_urgency"
            },
            "Frying Pan": {
                "name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "Warrior's Spirit": {
                "name": "Warrior's Spirit",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "Fists of Steel": {
                "name": "Fists of Steel",
                "Id": "tf_weapon_fists",
                "Icon": "Backpack_Fists_of_Steel"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Eviction Notice": {
                "name": "The Eviction Notice",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "The Conscientious Objector": {
                "name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "Apoco-Fists": {
                "name": "Apoco-Fists",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "The Holiday Punch": {
                "name": "The Holiday Punch",
                "Id": "tf_weapon_fists",
                "Icon": "None"
            },
            "The Freedom Staff": {
                "name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "Festive Gloves of Running Urgently (G.R.U.)": {
                "name": "Festive Gloves of Running Urgently (G.R.U.)",
                "Id": "tf_weapon_fists",
                "Icon": "boxing_gloves_xmas"
            },
            "The Bread Bite": {
                "name": "The Bread Bite",
                "Id": "tf_weapon_fists",
                "Icon": "breadmonster_gloves"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
        }
    },
    "Engineer": {
        "Primary": {
            "Shotgun": {
                "name": "Shotgun",
                "Id": "tf_weapon_shotgun_primary",
                "Icon": "shotgun"
            },
            "Shotgun (Renamed/Str": {
                "name": "Shotgun (Renamed/Str",
                "Id": "ange)tf_weapon_shotgun",
                "Icon": "None"
            },
            "The Frontier Justice": {
                "name": "The Frontier Justice",
                "Id": "tf_weapon_sentry_revenge",
                "Icon": "frontierjustice"
            },
            "The Widowmaker": {
                "name": "The Widowmaker",
                "Id": "tf_weapon_shotgun_primary",
                "Icon": "None"
            },
            "The Pomson 6000": {
                "name": "The Pomson 6000",
                "Id": "tf_weapon_drg_pomson",
                "Icon": "drg_pomson"
            },
            "The Rescue Ranger": {
                "name": "The Rescue Ranger",
                "Id": "tf_weapon_shotgun_building_rescue",
                "Icon": "None"
            },
            "Festive Frontier Jus": {
                "name": "Festive Frontier Jus",
                "Id": "ticetf_weapon_sentry_revenge",
                "Icon": "frontierjustice_xmas"
            },
            "Festive Shotgun": {
                "name": "Festive Shotgun",
                "Id": "tf_weapon_shotgun",
                "Icon": "shotgun_xmas"
            },
            "Panic Attack": {
                "name": "Panic Attack",
                "Id": "tf_weapon_shotgun",
                "Icon": "None"
            },
        },
        "Secondary": {
            "Pistol": {
                "name": "Pistol",
                "Id": "tf_weapon_pistol",
                "Icon": "pistol"
            },
            "The Wrangler": {
                "name": "The Wrangler",
                "Id": "tf_weapon_laser_pointer",
                "Icon": "wrangler"
            },
            "Lugermorph": {
                "name": "Lugermorph",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_Lugermorph"
            },
            "The Short Circuit": {
                "name": "The Short Circuit",
                "Id": "tf_weapon_mechanical_arm",
                "Icon": "None"
            },
            "Festive Wrangler": {
                "name": "Festive Wrangler",
                "Id": "tf_weapon_laser_pointer",
                "Icon": "wrangler_xmas"
            },
            "Red Rock Roscoe": {
                "name": "Red Rock Roscoe",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Homemade Heater": {
                "name": "Homemade Heater",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Hickory Holepuncher": {
                "name": "Hickory Holepuncher",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Local Hero": {
                "name": "Local Hero",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Black Dahlia": {
                "name": "Black Dahlia",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Sandstone Special": {
                "name": "Sandstone Special",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Macabre Web": {
                "name": "Macabre Web",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Nutcracker": {
                "name": "Nutcracker",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Blue Mew": {
                "name": "Blue Mew",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Brain Candy": {
                "name": "Brain Candy",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Shot to Hell": {
                "name": "Shot to Hell",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Dressed To Kill": {
                "name": "Dressed To Kill",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "Blitzkrieg": {
                "name": "Blitzkrieg",
                "Id": "tf_weapon_pistol",
                "Icon": "None"
            },
            "The C.A.P.P.E.R.": {
                "name": "The C.A.P.P.E.R.",
                "Id": "tf_weapon_pistol",
                "Icon": "Backpack_C.A.P.P.E.R"
            },
            "The Gigar Counter": {
                "name": "The Gigar Counter",
                "Id": "tf_weapon_laser_pointer",
                "Icon": "None"
            }
        },
        "Melee": {
            "Wrench": {
                "name": "Wrench",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench"
            },
            "The Gunslinger": {
                "name": "The Gunslinger",
                "Id": "tf_weapon_robot_arm",
                "Icon": "gunslinger"
            },
            "The Southern Hospitality": {
                "name": "The Southern Hospitality",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Golden Wrench": {
                "name": "Golden Wrench",
                "Id": "tf_weapon_wrench",
                "Icon": "botkiller_wrench_gold"
            },
            "The Jag": {
                "name": "The Jag",
                "Id": "tf_weapon_wrench",
                "Icon": "jag"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Eureka Effect": {
                "name": "The Eureka Effect",
                "Id": "tf_weapon_wrench",
                "Icon": "drg_wrenchmotron"
            },
            "Festive Wrench": {
                "name": "Festive Wrench",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_xmas"
            },
            "Silver Botkiller Wrench Mk.I": {
                "name": "Silver Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "fob_h_wrench"
            },
            "Gold Botkiller Wrench Mk.I": {
                "name": "Gold Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "fob_h_wrench_gold"
            },
            "Rust Botkiller Wrench Mk.I": {
                "name": "Rust Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_rust"
            },
            "Blood Botkiller Wrench Mk.I": {
                "name": "Blood Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_blood"
            },
            "Carbonado Botkiller Wrench Mk.I": {
                "name": "Carbonado Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Diamond Botkiller Wrench Mk.I": {
                "name": "Diamond Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_diamond"
            },
            "Diamond Black Botkiller Wrench Mk.I": {
                "name": "Diamond Black Botkiller Wrench Mk.I",
                "Id": "tf_weapon_wrench",
                "Icon": "wrench_diamond_black"
            },
            "Silver Botkiller Wrench Mk.II": {
                "name": "Silver Botkiller Wrench Mk.II",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Gold Botkiller Wrench Mk.II": {
                "name": "Gold Botkiller Wrench Mk.II",
                "Id": "tf_weapon_wrench",
                "Icon": "None"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
        },
        "PDA": {
            "Construction PDA": {
                "name": "Construction PDA",
                "Id": "tf_weapon_pda_engineer_build",
                "Icon": "builder"
            },
            "Destruction PDA": {
                "name": "Destruction PDA",
                "Id": "tf_weapon_pda_engineer_destroy",
                "Icon": "pda_engineer"
            }
        }
    },
    "Medic": {
        "Primary": {
            "Syringe Gun": {
                "name": "Syringe Gun",
                "Id": "tf_weapon_syringegun_medic",
                "Icon": "syringegun"
            },
            "The Blutsauger": {
                "name": "The Blutsauger",
                "Id": "tf_weapon_syringegun_medic",
                "Icon": "bloodsiger"
            },
            "Crusader's Crossbow": {
                "name": "Crusader's Crossbow",
                "Id": "tf_weapon_crossbow",
                "Icon": "None"
            },
            "The Overdose": {
                "name": "The Overdose",
                "Id": "tf_weapon_syringegun_medic",
                "Icon": "overdose"
            },
            "Festive Crusader's Crossbow": {
                "name": "Festive Crusader's Crossbow",
                "Id": "tf_weapon_crossbow",
                "Icon": "None"
            }
        },
        "Secondary": {
            "Medi Gun": {
                "name": "Medi Gun",
                "Id": "tf_weapon_medigun",
                "Icon": "w_medigun"
            },
            "The Kritzkrieg": {
                "name": "The Kritzkrieg",
                "Id": "tf_weapon_medigun",
                "Icon": "medigun_overhealer"
            },
            "The Quick-Fix": {
                "name": "The Quick-Fix",
                "Id": "tf_weapon_medigun",
                "Icon": "proto_medigun"
            },
            "Festive Medi Gun": {
                "name": "Festive Medi Gun",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Silver Botkiller Medi Gun Mk.I": {
                "name": "Silver Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Gold Botkiller Medi Gun Mk.I": {
                "name": "Gold Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Rust Botkiller Medi Gun Mk.I": {
                "name": "Rust Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Blood Botkiller Medi Gun Mk.I": {
                "name": "Blood Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Carbonado Botkiller Medi Gun Mk.I": {
                "name": "Carbonado Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Diamond Botkiller Medi Gun Mk.I": {
                "name": "Diamond Botkiller Medi Gun Mk.I",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
            "Silver Botkiller Medi Gun Mk.II": {
                "name": "Silver Botkiller Medi Gun Mk.II",
                "Id": "tf_weapon_medigun",
                "Icon": "fob_h_medigun"
            },
            "Gold Botkiller Medi Gun Mk.II": {
                "name": "Gold Botkiller Medi Gun Mk.II",
                "Id": "tf_weapon_medigun",
                "Icon": "fob_h_medigun_gold"
            },
            "The Vaccinator": {
                "name": "The Vaccinator",
                "Id": "tf_weapon_medigun",
                "Icon": "None"
            },
        },
        "Melee": {
            "Bonesaw": {
                "name": "Bonesaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "bonesaw"
            },
            "The Ubersaw": {
                "name": "The Ubersaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "ubersaw"
            },
            "The Vita-Saw": {
                "name": "The Vita-Saw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "uberneedle"
            },
            "Frying Pan": {
                "name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "Amputator": {
                "name": "Amputator",
                "Id": "tf_weapon_bonesaw",
                "Icon": "amputator"
            },
            "The Solemn Vow": {
                "name": "The Solemn Vow",
                "Id": "tf_weapon_bonesaw",
                "Icon": "hippocrates_bust"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Conscientious Objector": {
                "name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Freedom Staff": {
                "name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "Festive Ubersaw": {
                "name": "Festive Ubersaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "ubersaw_xmas"
            },
            "The Ham Shank": {
                "name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Festive Bonesaw": {
                "name": "Festive Bonesaw",
                "Id": "tf_weapon_bonesaw",
                "Icon": "bonesaw_xmas"
            },
        }
    },
    "Sniper": {
        "Primary": {
            "Rifle": {
                "name": "Rifle",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "fob_e_sniperrifle"
            },
            "The Huntsman": {
                "name": "The Huntsman",
                "Id": "tf_weapon_compound_bow",
                "Icon": "bow"
            },
            "The Sydney Sleeper": {
                "name": "The Sydney Sleeper",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "The Bazaar Bargain": {
                "name": "The Bazaar Bargain",
                "Id": "tf_weapon_sniperrifle_decap",
                "Icon": "bazaar_sniper"
            },
            "The Machina": {
                "name": "The Machina",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Festive Sniper Rifle": {
                "name": "Festive Sniper Rifle",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "sniperrifle_xmas"
            },
            "The Hitman's Heatmaker": {
                "name": "The Hitman's Heatmaker",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Silver Botkiller Sniper Rifle Mk.I": {
                "name": "Silver Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Gold Botkiller Sniper Rifle Mk.I": {
                "name": "Gold Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "The AWPer Hand": {
                "name": "The AWPer Hand",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "awp"
            },
            "Rust Botkiller Sniper Rifle Mk.I": {
                "name": "Rust Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Blood Botkiller Sniper Rifle Mk.I": {
                "name": "Blood Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Carbonado Botkiller Sniper Rifle Mk.I": {
                "name": "Carbonado Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Diamond Botkiller Sniper Rifle Mk.I": {
                "name": "Diamond Botkiller Sniper Rifle Mk.I",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "None"
            },
            "Silver Botkiller Sniper Rifle Mk.II": {
                "name": "Silver Botkiller Sniper Rifle Mk.II",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "fob_e_sniperrifle"
            },
            "Gold Botkiller Sniper Rifle Mk.II": {
                "name": "Gold Botkiller Sniper Rifle Mk.II",
                "Id": "tf_weapon_sniperrifle",
                "Icon": "fob_e_sniperrifle_gold"
            },
            "Festive Huntsman": {
                "name": "Festive Huntsman",
                "Id": "tf_weapon_compound_bow",
                "Icon": "bow_xmas"
            },
            "The Fortified Compound": {
                "name": "The Fortified Compound",
                "Id": "tf_weapon_compound_bow",
                "Icon": "None"
            },
            "The Classic": {
                "name": "The Classic",
                "Id": "tf_weapon_sniperrifle_classic",
                "Icon": "tfc_sniperrifle"
            },
            "Shooting Star": {
                "name": "Shooting Star",
                "Id": "tf_weapon_sniperrifle ",
                "Icon": "None"
            }
        },
        "Secondary": {
            "SMG": {
                "name": "SMG",
                "Id": "tf_weapon_smg",
                "Icon": "smg"
            },
            "The Razorback": {
                "name": "The Razorback",
                "Id": "tf_wearable_razorback",
                "Icon": "None"
            },
            "Jarate": {
                "name": "Jarate",
                "Id": "tf_weapon_jar",
                "Icon": "urinejar"
            },
            "Darwin's Danger Shield": {
                "name": "Darwin's Danger Shield",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "Cozy Camper": {
                "name": "Cozy Camper",
                "Id": "tf_wearable",
                "Icon": "None"
            },
            "The Cleaner's Carbine": {
                "name": "The Cleaner's Carbine",
                "Id": "tf_weapon_charged_smg",
                "Icon": "None"
            },
            "Festive Jarate": {
                "name": "Festive Jarate",
                "Id": "tf_weapon_jar",
                "Icon": "xms_urinejar"
            },
            "The Self-Aware Beauty Mark": {
                "name": "The Self-Aware Beauty Mark",
                "Id": "tf_weapon_jar",
                "Icon": "breadmonster"
            },
            "Festive SMG": {
                "name": "Festive SMG",
                "Id": "tf_weapon_smg",
                "Icon": "smg_xmas"
            },
        },
        "Melee": {
            "Kukri": {
                "name": "Kukri",
                "Id": "tf_weapon_club",
                "Icon": "machete"
            },
            "The Tribalman's Shiv": {
                "name": "The Tribalman's Shiv",
                "Id": "tf_weapon_club",
                "Icon": "wood_machete"
            },
            "The Bushwacka": {
                "name": "The Bushwacka",
                "Id": "tf_weapon_club",
                "Icon": "None"
            },
            "Frying Pan": {
                "name": "Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Frying_Pan"
            },
            "The Shahanshah": {
                "name": "The Shahanshah",
                "Id": "tf_weapon_club",
                "Icon": "None"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Conscientious Objector": {
                "name": "The Conscientious Objector",
                "Id": "saxxy",
                "Icon": "Backpack_Conscientious_Objector"
            },
            "The Freedom Staff": {
                "name": "The Freedom Staff",
                "Id": "saxxy",
                "Icon": "Backpack_Freedom_Staff"
            },
            "The Bat Outta Hell": {
                "name": "The Bat Outta Hell",
                "Id": "saxxy",
                "Icon": "Backpack_Bat_Outta_Hell"
            },
            "The Memory Maker": {
                "name": "The Memory Maker",
                "Id": "saxxy",
                "Icon": "None"
            },
            "The Ham Shank": {
                "name": "The Ham Shank",
                "Id": "saxxy",
                "Icon": "Backpack_Ham_Shank"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
            "The Necro Smasher": {
                "name": "The Necro Smasher",
                "Id": "saxxy",
                "Icon": "Backpack_Necro_Smasher"
            },
            "The Crossing Guard": {
                "name": "The Crossing Guard",
                "Id": "saxxy",
                "Icon": "Backpack_Crossing_Guard"
            },
            "Prinny Machete": {
                "name": "Prinny Machete",
                "Id": "saxxy",
                "Icon": "None"
            }
        }
    },
    "Spy": {
        "Primary": {
            "Revolver": {
                "name": "Revolver",
                "Id": "tf_weapon_revolver",
                "Icon": "revolver"
            },
            "The Ambassador": {
                "name": "The Ambassador",
                "Id": "tf_weapon_revolver",
                "Icon": "ambassador_opt"
            },
            "Big Kill": {
                "name": "Big Kill",
                "Id": "tf_weapon_revolver",
                "Icon": "None"
            },
            "L'Etranger": {
                "name": "L'Etranger",
                "Id": "tf_weapon_revolver",
                "Icon": "letranger"
            },
            "The Enforcer": {
                "name": "The Enforcer",
                "Id": "tf_weapon_revolver",
                "Icon": "None"
            },
            "The Diamondback": {
                "name": "The Diamondback",
                "Id": "tf_weapon_revolver",
                "Icon": "None"
            },
            "Festive Ambassador": {
                "name": "Festive Ambassador",
                "Id": "tf_weapon_revolver",
                "Icon": "ambassador_xmas"
            },
            "Festive Revolver": {
                "name": "Festive Revolver",
                "Id": "tf_weapon_revolver",
                "Icon": "revolver_xmas"
            },
        },
        "Secondary": {
            "Sapper": {
                "name": "Sapper",
                "Id": "tf_weapon_builder",
                "Icon": "sapper"
            },
            "The Red-Tape Recorder": {
                "name": "The Red-Tape Recorder",
                "Id": "tf_weapon_sapper",
                "Icon": "None"
            },
            "The Ap-Sap (Genuine)": {
                "name": "The Ap-Sap (Genuine)",
                "Id": "tf_weapon_sapper",
                "Icon": "p2rec"
            },
            "Festive Sapper": {
                "name": "Festive Sapper",
                "Id": "tf_weapon_sapper",
                "Icon": "sapper_xmas"
            },
            "The Snack Attack": {
                "name": "The Snack Attack",
                "Id": "tf_weapon_sapper",
                "Icon": "breadmonster_sap"
            }
        },
        "Melee": {
            "Knife": {
                "name": "Knife",
                "Id": "tf_weapon_knife",
                "Icon": "knife"
            },
            "Your Eternal Reward": {
                "name": "Your Eternal Reward",
                "Id": "tf_weapon_knife",
                "Icon": "eternal_reward"
            },
            "Conniver's Kunai": {
                "name": "Conniver's Kunai",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Saxxy": {
                "name": "Saxxy",
                "Id": "saxxy",
                "Icon": "Backpack_Saxxy"
            },
            "The Big Earner": {
                "name": "The Big Earner",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "The Wanga Prick": {
                "name": "The Wanga Prick",
                "Id": "tf_weapon_knife",
                "Icon": "voodoo_pin"
            },
            "The Sharp Dresser": {
                "name": "The Sharp Dresser",
                "Id": "tf_weapon_knife",
                "Icon": "acr_hookblade"
            },
            "The Spy-cicle": {
                "name": "The Spy-cicle",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Festive Knife": {
                "name": "Festive Knife",
                "Id": "tf_weapon_knife",
                "Icon": "knife_xmas"
            },
            "The Black Rose": {
                "name": "The Black Rose",
                "Id": "tf_weapon_knife",
                "Icon": "ava_roseknife_v"
            },
            "Silver Botkiller Knife Mk.I": {
                "name": "Silver Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Gold Botkiller Knife Mk.I": {
                "name": "Gold Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Rust Botkiller Knife Mk.I": {
                "name": "Rust Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_rust"
            },
            "Blood Botkiller Knife Mk.I": {
                "name": "Blood Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_blood"
            },
            "Carbonado Botkiller Knife Mk.I": {
                "name": "Carbonado Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "None"
            },
            "Diamond Botkiller Knife Mk.I": {
                "name": "Diamond Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_diamond"
            },
            "Diamond Black Botkiller Knife Mk.I": {
                "name": "Diamond Black Botkiller Knife Mk.I",
                "Id": "tf_weapon_knife",
                "Icon": "knife_diamond_black"
            },
            "Silver Botkiller Knife Mk.II": {
                "name": "Silver Botkiller Knife Mk.II",
                "Id": "tf_weapon_knife",
                "Icon": "knife_botkiller_mk2"
            },
            "Gold Botkiller Knife Mk.II": {
                "name": "Gold Botkiller Knife Mk.II",
                "Id": "tf_weapon_knife",
                "Icon": "knife_botkiller_mk2_gold"
            },
            "Gold Frying Pan": {
                "name": "Gold Frying Pan",
                "Id": "saxxy",
                "Icon": "Backpack_Golden_Frying_Pan"
            },
        },
        "Clock": {
            "Invis Watch": {
                "name": "Invis Watch",
                "Id": "tf_weapon_invis",
                "Icon": "spy_watch"
            },
            "The Dead Ringer": {
                "name": "The Dead Ringer",
                "Id": "tf_weapon_invis",
                "Icon": "pocket_watch"
            },
            "The Cloak and Dagger": {
                "name": "The Cloak and Dagger",
                "Id": "tf_weapon_invis",
                "Icon": "leather_watch"
            },
            "Enthusiast's Timepiece": {
                "name": "Enthusiast's Timepiece",
                "Id": "tf_weapon_invis",
                "Icon": "ttg_watch"
            },
            "The Quackenbirdt": {
                "name": "The Quackenbirdt",
                "Id": "tf_weapon_invis ",
                "Icon": "None"
            }
        }
    }
}