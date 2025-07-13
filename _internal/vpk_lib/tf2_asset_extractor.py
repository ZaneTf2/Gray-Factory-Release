from typing import List, Optional
from pathlib import Path

from .vpk_reader import VPKReader
from .model_manager import ModelManager, ModelFiles
from .texture_manager import TextureManager

class TF2AssetExtractor:
    """Главный класс для извлечения моделей и текстур из TF2"""
    
    def __init__(self, game_dir: str, output_dir: str, model_dirs: list = None, texture_dirs: list = None):
        """
        Инициализирует экстрактор
        
        Args:
            game_dir: Путь к директории TF2
            output_dir: Директория для сохранения извлеченных файлов
            model_dirs: Список дополнительных директорий для поиска моделей
            texture_dirs: Список дополнительных директорий для поиска текстур
        """
        self.game_dir = Path(game_dir)
        self.output_dir = Path(output_dir)
        model_dirs = model_dirs or []
        texture_dirs = texture_dirs or []
        # Инициализируем VPK ридеры с поддержкой поиска в папках
        self.models_vpk = VPKReader(str(self.game_dir / 'tf2_misc_dir.vpk'), search_dirs=model_dirs)
        self.textures_vpk = VPKReader(str(self.game_dir / 'tf2_textures_dir.vpk'), search_dirs=texture_dirs)
        
        # Создаем менеджеры
        self.model_manager = ModelManager(self.models_vpk, str(self.output_dir))
        self.texture_manager = TextureManager(self.textures_vpk, str(self.output_dir))
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def close(self):
        """Закрывает VPK файлы"""
        self.models_vpk.close()
        self.textures_vpk.close()
        
    def extract_bot_models(self, output_callback=None) -> List[ModelFiles]:
        """
        Извлекает все модели ботов и их текстуры
        
        Args:
            output_callback: Функция обратного вызова для вывода прогресса
            
        Returns:
            List[ModelFiles]: Список найденных и извлеченных моделей
        """
        if output_callback:
            output_callback("Поиск моделей ботов...")
            
        # Ищем все модели ботов
        models = self.model_manager.find_model_files("models/bots/**/*.mdl")
        
        if output_callback:
            output_callback(f"Найдено {len(models)} моделей")
            
        # Извлекаем модели
        for i, model in enumerate(models, 1):
            if output_callback:
                output_callback(f"Извлечение модели {i}/{len(models)}: {model.base_name}")
            self.model_manager.extract_model(model)
            
        if output_callback:
            output_callback("Поиск текстур для моделей...")
            
        # Ищем и извлекаем текстуры для каждой модели
        for model in models:
            if output_callback:
                output_callback(f"Обработка текстур для {model.base_name}")
                
            # Ищем текстуры для конкретной модели
            texture_pattern = f"materials/models/bots/{model.base_name}/*.vtf"
            textures = list(self.textures_vpk.find_files(texture_pattern))
            
            if output_callback:
                output_callback(f"Найдено {len(textures)} текстур")
                
            # Конвертируем текстуры
            for i, texture in enumerate(textures, 1):
                if output_callback:
                    output_callback(f"Конвертация текстуры {i}/{len(textures)}: {Path(texture).stem}")
                self.texture_manager.extract_and_convert_texture(texture)
                
        return models
        
    def get_model_info(self, model: ModelFiles) -> dict:
        """
        Получает информацию о модели
        
        Args:
            model: Модель для анализа
            
        Returns:
            dict: Словарь с информацией о модели
        """
        return {
            "name": model.base_name,
            "files": {
                "mdl": str(self.output_dir / model.mdl_path) if model.mdl_path else None,
                "phy": str(self.output_dir / model.phy_path) if model.phy_path else None,
                "vtx": str(self.output_dir / model.vtx_path) if model.vtx_path else None,
                "vvd": str(self.output_dir / model.vvd_path) if model.vvd_path else None,
            },
            "textures": [
                str(path) for path in 
                Path(self.output_dir / "materials/models/bots" / model.base_name).glob("*.png")
            ]
        }
