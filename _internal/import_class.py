from typing import Dict, List, Any
from pop_file_parser.parser import Mission
from pop_file_parser.models.tf_bot import TFBot
from pop_file_parser.models.wave import Wave
from pop_file_parser.valve_parser import ValveFormat
from pop_file_parser.models.wave_spawn import WaveSpawn

class PopFileImporter:
    """Класс для импорта .pop файлов в формат Gray Factory"""
    
    def __init__(self, wave_manager=None, squad_settings=None):
        self.wave_manager = wave_manager
        self.squad_settings = squad_settings
        self._class_map = {
            "Scout": "Scout",
            "Soldier": "Soldier",
            "Pyro": "Pyro",
            "Demoman": "Demoman",
            "Heavy": "Heavy",
            "Engineer": "Engineer",
            "Medic": "Medic",
            "Sniper": "Sniper",
            "Spy": "Spy"
        }
        self._skill_map = {
            "Easy": "Easy",
            "Normal": "Normal",
            "Hard": "Hard",
            "Expert": "Expert"
        }

    def import_pop_file(self, file_path: str) -> Dict[str, Any]:
        """
        Импортирует .pop файл и конвертирует его в формат Gray Factory
        
        Args:
            file_path: Путь к .pop файлу
            
        Returns:
            Dict с данными в формате Gray Factory
        """            
        # Создаем экземпляр парсера
        valve_parser = ValveFormat()
        
        # Парсим содержимое файла
        parsed_data = valve_parser.parse_file(file_path)
        
        # Получаем данные миссии
        mission_data = parsed_data.get('population', {})
        
        # Конвертируем в формат Gray Factory
        result = {
            "WaveManager": self._convert_waves(mission_data.get('Wave', [])),
            "InitialSettings": {
                "StartingCurrency": int(mission_data.get('StartingCurrency', '400')),
                "RespawnWaveTime": int(mission_data.get('RespawnWaveTime', '6')),
                "CanBotsAttackWhileInSpawnRoom": mission_data.get('CanBotsAttackWhileInSpawnRoom', 'no').lower() == 'yes',
                "Advanced": mission_data.get('Advanced', '0') == '1'
            }
        }
        
        return result

    def _convert_initial_settings(self, mission: Mission) -> Dict[str, Any]:
        """Конвертирует начальные настройки миссии"""
        return {
            "StartingCurrency": mission.starting_currency,
            "RespawnWaveTime": mission.respawn_wave_time,
            "CanBotsAttackWhileInSpawnRoom": mission.can_bots_attack_while_in_spawn_room,
            "Advanced": mission.advanced
        }

    def _convert_waves(self, waves: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Конвертирует волны в формат Gray Factory"""
        result = {}
        
        for i, wave in enumerate(waves, 1):
            wave_spawns = wave.get('WaveSpawn', [])
            if not isinstance(wave_spawns, list):
                wave_spawns = [wave_spawns]
                
            wave_data = {
                "Squads": self._convert_wave_spawns(wave_spawns),
                "WaitWhenDone": wave.get('WaitWhenDone', ''),
                "Checkpoint": wave.get('Checkpoint', '').lower() == 'yes'
            }
            
            result[f"Wave_{i}"] = wave_data
            
        return result

    def _convert_wave_spawns(self, wave_spawns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Конвертирует спавны волны в формат Gray Factory"""
        result = {}
        
        for i, spawn in enumerate(wave_spawns, 1):
            squad = spawn.get('Squad', {})
            squad_data = {
                "Name": spawn.get('Name', f'Squad_{i}'),
                "TotalCurrency": self._to_int(spawn.get('TotalCurrency', '0')),
                "TotalCount": self._to_int(spawn.get('TotalCount', '1')),
                "MaxActive": self._to_int(spawn.get('MaxActive', '1')),
                "SpawnCount": self._to_int(spawn.get('SpawnCount', '1')),
                "WaitBeforeStarting": self._to_int(spawn.get('WaitBeforeStarting', '0')),
                "WaitBetweenSpawns": self._to_int(spawn.get('WaitBetweenSpawns', '0')),
                "Where": spawn.get('Where', 'spawnbot'),
                "Support": spawn.get('Support', '0') == '1',
                "RandomSpawn": spawn.get('RandomSpawn', '0') == '1',
                "WaitForAllSpawned": spawn.get('WaitForAllSpawned', ''),
                "WaitForAllDead": spawn.get('WaitForAllDead', '')
            }

            # Конвертируем TFBot или Tank
            if 'TFBot' in squad:
                tf_bot = squad['TFBot']
                if isinstance(tf_bot, list):
                    # Если это список ботов
                    squad_data["Bots"] = [self._convert_bot_to_mercenary(bot) for bot in tf_bot]
                else:
                    # Если это один бот
                    squad_data["Bot"] = self._convert_bot_to_mercenary(tf_bot)
            elif 'Tank' in squad:
                squad_data["Tank"] = self._convert_tank(squad['Tank'])
            
            result[squad_data["Name"]] = squad_data
            
        return result

    def _to_int(self, value, default=0):
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        try:
            return int(str(value).replace(',', '.'))
        except Exception:
            try:
                return int(float(str(value).replace(',', '.')))
            except Exception:
                return default

    def _to_float(self, value, default=0.0):
        if isinstance(value, float):
            return value
        if isinstance(value, int):
            return float(value)
        try:
            return float(str(value).replace(',', '.'))
        except Exception:
            return default

    def _convert_bot_to_mercenary(self, tf_bot: Dict[str, Any]) -> Dict[str, Any]:
        """Конвертирует TFBot в формат Mercenary"""
        if not tf_bot:
            return {}

        result = {
            "Class": self._class_map.get(tf_bot.get('Class', 'Scout'), "Scout"),
            "Name": tf_bot.get('Name', ''),
            "Health": self._to_int(tf_bot.get('Health', '0')),
            "Scale": self._to_float(tf_bot.get('Scale', '1.0')),
            "Skill": self._skill_map.get(tf_bot.get('Skill', 'Normal'), "Normal"),
            "ClassIcon": tf_bot.get('ClassIcon', ''),
            "WeaponRestrictions": tf_bot.get('WeaponRestrictions', ''),
            "MaxVisionRange": 0  # По умолчанию
        }
        
        # Обработка атрибутов
        attributes = tf_bot.get('Attributes', '')
        attr_list = []
        if isinstance(attributes, str) and attributes:
            attr_list = attributes.split()
        elif isinstance(attributes, list):
            attr_list = attributes
        elif attributes:
            attr_list = [attributes]
        if attr_list:
            result["Attributes"] = self._convert_attributes(attr_list)
        
        # Обработка предметов (косметика и оружие)
        items = tf_bot.get('Item', [])
        if isinstance(items, str):
            items = [items]
        result["Cosmetics"] = self._convert_items_to_cosmetics(items)
        
        # Обработка характеристик
        if 'CharacterAttributes' in tf_bot:
            result["CharacterAttributes"] = tf_bot['CharacterAttributes']
            
        # Обработка атрибутов предметов
        if 'ItemAttributes' in tf_bot:
            result["ItemAttributes"] = tf_bot['ItemAttributes']
            
        return result

    def _convert_attributes(self, attributes: list) -> List[Dict[str, Any]]:
        """Конвертирует атрибуты в формат Gray Factory"""
        result = []
        for attr in attributes:
            if isinstance(attr, dict):
                # Если это словарь, добавляем все пары ключ-значение
                for k, v in attr.items():
                    result.append({"Name": k, "Value": v})
            else:
                result.append({"Name": str(attr), "Value": 1})
        return result

    def _convert_items_to_cosmetics(self, items: List[str]) -> List[Dict[str, Any]]:
        """Конвертирует предметы в формат косметики Gray Factory"""
        result = []
        
        for item in items:
            result.append({
                "Name": item,
                "Painted": False,
                "Style": 0
            })
            
        return result

    def _convert_weapons(self, weapons: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Конвертирует оружие в формат Gray Factory"""
        result = []
        
        for slot, weapon_data in weapons.items():
            weapon = {
                "Name": weapon_data.get("Name", ""),
                "Slot": slot,
                "Attributes": []
            }
            
            if "Attributes" in weapon_data:
                for attr_name, attr_value in weapon_data["Attributes"].items():
                    weapon["Attributes"].append({
                        "Name": attr_name,
                        "Value": attr_value
                    })
                    
            result.append(weapon)
            
        return result

    def _convert_templates(self, templates: Dict[str, Any]) -> Dict[str, Any]:
        """Конвертирует шаблоны в формат Gray Factory"""
        result = {}
        
        if not templates:
            return result
            
        for name, template in templates.items():
            if hasattr(template, "tf_bot"):
                result[name] = self._convert_bot_to_mercenary(template.tf_bot)
                
        return result

    def _convert_tank(self, tank_data: Dict[str, Any]) -> Dict[str, Any]:
        """Конвертирует Tank в формат Gray Factory"""
        if not tank_data:
            return {}
            
        result = {
            "Name": tank_data.get('Name', 'Tank'),
            "Health": self._to_int(tank_data.get('Health', '25000')),
            "Speed": self._to_int(tank_data.get('Speed', '75')),
            "StartingPathTrackNode": tank_data.get('StartingPathTrackNode', '')
        }
        
        return result
