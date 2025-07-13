import random
from atribute_libary import Atribute
from cosmetic_libary import Cosmetic
from weapons_libary import Weapon_Libary
from rich.console import Console
from rich.table import Table
from rich import print

class Robot:
    def __init__(self, robot_type, size=1.0, squad=None, speed=0, skill="Normal", path=None):
        self.robot_type = robot_type
        self.size = size
        self.squad = squad
        self.speed = speed
        self.skill = skill
        self.path = path
        self.power = 0
        self.max_vision_range = None  # Initialize here to ensure availability

        if self.robot_type not in ["Mini Sentry Buster", "Sentry Buster"]:
            self.cosmetics = self.assign_cosmetics()
            self.weapons = self.assign_weapons()
            self.character_attributes = self.assign_character_attributes()
        else:
            self.cosmetics = []
            self.weapons = {}
            self.character_attributes = {}

        self.health = self.calculate_health()
        self.max_vision_range = self.assign_max_vision_range()
        self.power += self.calculate_power()  # Calculate at the end

    def calculate_health(self):
        return int(100 * self.size)

    def assign_max_vision_range(self):
        base_vision = 800
        vision_bonus = self.power * 1000
        return int(base_vision + vision_bonus)

    def assign_cosmetics(self):
        if self.robot_type == "Tank":
            return []

        available_cosmetics = [
            cosmetic for cosmetic in Cosmetic.values()
            if "Class" in cosmetic and (
                isinstance(cosmetic["Class"], str) and self.robot_type == cosmetic["Class"]
                or isinstance(cosmetic["Class"], list) and self.robot_type in cosmetic["Class"]
            )
        ]
        return random.sample(available_cosmetics, min(len(available_cosmetics), random.randint(1, 8)))

    def assign_weapons(self):
        if self.robot_type == "Tank":
            return {"None": {"Name": "No Weapon", "ItemAttributes": {}}}

        weapon_name = random.choice(list(random.choice(list(Weapon_Libary[self.robot_type].values()))))
        item_attributes = self.assign_item_attributes()

        return {self.robot_type: {"Name": weapon_name, "ItemAttributes": item_attributes}}

    def assign_item_attributes(self):
        possible_attributes = list(Atribute.keys())
        selected_attributes = random.sample(possible_attributes, int(random.randint(1, 3) * self.power))
        item_attributes = {}

        for attr in selected_attributes:
            if "Mod" in attr or "Mode" in attr:
                item_attributes[attr] = 1
            else:
                effect_type = Atribute[attr].get("Effect", "Neutral")
                if effect_type == "Positive":
                    value = 0.15
                    self.power += value
                elif effect_type == "Negative":
                    value = -0.15
                    self.power += value
                else:
                    value = 1
                item_attributes[attr] = value

        return item_attributes

    def assign_character_attributes(self):
        attributes = { }
        possible_attributes = list(Atribute.keys())
        selected_attributes = random.sample(possible_attributes, random.randint(1, 3))

        for attr in selected_attributes:
            if "Mod" in attr or "Mode" in attr:
                attributes[attr] = 1
            else:
                effect_type = Atribute[attr].get("Effect", "Neutral")
                if effect_type == "Positive":
                    value = round(random.uniform(0.1, 1), 2)
                    self.power += value
                elif effect_type == "Negative":
                    value = round(random.uniform(0.1, 1), 2)
                    self.power += value
                else:
                    value = 1
                attributes[attr] = value

        return attributes

    def calculate_power(self):
        power = 0
        base_power = {
            "Scout": 0.1, "Soldier": 0.25, "Pyro": 0.2, "Demoman": 0.2,
            "Heavy": 0.45, "Engineer": 0.35, "Medic": 0.15, "Sniper": 0.12,
            "Spy": 0.12, "Tank": 2.0, "Sentry Buster": 0.5, "Mini Sentry Buster": 0.3
        }
        power += base_power.get(self.robot_type, 0)

        for weapon in self.weapons.values():
            for attr, value in weapon["ItemAttributes"].items():
                power += value

        for attr, value in self.character_attributes.items():
            if attr == "move_speed":
                power += (value - 1.0) * 0.5
            elif attr == "damage_resistance":
                power += value * 0.3

        return power


class Mission:
    def __init__(self, waves, difficulty, available_paths=None, progression_factor=1.1, default_robot_params=None):
        self.waves = waves
        self.difficulty = difficulty
        self.progression_factor = progression_factor
        self.default_robot_params = default_robot_params or {
            "Scout":    {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Soldier":  {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Pyro":     {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Demoman":  {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Heavy":    {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Engineer": {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Medic":    {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Sniper":   {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Spy":      {"size": 1.0, "speed": 1,   "skill": "Normal"},
            "Tank":     {"size": 1.0, "speed": 75,  "skill": "Normal"},
        }
        self.available_paths = available_paths or [
            {"standard_path": "Path_A", "tank_paths": ["Tank_Path_A", "Tank_Path_B"]},
            {"standard_path": "Path_B", "tank_paths": ["Tank_Path_C", "Tank_Path_D"]},
            {"standard_path": "Path_C", "tank_paths": ["Tank_Path_E", "Tank_Path_F"]},
            {"standard_path": "Path_D", "tank_paths": ["Tank_Path_G", "Tank_Path_H"]},
        ]

    def generate_helpers(self, wave_number):
        helper_types = ["Spy", "Sniper", "Sydney Sniper", "Mini Sentry Buster", "Sentry Buster", "Engineer"]
        max_helpers = min(3, wave_number)
        helpers = []

        for _ in range(random.randint(1, max_helpers)):
            helper_type = random.choice(helper_types)
            if helper_type == "Sydney Sniper":
                helper_type = "Sniper"

            helper_robot = Robot(
                robot_type=helper_type,
                size=1.0,
                squad=f"Helper-Squad-{wave_number}",
                speed=1,
                skill="Normal",
                path=None
            )
            helpers.append(helper_robot)

        return helpers

    def generate_wave(self, wave_number):
        selected_path_set = random.choice(self.available_paths)
        path = selected_path_set["standard_path"]
        tank_paths = selected_path_set["tank_paths"]

        total_robots = max(5, int((wave_number ** self.progression_factor) * self.difficulty * 1.5))
        squad_count = max(2, min(4 + (10 - self.difficulty) // 2, 7))
        squads = self.generate_squads(squad_count, total_robots, wave_number, path, tank_paths)
        squads = self.adjust_squads(squads, wave_number)
        self.assign_squad_parameters(squads, wave_number)

        helpers = self.generate_helpers(wave_number)

        return squads, path, helpers

    def generate_squads(self, squad_count, total_robots, wave_number, path, tank_paths):
        squads = []
        remaining_robots = total_robots
        tank_count = 0

        for _ in range(remaining_robots):
            robot_type = random.choice(list(self.default_robot_params.keys()))
            if robot_type == "Tank":
                tank_count += 1

        remaining_robots -= tank_count

        for squad_index in range(1, squad_count + 1):
            if remaining_robots < 2:
                if squads:
                    squads[-1]["robots"].extend(self.create_robots(remaining_robots, squads[-1]["name"], wave_number, path))
                break

            if squad_index == squad_count:
                squad_size = remaining_robots
            else:
                max_size = 3 if random.random() < 0.8 else 5
                squad_size = random.randint(2, min(max_size, remaining_robots)) if max_size >= 2 else remaining_robots

            remaining_robots -= squad_size

            squad_robots = self.create_robots(squad_size, f"Squad-{squad_index}", wave_number, path)
            squad_parameters = {
                "name": f"Squad-{squad_index}",
                "robots": squad_robots,
                "wait_between_spawns": None,
                "wait_before_starting": None,
                "wait_all_dead": None,
                "wait_all_spawn": None,
                "total_count": len(squad_robots),
                "max_active": max(1, len(squad_robots) // 2),
                "spawn_count": len(squad_robots)
            }
            squads.append(squad_parameters)

        for tank_index in range(tank_count):
            tank_path = random.choice(tank_paths)
            tank_robots = self.create_robots(1, f"Tank-Squad-{tank_index + 1}", wave_number, tank_path, tank_only=True)
            squad_parameters = {
                "name": f"Tank-Squad-{tank_index + 1}",
                "robots": tank_robots,
                "wait_between_spawns": None,
                "wait_before_starting": None,
                "wait_all_dead": None,
                "wait_all_spawn": None,
                "total_count": len(tank_robots),
                "max_active": 1,
                "spawn_count": 1
            }
            squads.append(squad_parameters)

        return squads

    def adjust_squads(self, squads, wave_number):
        adjusted_squads = []
        buffer = []

        for squad_data in squads:
            robots = squad_data["robots"]
            if len(robots) < 2 and not squad_data["name"].startswith("Tank-Squad"):
                buffer.extend(robots)
            else:
                if buffer:
                    robots.extend(buffer)
                    buffer = []
                adjusted_squads.append(squad_data)

        if buffer:
            if adjusted_squads:
                adjusted_squads[-1]["robots"].extend(buffer)
            else:
                adjusted_squads.append({
                    "name": f"Squad-{wave_number}-1",
                    "robots": buffer,
                    "wait_between_spawns": None,
                    "wait_before_starting": None,
                    "wait_all_dead": None,
                    "wait_all_spawn": None,
                    "total_count": len(buffer),
                    "max_active": max(1, len(buffer) // 2),
                    "spawn_count": len(buffer)
                })

        return adjusted_squads

    def assign_squad_parameters(self, squads, wave_number):
        for i, squad in enumerate(squads):
            squad["wait_between_spawns"] = round(random.uniform(1.0, 3.0) * (wave_number + 1), 2)
            squad["wait_before_starting"] = round(random.uniform(1.0, 5.0) * wave_number, 2)

            other_squads = squads[:i]
            if other_squads:
                squad["wait_all_dead"] = random.choice([s["name"] for s in other_squads])
                remaining_squads = [s["name"] for s in other_squads if s["name"] != squad["wait_all_dead"]]
                squad["wait_all_spawn"] = random.choice(remaining_squads) if remaining_squads else None
            else:
                squad["wait_all_dead"] = None
                squad["wait_all_spawn"] = None

    def create_robots(self, count, squad_name, wave_number, path, tank_only=False):
        robots = []
        giant_limit = max(1, int(count * 0.25))
        giant_count = 0

        for _ in range(count):
            if tank_only:
                robot_type = "Tank"
            else:
                robot_type = random.choice(list(self.default_robot_params.keys()))

            size = self.default_robot_params[robot_type]["size"]
            speed = self.default_robot_params[robot_type]["speed"]
            skill = self.default_robot_params[robot_type]["skill"]

            if robot_type != "Tank" and random.random() < (self.difficulty * 0.1):
                size = random.uniform(1.25, 2.0)
                if giant_count >= giant_limit:
                    size = self.default_robot_params[robot_type]["size"]
                else:
                    giant_count += 1

            robot = Robot(
                robot_type=robot_type,
                size=size,
                squad=squad_name,
                speed=speed,
                skill=skill,
                path=path
            )
            robots.append(robot)
        return robots


    def print_wave(self, wave_number, squads, path, helpers):
        console = Console()
        table = Table(title=f"Wave {wave_number} (Path: {path})", title_style="bold cyan")
        table.add_column("Squad", style="bold yellow")
        table.add_column("Robot", style="bold green")
        table.add_column("Size", justify="center", style="cyan")
        table.add_column("Health", justify="right", style="green")
        table.add_column("Power", style="red")
        table.add_column("Weapons", style="bold magenta")
        table.add_column("ItemAttributes", style="dim")
        table.add_column("CharacterAttributes", style="dim")
        table.add_column("Cosmetics", style="bold blue")

        for squad in squads:
            console.print(f"[bold blue]Squad: {squad['name']}[/bold blue]")
            console.print(f"  WaitBetweenSpawns: {squad['wait_between_spawns']}")
            console.print(f"  WaitBeforeStarting: {squad['wait_before_starting']}")
            console.print(f"  WaitAllDead: {squad['wait_all_dead']}")
            console.print(f"  WaitAllSpawn: {squad['wait_all_spawn']}")
            console.print(f"  TotalCount: {squad['total_count']}, MaxActive: {squad['max_active']}, SpawnCount: {squad['spawn_count']}")

            for robot in squad["robots"]:
                weapon_info = ", ".join([f"{type}: {data['Name']}" for type, data in robot.weapons.items()])
                item_attributes = ", ".join([f"{attr}: {value}" for type, data in robot.weapons.items() for attr, value in data["ItemAttributes"].items()])
                character_attributes = ", ".join([f"{attr}: {value}" for attr, value in robot.character_attributes.items()])
                cosmetics_info = ", ".join([cosmetic["Name"] for cosmetic in robot.cosmetics])
                table.add_row(
                    squad["name"],
                    robot.robot_type,
                    f"{robot.size:.2f}",
                    str(robot.health),
                    f"{robot.power:.2f}",
                    weapon_info,
                    item_attributes,
                    character_attributes,
                    cosmetics_info
                )

        # Print helpers as a separate column
        helper_table = Table(title="Helpers", title_style="bold magenta")
        helper_table.add_column("Type", style="bold green")
        helper_table.add_column("Health", justify="right", style="green")
        helper_table.add_column("Power", style="red")

        for helper in helpers:
            helper_table.add_row(
                helper.robot_type,
                str(helper.health),
                f"{helper.power:.2f}"
            )

        console.print(table)
        console.print(helper_table)


if __name__ == "__main__":
    def main():
        waves =         1
        difficulty =    1
        complexity =    1
        progressive =   1.175
        
        available_paths = [
            {"standard_path": "Path_A", "tank_paths": ["Tank_Path_A", "Tank_Path_B"]},
            {"standard_path": "Path_B", "tank_paths": ["Tank_Path_C", "Tank_Path_D"]},
            {"standard_path": "Path_C", "tank_paths": ["Tank_Path_E", "Tank_Path_F"]},
            {"standard_path": "Path_D", "tank_paths": ["Tank_Path_G", "Tank_Path_H"]},
        ]

        mission = Mission(waves, difficulty, progression_factor = progressive, available_paths = available_paths)

        print("Mission Parameters:")
        print(f"  Waves: {waves}")
        print(f"  Difficulty: {difficulty}")
        print(f"  Complexity: {complexity}")
        print("  Available Paths:")
        for path in available_paths:
            print(f"    Standard Path: {path['standard_path']}, Tank Paths: {', '.join(path['tank_paths'])}")

        for wave_number in range(1, waves + 1):
            squads, path, helpers = mission.generate_wave(wave_number)
            print(f"\n[bold yellow]Generated Wave {wave_number}:[/bold yellow]")
            mission.print_wave(wave_number, squads, path, helpers)
        
    main()

